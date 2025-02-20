"""
Module for handling order-related routes.
"""

from typing import List

from beanie import PydanticObjectId
from fastapi import APIRouter, Depends, HTTPException, Path, Query, Request, status

from app.auth.dependencies import get_current_user
from app.cafe.models import Role
from app.cafe.service import CafeService
from app.order.schemas import OrderCreate, OrderOut, OrderUpdate
from app.order.service import OrderService
from app.user.models import User

order_router = APIRouter()


@order_router.get(
    "/orders",
    response_model=List[OrderOut],
    summary="🔵 List Orders",
    description="Retrieve a list of all orders.",
)
async def list_orders(
    request: Request,
    sort_by: str = Query(
        "-order_number", description="The field to sort the results by."
    ),
    page: int = Query(1, description="The page number to retrieve."),
    limit: int = Query(20, description="The number of orders to retrieve per page."),
    current_user: User = Depends(get_current_user),
) -> List[OrderOut]:
    """Retrieve a list of all orders."""
    filters = dict(request.query_params)
    return await OrderService.list_orders(**filters)


@order_router.get(
    "/orders/{order_id}",
    response_model=OrderOut,
    summary="🔵 Get Order",
    description="Retrieve detailed information about a specific order.",
)
async def get_order(
    order_id: PydanticObjectId = Path(
        ..., description="The unique identifier of the order"
    ),
    current_user: User = Depends(get_current_user),
) -> OrderOut:
    """Retrieve detailed information about a specific order."""
    try:
        order = await OrderService.retrieve_order(order_id)
        if not order:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Order not found"
            )

        # Authorization check
        if (
            order.user_username != current_user.username
            and not await CafeService.is_authorized_for_cafe_action_by_slug(
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
    summary="🔵 Create Order",
    description="Create a new order with the provided details.",
)
async def create_order(
    order: OrderCreate, current_user: User = Depends(get_current_user)
) -> OrderOut:
    """Create a new order with the provided details."""
    cafe = await CafeService.retrieve_cafe(order.cafe_slug)
    if not cafe:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Cafe not found"
        )
    return await OrderService.create_order(order, current_user.username)


@order_router.put(
    "/orders/{order_id}",
    response_model=OrderOut,
    summary="🔵 Update Order",
    description="Update the details of an existing order.",
)
async def update_order(
    orderUpdate: OrderUpdate,
    order_id: PydanticObjectId = Path(
        ..., description="The unique identifier of the order to update"
    ),
    current_user: User = Depends(get_current_user),
) -> OrderOut:
    """Update the details of an existing order."""
    try:
        order = await OrderService.retrieve_order(order_id)
        if not order:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Order not found"
            )

        # Authorization check
        if (
            order.user_username != current_user.username
            and not await CafeService.is_authorized_for_cafe_action_by_slug(
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
    response_model=List[OrderOut],
    summary="🔵 List User Orders",
    description="Retrieve a list of orders for a specific user.",
)
async def list_user_orders(
    request: Request,
    username: str = Path(..., description="The username of the user"),
    sort_by: str = Query(
        "-order_number", description="The field to sort the results by."
    ),
    page: int = Query(1, description="The page number to retrieve."),
    limit: int = Query(20, description="The number of orders to retrieve per page."),
    current_user: User = Depends(get_current_user),
) -> List[OrderOut]:
    """Retrieve a list of orders for a specific user."""
    # Authorization check
    if username != current_user.username:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail="Access forbidden"
        )
    filters = dict(request.query_params)
    return await OrderService.list_orders_for_user(username, **filters)


@order_router.get(
    "/cafes/{cafe_slug}/orders",
    response_model=List[OrderOut],
    summary="🟢 List Cafe Orders",
    description="Retrieve a list of orders for a specific cafe.",
)
async def list_cafe_orders(
    request: Request,
    cafe_slug: str = Path(..., description="The slug of the cafe"),
    sort_by: str = Query(
        None, description="The field to sort the results by. Default: -order_number"
    ),
    page: int = Query(1, description="The page number to retrieve."),
    limit: int = Query(20, description="The number of orders to retrieve per page."),
    current_user: User = Depends(get_current_user),
) -> List[OrderOut]:
    """Retrieve a list of orders for a specific cafe."""
    try:
        # Authorization check
        if not await CafeService.is_authorized_for_cafe_action_by_slug(
            cafe_slug, current_user, [Role.ADMIN, Role.VOLUNTEER]
        ):
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN, detail="Access forbidden"
            )

        filters = dict(request.query_params)
        return await OrderService.list_orders_for_cafe(cafe_slug, **filters)
    except ValueError as e:
        if str(e) == "Cafe not found":
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
        elif str(e) == "Access forbidden":
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=str(e))
