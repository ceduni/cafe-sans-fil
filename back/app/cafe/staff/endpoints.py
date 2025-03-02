"""
Module for handling staff-related routes.
"""

from beanie import PydanticObjectId
from fastapi import APIRouter, Depends, HTTPException, Path, status

from app.cafe.permissions import AdminPermission
from app.cafe.service import CafeService
from app.cafe.staff.enums import Role
from app.cafe.staff.service import StaffService
from app.models import ErrorResponse
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
    dependencies=[Depends(AdminPermission())],
)
async def add_staff(
    slug: str = Path(..., description="Slug of the cafe"),
    role: str = Path(..., description="Role of the staff"),
    id: PydanticObjectId = Path(..., description="ID of the user"),
):
    """Add a staff member to a cafe. (`ADMIN`)"""
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

    user = await UserService.get_by_id(id)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=[{"msg": "A user with this ID does not exist."}],
        )

    if await StaffService.is_staff(cafe, id):
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=[{"msg": "User is already a staff member of this cafe."}],
        )

    return await StaffService.add(cafe, role, id)


@staff_router.delete(
    "/cafes/{slug}/staff/{role}/{id}",
    responses={
        401: {"model": ErrorResponse},
        403: {"model": ErrorResponse},
        404: {"model": ErrorResponse},
    },
    dependencies=[Depends(AdminPermission())],
)
async def remove_staff(
    slug: str = Path(..., description="Slug of the cafe"),
    role: str = Path(..., description="Role of the staff"),
    id: PydanticObjectId = Path(..., description="ID of the user"),
):
    """Remove a staff member from a cafe. (`ADMIN`)"""
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

    user = await UserService.get_by_id(id)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=[{"msg": "A user with this ID does not exist."}],
        )

    if not await StaffService.is_staff(cafe, id):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=[{"msg": "User is not a staff member of this cafe."}],
        )

    return await StaffService.remove(cafe, role, id)
