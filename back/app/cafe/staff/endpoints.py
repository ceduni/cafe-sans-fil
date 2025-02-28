"""
Module for handling staff-related routes.
"""

from beanie import PydanticObjectId
from fastapi import APIRouter, Depends, HTTPException, Path, status

from app.auth.dependencies import get_current_user
from app.cafe.models import Role
from app.cafe.service import CafeService
from app.cafe.staff.service import StaffService
from app.models import ErrorResponse
from app.user.models import User
from app.user.service import UserService

staff_router = APIRouter()


@staff_router.post(
    "/cafes/{slug}/staff/{role}/{id}",
    responses={
        401: {"model": ErrorResponse},
        403: {"model": ErrorResponse},
        404: {"model": ErrorResponse},
        409: {"model": ErrorResponse},
    },
)
async def add_staff(
    slug: str = Path(..., description="Slug of the cafe"),
    role: str = Path(..., description="Role of the staff"),
    id: PydanticObjectId = Path(..., description="ID of the user"),
    current_user: User = Depends(get_current_user),
):
    """Add a staff member to a cafe. (`admin`)."""
    cafe = await CafeService.get(slug)
    if not cafe:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=[{"msg": "A cafe with this slug does not exist."}],
        )

    if role.upper() not in [r.name for r in Role]:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=[{"msg": "A role with this name does not exist."}],
        )

    user = await UserService.get(id)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=[{"msg": "A user with this username does not exist."}],
        )

    if await StaffService.is_staff(cafe, id):
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=[{"msg": "User is already a staff member of this cafe."}],
        )

    await CafeService.is_authorized_for_cafe_action(cafe, current_user, [Role.ADMIN])

    return await StaffService.add(cafe, role, id)


@staff_router.delete(
    "/cafes/{slug}/staff/{role}/{id}",
    responses={
        401: {"model": ErrorResponse},
        403: {"model": ErrorResponse},
        404: {"model": ErrorResponse},
    },
)
async def remove_staff(
    slug: str = Path(..., description="Slug of the cafe"),
    role: str = Path(..., description="Role of the staff"),
    id: PydanticObjectId = Path(..., description="ID of the user"),
    current_user: User = Depends(get_current_user),
):
    """Remove a staff member from a cafe. (`admin`)."""
    cafe = await CafeService.get(slug)
    if not cafe:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=[{"msg": "A cafe with this slug does not exist."}],
        )

    if role.upper() not in [r.name for r in Role]:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=[{"msg": "A role with this name does not exist."}],
        )

    user = await UserService.get(id)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=[{"msg": "A user with this username does not exist."}],
        )

    if not await StaffService.is_staff(cafe, id):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=[{"msg": "User is not a staff member of this cafe."}],
        )

    await CafeService.is_authorized_for_cafe_action(cafe, current_user, [Role.ADMIN])

    return await StaffService.remove(cafe, role, id)
