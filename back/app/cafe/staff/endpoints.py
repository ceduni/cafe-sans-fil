"""
Module for handling staff-related routes.
"""

from typing import Literal

from beanie import PydanticObjectId
from fastapi import APIRouter, Depends, HTTPException, Path, status

from app.cafe.permissions import AdminPermission
from app.cafe.service import CafeService
from app.cafe.staff.enums import Role
from app.cafe.staff.models import StaffWithOwnerOut
from app.cafe.staff.service import StaffService
from app.models import ErrorResponse
from app.user.service import UserService

staff_router = APIRouter()


@staff_router.get(
    "/cafes/{slug}/staff",
    response_model=StaffWithOwnerOut,
)
async def get_staff(
    slug: str = Path(..., description="Slug of the cafe"),
):
    """Get staff members."""
    staff = await StaffService.get(slug)
    if not staff:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=[{"msg": "A cafe with this slug does not exist."}],
        )

    return staff


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
    role: Literal[Role.ADMIN, Role.VOLUNTEER] = Path(
        ..., description="Role of the staff"
    ),
    id: PydanticObjectId = Path(..., description="ID of the user"),
):
    """Add a staff member to a cafe. (`ADMIN`)"""
    cafe = await CafeService.get(slug)
    if not cafe:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=[{"msg": "A cafe with this slug does not exist."}],
        )

    role = role.upper()
    if role not in [r.name for r in Role]:
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

    await UserService.add_cafe(user, cafe)
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
    role: Literal[Role.ADMIN, Role.VOLUNTEER] = Path(
        ..., description="Role of the staff"
    ),
    id: PydanticObjectId = Path(..., description="ID of the user"),
):
    """Remove a staff member from a cafe. (`ADMIN`)"""
    cafe = await CafeService.get(slug)
    if not cafe:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=[{"msg": "A cafe with this slug does not exist."}],
        )

    role = role.upper()
    if role not in [r.name for r in Role]:
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

    await UserService.remove_cafe(user, cafe)
    return await StaffService.remove(cafe, role, id)
