"""
Module for handling order-related routes.
"""

from typing import Optional

from beanie import PydanticObjectId
from fastapi import APIRouter, Depends, HTTPException, Path, Query, Request, status
from fastapi_pagination.ext.beanie import paginate
from fastapi_pagination.links import Page

from app.auth.dependencies import get_current_user
from app.cafe.models import Role
from app.cafe.service import CafeService
from app.models import ErrorResponse
from app.order.models import OrderCreate, OrderOut, OrderUpdate
from app.order.service import OrderService
from app.service import parse_query_params
from app.user.models import User

order_router = APIRouter()


@order_router.get(
    "/orders",
    response_model=Page[OrderOut],
    responses={
        401: {"model": ErrorResponse},
        403: {"model": ErrorResponse},
    },
)
async def get_orders(
    request: Request,
    sort_by: Optional[str] = Query(None, description="Sort by a specific field"),
    current_user: User = Depends(get_current_user),
):
    """Get a list of orders. (`member`)"""
    filters = parse_query_params(dict(request.query_params))
    orders = await OrderService.get_all(**filters)
    return await paginate(orders)


@order_router.get(
    "/orders/{id}",
    response_model=OrderOut,
    responses={
        401: {"model": ErrorResponse},
        403: {"model": ErrorResponse},
        404: {"model": ErrorResponse},
    },
)
async def get_order(
    id: PydanticObjectId = Path(..., description="ID of the order"),
    current_user: User = Depends(get_current_user),
) -> OrderOut:
    """Get an order. (`member`)"""
    try:
        order = await OrderService.get(id)
        if not order:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Order not found"
            )

        # Authorization check
        if (
            order.user_username != current_user.username
            and not await CafeService.is_authorized_for_cafe_action(
                order.cafe_slug, current_user, [Role.ADMIN, Role.VOLUNTEER]
            )
        ):
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN, detail="Access forbidden"
            )

        return order
    except ValueError as e:
        if str(e) == "Cafe not found":
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
        elif str(e) == "Access forbidden":
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=str(e))


@order_router.post(
    "/orders",
    response_model=OrderOut,
    responses={
        401: {"model": ErrorResponse},
        403: {"model": ErrorResponse},
        404: {"model": ErrorResponse},
    },
)
async def create_order(
    data: OrderCreate, current_user: User = Depends(get_current_user)
):
    """Create an order. (`member`)"""
    cafe = await CafeService.get(data.cafe_slug)
    if not cafe:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Cafe not found"
        )
    return await OrderService.create(data, current_user.username)


@order_router.put(
    "/orders/{id}",
    response_model=OrderOut,
    responses={
        401: {"model": ErrorResponse},
        403: {"model": ErrorResponse},
        404: {"model": ErrorResponse},
    },
)
async def update_order(
    data: OrderUpdate,
    id: PydanticObjectId = Path(..., description="ID of the order"),
    current_user: User = Depends(get_current_user),
):
    """Update an order. (`member`)"""
    try:
        order = await OrderService.get(id)
        if not order:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Order not found"
            )

        # Authorization check
        if (
            order.user_username != current_user.username
            and not await CafeService.is_authorized_for_cafe_action(
                order.cafe_slug, current_user, [Role.ADMIN, Role.VOLUNTEER]
            )
        ):
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN, detail="Access forbidden"
            )

        return await OrderService.update(id, data)
    except ValueError as e:
        if str(e) == "Cafe not found":
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
        elif str(e) == "Access forbidden":
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=str(e))
