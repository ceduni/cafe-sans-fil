"""
Module for handling cafe-related routes.
"""

from typing import Dict, List, Optional

from fastapi import APIRouter, Depends, HTTPException, Path, Query, Request, status

from app.auth.dependencies import get_current_user
from app.cafe.models import CafeView, Role
from app.cafe.schemas import (
    CafeCreate,
    CafeOut,
    CafeShortOut,
    CafeUpdate,
    StaffCreate,
    StaffOut,
    StaffUpdate,
)
from app.cafe.service import CafeService
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
    response_model=List[CafeShortOut],
    summary="List Cafes",
    description="Retrieve a list of all cafes with short information.",
)
async def list_cafes(
    request: Request,
    is_open: Optional[bool] = Query(None, description="Filter cafes by open status"),
    sort_by: Optional[str] = Query(
        "name", description="Sort cafes by a specific field"
    ),
    page: Optional[int] = Query(
        1, description="Specify the page number for pagination"
    ),
    limit: Optional[int] = Query(
        40, description="Set the number of cafes to return per page"
    ),
):
    """Retrieve a list of all cafes with short information."""
    query_params = dict(request.query_params)
    parsed_params = parse_query_params(query_params)
    return await CafeService.list_cafes(**parsed_params)


@cafe_router.get(
    "/cafes/{cafe_slug}",
    response_model=CafeOut,
    summary="Get Cafe",
    description="Retrieve detailed information about a specific cafe.",
)
async def get_cafe(
    cafe_slug: str = Path(..., description="The slug or ID of the cafe")
):
    """Retrieve detailed information about a specific cafe."""
    cafe = await CafeService.retrieve_cafe(cafe_slug)
    if not cafe:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Café not found"
        )
    return cafe


@cafe_router.post(
    "/cafes",
    summary="⚫ Create Cafe",
    description="Create a new cafe with the provided information.",
)
async def create_cafe(cafe: CafeCreate, current_user: User = Depends(get_current_user)):
    """Create a new cafe with the provided information."""
    if "7802085" != current_user.username:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail="Access forbidden"
        )
    try:
        return await CafeService.create_cafe(cafe)
    except ValueError as e:
        if "duplicate" in str(e).lower() and len(str(e)) < 100:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=str(e))
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT, detail="Cafe already exists"
        )


@cafe_router.put(
    "/cafes/{cafe_slug}",
    summary="🔴 Update Cafe",
    description="Update the details of an existing cafe.",
)
async def update_cafe(
    cafe_slug: str, cafe: CafeUpdate, current_user: User = Depends(get_current_user)
) -> CafeOut:
    """Update the details of an existing cafe."""
    cafe_obj = await CafeService.retrieve_cafe(cafe_slug)
    if not cafe_obj:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Café not found"
        )
    try:
        await CafeService.is_authorized_for_cafe_action(
            cafe_obj.id, current_user, [Role.ADMIN]
        )
        return await CafeService.update_cafe(cafe_obj.id, cafe)
    except ValueError as e:
        if str(e) == "Cafe not found":
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
        elif str(e) == "Access forbidden":
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=str(e))
        elif "duplicate" in str(e).lower() and len(str(e)) < 100:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=str(e))
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT, detail="Cafe already exists"
        )


# --------------------------------------
#               Staff
# --------------------------------------


@cafe_router.get(
    "/cafes/{cafe_slug}/staff",
    response_model=List[StaffOut],
    summary="List Staff",
    description="Retrieve a list of all staff members for a specific cafe.",
)
async def list_staff(
    cafe_slug: str = Path(..., description="The slug or ID of the cafe")
):
    """Retrieve a list of all staff members for a specific cafe."""
    cafe_obj = await CafeService.retrieve_cafe(cafe_slug)
    if not cafe_obj:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Café not found"
        )
    return await CafeService.list_staff_members(cafe_obj.id)


@cafe_router.post(
    "/cafes/{cafe_slug}/staff",
    response_model=StaffOut,
    summary="🔴 Create Staff Member",
    description="Add a new staff member to a specific cafe.",
)
async def create_staff_member(
    cafe_slug: str, staff: StaffCreate, current_user: User = Depends(get_current_user)
):
    """Add a new staff member to a specific cafe."""
    cafe_obj = await CafeService.retrieve_cafe(cafe_slug)
    if not cafe_obj:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Café not found"
        )

    user = await CafeService.retrieve_staff_member(cafe_obj.id, staff.username)
    if user:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT, detail="Staff member already exists"
        )

    user = await UserService.retrieve_user(staff.username)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="User not found"
        )

    try:
        await CafeService.is_authorized_for_cafe_action(
            cafe_obj.id, current_user, [Role.ADMIN]
        )
    except ValueError as e:
        if str(e) == "Cafe not found":
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
        elif str(e) == "Access forbidden":
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=str(e))

    return await CafeService.create_staff_member(cafe_obj.id, staff)


@cafe_router.put(
    "/cafes/{cafe_slug}/staff/{username}",
    response_model=StaffOut,
    summary="🔴 Update Staff Member",
    description="Update details of an existing staff member.",
)
async def update_staff_member(
    cafe_slug: str,
    username: str,
    staff: StaffUpdate,
    current_user: User = Depends(get_current_user),
) -> StaffOut:
    """Update details of an existing staff member."""
    cafe_obj = await CafeService.retrieve_cafe(cafe_slug)
    if not cafe_obj:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Café not found"
        )

    try:
        await CafeService.is_authorized_for_cafe_action(
            cafe_obj.id, current_user, [Role.ADMIN]
        )
        return await CafeService.update_staff_member(cafe_obj.id, username, staff)
    except ValueError as e:
        if str(e) == "Cafe not found":
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
        elif str(e) == "Access forbidden":
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=str(e))
        elif str(e) == "Staff member not found":
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))


@cafe_router.delete(
    "/cafes/{cafe_slug}/staff/{username}",
    summary="🔴 Delete Staff Member",
    description="Remove a staff member from a cafe.",
)
async def delete_staff_member(
    cafe_slug: str, username: str, current_user: User = Depends(get_current_user)
):
    """Remove a staff member from a cafe."""
    cafe_obj = await CafeService.retrieve_cafe(cafe_slug)
    if not cafe_obj:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Café not found"
        )

    try:
        await CafeService.is_authorized_for_cafe_action(
            cafe_obj.id, current_user, [Role.ADMIN]
        )
        await CafeService.delete_staff_member(cafe_obj.id, username)
    except ValueError as e:
        if str(e) == "Cafe not found":
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
        elif str(e) == "Access forbidden":
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=str(e))
        elif str(e) == "Staff member not found":
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))

    return {"message": f"Staff member {username} has been successfully deleted."}


# --------------------------------------
#               Sales Report
# --------------------------------------


@cafe_router.get(
    "/cafes/{cafe_slug}/sales-report",
    summary="🔴 Get Sales Report",
    description="Retrieve a sales report for a specific cafe.",
)
async def get_sales_report(
    cafe_slug: str = Path(..., description="The slug or ID of the cafe"),
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
    """Retrieve a sales report for a specific cafe."""
    cafe_obj = await CafeService.retrieve_cafe(cafe_slug)
    if not cafe_obj:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Café not found"
        )

    try:
        await CafeService.is_authorized_for_cafe_action(
            cafe_obj.id, current_user, [Role.ADMIN]
        )
    except ValueError as e:
        if str(e) == "Cafe not found":
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
        elif str(e) == "Access forbidden":
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=str(e))

    report_data = await OrderService.generate_sales_report_data(
        cafe_obj.id, start_date, end_date, report_type
    )
    return report_data
