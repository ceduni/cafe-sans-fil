from fastapi import APIRouter, HTTPException, Path, status, Request, Depends
from app.schemas.order_schema import OrderCreate, OrderUpdate, OrderOut
from app.services.order_service import OrderService
from uuid import UUID
from typing import List
from app.models.user_model import User
from app.models.cafe_model import Role
from app.api.deps.user_deps import get_current_user
from app.services.cafe_service import CafeService

"""
This module defines the API routes related to the ordering system of the application.
"""

order_router = APIRouter()

# --------------------------------------
#               Order
# --------------------------------------

@order_router.get("/orders", response_model=List[OrderOut], summary="List Orders", description="Retrieve a list of all orders.")
async def list_orders(request: Request, current_user: User = Depends(get_current_user)):
    filters = dict(request.query_params)
    return await OrderService.list_orders(**filters)

@order_router.get("/orders/{order_id}", response_model=OrderOut, summary="Get Order", description="Retrieve detailed information about a specific order.")
async def get_order(order_id: UUID = Path(..., description="The unique identifier of the order"), current_user: User = Depends(get_current_user)):
    try:
        order = await OrderService.retrieve_order(order_id)
        if not order:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Order not found"
            )

        # Authorization check
        if order.user_username != current_user.username and not await CafeService.is_authorized_for_cafe_action_by_slug(order.cafe_slug, current_user, [Role.ADMIN, Role.VOLUNTEER]):
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Access forbidden"
            )

        return order
    except ValueError as e:
        if str(e) == "Cafe not found":
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=str(e)
            )
        elif str(e) == "Access forbidden":
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=str(e)
            )

@order_router.post("/orders", response_model=OrderOut, summary="Create Order", description="Create a new order with the provided details.")
async def create_order(order: OrderCreate, current_user: User = Depends(get_current_user)):
    cafe = await CafeService.retrieve_cafe(order.cafe_slug)
    if not cafe:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Cafe not found"
        )
    return await OrderService.create_order(order, current_user.username)

@order_router.put("/orders/{order_id}", response_model=OrderOut, summary="Update Order", description="Update the details of an existing order.")
async def update_order(orderUpdate: OrderUpdate, order_id: UUID = Path(..., description="The unique identifier of the order to update"), current_user: User = Depends(get_current_user)):
    try:
        order = await OrderService.retrieve_order(order_id)
        if not order:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, 
                detail="Order not found"
            )

        # Authorization check
        if order.user_username != current_user.username and not await CafeService.is_authorized_for_cafe_action_by_slug(order.cafe_slug, current_user, [Role.ADMIN, Role.VOLUNTEER]):
            raise HTTPException(status_code=403, detail="Access forbidden")

        return await OrderService.update_order(order_id, orderUpdate)
    except ValueError as e:
        if str(e) == "Cafe not found":
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=str(e)
            )
        elif str(e) == "Access forbidden":
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=str(e)
            )

@order_router.get("/users/{username}/orders", response_model=List[OrderOut], summary="List User Orders", description="Retrieve a list of orders for a specific user.")
async def list_user_orders(request: Request, username: str = Path(..., description="The username of the user"), current_user: User = Depends(get_current_user)):
    # Authorization check
    if username != current_user.username:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Access forbidden"
        )
    filters = dict(request.query_params)
    return await OrderService.list_orders_for_user(username, **filters)

@order_router.get("/cafes/{cafe_slug}/orders", response_model=List[OrderOut], summary="List Cafe Orders", description="Retrieve a list of orders for a specific cafe.")
async def list_cafe_orders(request: Request, cafe_slug: str = Path(..., description="The slug of the cafe"), current_user: User = Depends(get_current_user)):
    try:
        # Authorization check
        if not await CafeService.is_authorized_for_cafe_action_by_slug(cafe_slug, current_user, [Role.ADMIN, Role.VOLUNTEER]):
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Access forbidden"
            )

        filters = dict(request.query_params)
        return await OrderService.list_orders_for_cafe(cafe_slug, **filters)
    except ValueError as e:
        if str(e) == "Cafe not found":
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=str(e)
            )
        elif str(e) == "Access forbidden":
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=str(e)
            )
