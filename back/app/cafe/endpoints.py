"""
Module for handling cafe-related routes.
"""

from typing import Optional

from fastapi import APIRouter, Depends, HTTPException, Path, Query, Request, status
from fastapi_pagination.ext.beanie import paginate
from fastapi_pagination.links import Page

from app.auth.dependencies import get_current_user
from app.cafe.models import (
    CafeCreate,
    CafeOut,
    CafeShortOut,
    CafeUpdate,
    CafeViewOut,
    Role,
    StaffCreate,
    StaffOut,
)
from app.cafe.service import CafeService
from app.models import ErrorResponse
from app.order.service import OrderService
from app.service import parse_query_params
from app.user.models import User
from app.user.service import UserService

cafe_router = APIRouter()


# --------------------------------------
#               Cafe
# --------------------------------------


@cafe_router.get(
    "/cafes",
    response_model=Page[CafeShortOut],
)
async def get_cafes(
    request: Request,
    is_open: Optional[bool] = Query(None, description="Filter by open status"),
    sort_by: Optional[str] = Query(None, description="Sort by a specific field"),
):
    """Get a list of cafes with basic information."""
    filters = parse_query_params(dict(request.query_params))
    cafes = await CafeService.get_all(**filters)
    return await paginate(cafes)


@cafe_router.post(
    "/cafes",
    response_model=CafeOut,
    responses={
        401: {"model": ErrorResponse},
        403: {"model": ErrorResponse},
        409: {"model": ErrorResponse},
    },
)
async def create_cafe(
    data: CafeCreate,
):
    """Create a cafe (`superuser`)."""
    return await CafeService.create(data)


@cafe_router.get(
    "/cafes/{slug}",
    response_model=CafeViewOut,
    responses={
        404: {"model": ErrorResponse},
    },
)
async def get_cafe(
    slug: str = Path(..., description="Slug of the cafe"),
):
    """Get a cafe with full details."""
    cafe = await CafeService.get(slug, as_view=True)
    if not cafe:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=[{"msg": "Café not found"}]
        )
    return cafe


@cafe_router.put(
    "/cafes/{slug}",
    response_model=CafeOut,
    responses={
        401: {"model": ErrorResponse},
        403: {"model": ErrorResponse},
        404: {"model": ErrorResponse},
        409: {"model": ErrorResponse},
    },
)
async def update_cafe(
    data: CafeUpdate,
    slug: str = Path(..., description="Slug of the cafe"),
    current_user: User = Depends(get_current_user),
):
    """Update a cafe (`admin`)."""
    cafe = await CafeService.get(slug)
    if not cafe:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Café not found"
        )
    try:
        await CafeService.is_authorized_for_cafe_action(
            cafe, current_user, [Role.ADMIN]
        )
        return await CafeService.update(cafe, data)
    except ValueError as e:
        if str(e) == "Access forbidden":
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=str(e))
        elif "duplicate" in str(e).lower() and len(str(e)) < 100:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=str(e))


# --------------------------------------
#               Staff
# --------------------------------------


@cafe_router.post(
    "/cafes/{slug}/staff",
    response_model=StaffOut,
    responses={
        401: {"model": ErrorResponse},
        403: {"model": ErrorResponse},
        404: {"model": ErrorResponse},
    },
)
async def create_staff_member(
    data: StaffCreate,
    slug: str = Path(..., description="Slug of the cafe"),
    current_user: User = Depends(get_current_user),
):
    """Add a staff member to a cafe. (`admin`)."""
    cafe = await CafeService.get(slug)
    if not cafe:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Café not found"
        )

    user = await CafeService.get_staff(cafe, data.username)
    if user:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT, detail="Staff member already exists"
        )

    user = await UserService.get(data.username)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="User not found"
        )

    try:
        await CafeService.is_authorized_for_cafe_action(
            cafe, current_user, [Role.ADMIN]
        )
    except ValueError as e:
        if str(e) == "Cafe not found":
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
        elif str(e) == "Access forbidden":
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=str(e))

    return await CafeService.create_staff(cafe, data)


# --------------------------------------
#               Sales Report
# --------------------------------------


@cafe_router.get(
    "/cafes/{slug}/sales-report",
    responses={
        401: {"model": ErrorResponse},
        403: {"model": ErrorResponse},
        404: {"model": ErrorResponse},
    },
)
async def get_sales_report(
    slug: str = Path(..., description="Slug of the cafe"),
    start_date: Optional[str] = Query(
        None, description="The start date of the reporting period"
    ),
    end_date: Optional[str] = Query(
        None, description="The end date of the reporting period"
    ),
    report_type: str = Query(
        "daily",
        description="The type of report to generate ('daily', 'weekly', 'monthly')",
    ),
    current_user: User = Depends(get_current_user),
):
    """Get a sales report for a cafe. (`admin`)"""
    cafe = await CafeService.get(slug)
    if not cafe:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Café not found"
        )

    try:
        await CafeService.is_authorized_for_cafe_action(
            cafe, current_user, [Role.ADMIN]
        )
    except ValueError as e:
        if str(e) == "Cafe not found":
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
        elif str(e) == "Access forbidden":
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=str(e))

    report_data = await OrderService.generate_sales_report_data(
        cafe, start_date, end_date, report_type
    )
    return report_data
