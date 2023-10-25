from fastapi import APIRouter, HTTPException, Query, Depends
from app.schemas.order_schema import OrderCreate, OrderUpdate, OrderOut
from app.services.order_service import OrderService
from uuid import UUID
from typing import List
from app.models.user_model import User
from app.api.deps.user_deps import get_current_user
from app.services.cafe_service import CafeService
from app.schemas.cafe_schema import Role
"""
This module defines the API routes related to the ordering system of the application.
"""

order_router = APIRouter()

# --------------------------------------
#               Order
# --------------------------------------

@order_router.get("/orders", response_model=List[OrderOut])
async def list_orders(current_user: User = Depends(get_current_user)):
    return await OrderService.list_orders()

@order_router.get("/orders/{order_id}", response_model=OrderOut)
async def get_order(order_id: UUID, current_user: User = Depends(get_current_user)):
    # Authorization check
    order = await OrderService.retrieve_order(order_id)
    if order.user_id != current_user.user_id and not await CafeService.is_authorized_for_cafe_action(order.cafe_id, current_user, [Role.ADMIN, Role.VOLUNTEER]):
        raise HTTPException(status_code=403, detail="Access forbidden")
    
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")
    
    return order

@order_router.post("/orders", response_model=OrderOut)
async def create_order(order: OrderCreate, current_user: User = Depends(get_current_user)):
    return await OrderService.create_order(order)

@order_router.put("/orders/{order_id}", response_model=OrderOut)
async def update_order(order_id: UUID, orderUpdate: OrderUpdate, current_user: User = Depends(get_current_user)):
    # Authorization check
    order = await OrderService.retrieve_order(order_id)
    print(order.user_id != current_user.user_id)
    if order.user_id != current_user.user_id and not await CafeService.is_authorized_for_cafe_action(order.cafe_id, current_user, [Role.ADMIN, Role.VOLUNTEER]):
        raise HTTPException(status_code=403, detail="Access forbidden")
    
    return await OrderService.update_order(order_id, orderUpdate)

@order_router.get("/users/{user_id}/orders", response_model=List[OrderOut])
async def list_user_orders(user_id: UUID, status: str = Query(None, description="Filter orders by status"), current_user: User = Depends(get_current_user)):
    # Authorization check
    if user_id != current_user.user_id:
        raise HTTPException(status_code=403, detail="Access forbidden")

    return await OrderService.list_orders_for_user(user_id, status)

@order_router.get("/cafes/{cafe_id}/orders", response_model=List[OrderOut])
async def list_cafe_orders(cafe_id: UUID, status: str = Query(None, description="Filter orders by status"), current_user: User = Depends(get_current_user)):
    # Authorization check
    if not await CafeService.is_authorized_for_cafe_action(cafe_id, current_user, [Role.ADMIN, Role.VOLUNTEER]):
        raise HTTPException(status_code=403, detail="Access forbidden")
    
    return await OrderService.list_orders_for_cafe(cafe_id, status)
