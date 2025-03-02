"""
Module for handling order-related routes.
"""

from typing import Optional, TypeVar

from beanie import PydanticObjectId
from fastapi import APIRouter, Depends, HTTPException, Path, Query, Request, status
from fastapi_pagination import Params
from fastapi_pagination.customization import CustomizedPage, UseParams
from fastapi_pagination.ext.beanie import paginate
from fastapi_pagination.links import Page

from app.auth.dependencies import get_current_user
from app.cafe.menu.item.service import ItemService
from app.cafe.permissions import VolunteerPermission
from app.cafe.service import CafeService
from app.models import ErrorResponse
from app.order.enums import OrderStatus
from app.order.models import OrderCreate, OrderOut, OrderUpdate
from app.order.service import OrderService
from app.service import parse_query_params
from app.user.models import User

T = TypeVar("T")


class OrderParams(Params):
    """Custom pagination parameters."""

    size: int = Query(20, ge=1, le=100, description="Page size")
    page: int = Query(1, ge=1, description="Page number")
    sort_by: Optional[str] = Query(None, description="Sort by a specific field")


OrderPage = CustomizedPage[
    Page[T],
    UseParams(OrderParams),
]


order_router = APIRouter()


@order_router.get(
    "/cafes/{slug}/orders",
    response_model=OrderPage[OrderOut],
    responses={
        401: {"model": ErrorResponse},
        403: {"model": ErrorResponse},
        404: {"model": ErrorResponse},
    },
    dependencies=[Depends(VolunteerPermission())],
)
async def list_cafe_orders(
    request: Request,
    slug: str = Path(..., description="Slug of the cafe"),
):
    """Get a list of orders for a cafe. (`VOLUNTEER`)"""
    cafe = await CafeService.get(slug)
    if not cafe:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=[{"msg": "A cafe with this slug does not exist."}],
        )

    filters = parse_query_params(dict(request.query_params))
    orders = await OrderService.get_all(cafe_id=cafe.id, to_list=False, **filters)
    return await paginate(orders)


@order_router.post(
    "/cafes/{slug}/orders",
    response_model=OrderOut,
    responses={
        401: {"model": ErrorResponse},
        403: {"model": ErrorResponse},
        404: {"model": ErrorResponse},
    },
    dependencies=[Depends(VolunteerPermission())],
)
async def create_cafe_order(
    data: OrderCreate,
    slug: str = Path(..., description="Slug of the cafe"),
    current_user: User = Depends(get_current_user),
):
    """Create an order. (`MEMBER`)"""
    cafe = await CafeService.get(slug)
    if not cafe:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=[{"msg": "A cafe with this slug does not exist."}],
        )

    requested_ids = [item.item_id for item in data.items]
    requested_str_ids = [str(id) for id in requested_ids]

    items = await ItemService.get_by_ids_and_cafe_id(requested_ids, cafe.id)

    found_ids = {str(item.id) for item in items}
    missing_ids = list(set(requested_str_ids) - found_ids)

    if missing_ids:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=[
                {
                    "msg": f"Items not found in this cafe",
                    "missing_ids": list(missing_ids),
                }
            ],
        )

    return await OrderService.create(current_user, cafe, items, data)


@order_router.put(
    "/cafes/{slug}/orders/{id}",
    response_model=OrderOut,
    responses={
        400: {"model": ErrorResponse},
        401: {"model": ErrorResponse},
        403: {"model": ErrorResponse},
        404: {"model": ErrorResponse},
    },
    dependencies=[Depends(VolunteerPermission())],
)
async def update_cafe_order(
    data: OrderUpdate,
    slug: str = Path(..., description="Slug of the cafe"),
    id: PydanticObjectId = Path(..., description="ID of the order"),
):
    """Update an order. (`VOLUNTEER`)"""
    cafe = await CafeService.get(slug)
    if not cafe:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=[{"msg": "A cafe with this slug does not exist."}],
        )

    order = await OrderService.get(id)
    if not order:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=[{"msg": "An order with this ID does not exist."}],
        )

    if order.cafe_id != cafe.id:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=[{"msg": "An order with this ID does not exist in this cafe."}],
        )

    if order.status in [OrderStatus.COMPLETED, OrderStatus.CANCELLED]:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=[
                {"msg": "An order with this ID is already completed or cancelled."}
            ],
        )

    return await OrderService.update(order, data)


@order_router.get(
    "/users/me/orders",
    response_model=OrderPage[OrderOut],
    responses={
        401: {"model": ErrorResponse},
        403: {"model": ErrorResponse},
    },
)
async def list_my_orders(
    request: Request,
    current_user: User = Depends(get_current_user),
):
    """Get a list of orders for the current user. (`MEMBER`)"""
    filters = parse_query_params(dict(request.query_params))
    orders = await OrderService.get_all(
        user_id=current_user.id, to_list=False, **filters
    )
    return await paginate(orders)


@order_router.put(
    "/users/me/orders/{id}",
    response_model=OrderOut,
    responses={
        401: {"model": ErrorResponse},
        403: {"model": ErrorResponse},
        404: {"model": ErrorResponse},
    },
)
async def update_my_order(
    data: OrderUpdate,
    id: PydanticObjectId = Path(..., description="ID of the order"),
    current_user: User = Depends(get_current_user),
):
    """Update an order. (`MEMBER`)"""
    order = await OrderService.get(id)
    if not order:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=[{"msg": "An order with this ID does not exist."}],
        )

    if current_user.id != order.user_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=[{"msg": "You cannot update an order that is not yours."}],
        )

    if order.status in [OrderStatus.COMPLETED, OrderStatus.CANCELLED]:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=[
                {"msg": "An order with this ID is already completed or cancelled."}
            ],
        )

    if data.status in [OrderStatus.PLACED, OrderStatus.READY, OrderStatus.COMPLETED]:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=[
                {
                    "msg": "You cannot change the status of an order to PLACED, READY or COMPLETED."
                }
            ],
        )

    return await OrderService.update(order, data)
