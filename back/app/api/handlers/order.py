from fastapi import APIRouter, HTTPException, Depends, Query
from app.schemas.order_schema import Order
from app.services.order_service import OrderService
from uuid import UUID

"""
This module defines the API routes related to the ordering system of the application.
"""

order_router = APIRouter()

# --------------------------------------
#               Order
# --------------------------------------

@order_router.get("/orders/{order_id}", response_model=Order)
async def get_order(order_id: UUID):
    order = await OrderService.retrieve_order(order_id)
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")
    return order

@order_router.post("/orders", response_model=Order)
async def create_order(order: Order):
    return await OrderService.create_order(order)

@order_router.put("/orders/{order_id}", response_model=Order)
async def update_order(order_id: UUID, order: Order):
    return await OrderService.update_order(order_id, order)

@order_router.get("/users/{user_id}/orders")
async def list_user_orders(user_id: UUID, status: str = Query(None, description="Filter orders by status")):
    return await OrderService.list_orders_for_user(user_id, status)

@order_router.get("/cafes/{cafe_id}/orders")
async def list_cafe_orders(cafe_id: UUID, status: str = Query(None, description="Filter orders by status")):
    return await OrderService.list_orders_for_cafe(cafe_id, status)
