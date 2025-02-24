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
from app.order.models import OrderCreate, OrderOut, OrderUpdate
from app.order.service import OrderService
from app.service import parse_query_params
from app.user.models import User

order_router = APIRouter()


@order_router.get(
    "/orders",
    response_model=Page[OrderOut],
)
async def get_orders(
    request: Request,
    sort_by: Optional[str] = Query(None, description="Sort by a specific field"),
    current_user: User = Depends(get_current_user),
):
    """Get a list of orders. (`member`)"""
    filters = parse_query_params(dict(request.query_params))
    orders = await OrderService.get_orders(**filters)
    return await paginate(orders)


@order_router.get(
    "/orders/{order_id}",
    response_model=OrderOut,
)
async def get_order(
    order_id: PydanticObjectId = Path(
        ..., description="The unique identifier of the order"
    ),
    current_user: User = Depends(get_current_user),
) -> OrderOut:
    """Get an order. (`member`)"""
    try:
        order = await OrderService.get_order(order_id)
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
)
async def create_order(
    order: OrderCreate, current_user: User = Depends(get_current_user)
) -> OrderOut:
    """Create an order. (`member`)"""
    cafe = await CafeService.get_cafe(order.cafe_slug)
    if not cafe:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Cafe not found"
        )
    return await OrderService.create_order(order, current_user.username)


@order_router.put(
    "/orders/{order_id}",
    response_model=OrderOut,
)
async def update_order(
    orderUpdate: OrderUpdate,
    order_id: PydanticObjectId = Path(
        ..., description="The unique identifier of the order to update"
    ),
    current_user: User = Depends(get_current_user),
) -> OrderOut:
    """Update an order. (`member`)"""
    try:
        order = await OrderService.get_order(order_id)
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

        return await OrderService.update_order(order_id, orderUpdate)
    except ValueError as e:
        if str(e) == "Cafe not found":
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
        elif str(e) == "Access forbidden":
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=str(e))


@order_router.get(
    "/users/{username}/orders",
    response_model=Page[OrderOut],
)
async def get_user_orders(
    request: Request,
    username: str = Path(..., description="Username of the user"),
    sort_by: Optional[str] = Query(None, description="Sort by a specific field"),
    current_user: User = Depends(get_current_user),
):
    """Get a list of orders for a user. (`member`)"""
    # Authorization check
    if username != current_user.username:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail="Access forbidden"
        )

    filters = parse_query_params(dict(request.query_params))
    orders = await OrderService.get_orders_for_user(username, **filters)
    return await paginate(orders)


@order_router.get(
    "/cafes/{cafe_slug}/orders",
    response_model=Page[OrderOut],
)
async def get_cafe_orders(
    request: Request,
    cafe_slug: str = Path(..., description="Slug of the cafe"),
    sort_by: Optional[str] = Query(None, description="Sort by a specific field"),
    current_user: User = Depends(get_current_user),
):
    """Get a list of orders for a cafe. (`volunteer`)"""
    try:
        # Authorization check
        if not await CafeService.is_authorized_for_cafe_action(
            cafe_slug, current_user, [Role.ADMIN, Role.VOLUNTEER]
        ):
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN, detail="Access forbidden"
            )

        filters = parse_query_params(dict(request.query_params))
        orders = await OrderService.get_orders_for_cafe(cafe_slug, **filters)
        return await paginate(orders)

    except ValueError as e:
        if str(e) == "Cafe not found":
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
        elif str(e) == "Access forbidden":
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=str(e))
