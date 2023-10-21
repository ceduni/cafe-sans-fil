from uuid import UUID
from typing import List
from app.models.order_model import Order as OrderModel
from app.schemas.order_schema import Order

class OrderService:
    """
    Service class that provides methods for CRUD operations related to Orders.
    """
    
    # --------------------------------------
    #               Order
    # --------------------------------------

    @staticmethod
    async def create_order(data: Order) -> OrderModel:
        order = OrderModel(**data.dict())
        await order.insert()
        return order

    @staticmethod
    async def retrieve_order(order_id: UUID) -> OrderModel:
        return await OrderModel.find_one(OrderModel.order_id == order_id)

    @staticmethod
    async def update_order(order_id: UUID, data: Order) -> OrderModel:
        order = await OrderService.retrieve_order(order_id)
        await order.update({"$set": data.dict(exclude_unset=True)})
        return order

    @staticmethod
    async def list_orders_for_user(user_id: UUID, status: str = None) -> List[OrderModel]:
        filter_query = {"user_id": user_id}
        if status:
            filter_query["status"] = status
        return await OrderModel.find(filter_query).to_list()

    @staticmethod
    async def list_orders_for_cafe(cafe_id: UUID, status: str = None) -> List[OrderModel]:
        filter_query = {"cafe_id": cafe_id}
        if status:
            filter_query["status"] = status
        return await OrderModel.find(filter_query).to_list()