from uuid import UUID
from typing import List
from app.models.order_model import Order
from app.schemas.order_schema import OrderCreate, OrderUpdate

class OrderService:
    """
    Service class that provides methods for CRUD operations related to Orders.
    """
    
    # --------------------------------------
    #               Order
    # --------------------------------------

    @staticmethod
    async def list_orders(**filters) -> List[Order]:
        sort = filters.pop('sort', None)
        limit = int(filters.pop('limit', 20))
        page = int(filters.pop('page', 1))
        skip = (page - 1) * limit

        if sort:
            return await Order.find(filters).skip(skip).limit(limit).sort(sort).to_list()
        else:
            return await Order.find(filters).skip(skip).limit(limit).to_list()
        
    @staticmethod
    async def create_order(data: OrderCreate, user_id: UUID) -> Order:
        order_data = data.model_dump()
        order_data['user_id'] = user_id
        order = Order(**order_data)
        await order.insert()
        return order

    @staticmethod
    async def retrieve_order(order_id: UUID):
        return await Order.find_one(Order.order_id == order_id)

    @staticmethod
    async def update_order(order_id: UUID, data: OrderUpdate):
        order = await OrderService.retrieve_order(order_id)
        await order.update({"$set": data.model_dump(exclude_unset=True)})
        return order

    @staticmethod
    async def list_orders_for_user(user_id: UUID, **filters) -> List[Order]:
        filters["user_id"] = user_id
        sort = filters.pop('sort', None)
        limit = int(filters.pop('limit', 20))
        page = int(filters.pop('page', 1))
        skip = (page - 1) * limit

        if sort:
            return await Order.find(filters).skip(skip).limit(limit).sort(sort).to_list()
        else:
            return await Order.find(filters).skip(skip).limit(limit).to_list()

    @staticmethod
    async def list_orders_for_cafe(cafe_id: UUID, **filters) -> List[Order]:
        filters["cafe_id"] = cafe_id
        sort = filters.pop('sort', None)
        limit = int(filters.pop('limit', 20))
        page = int(filters.pop('page', 1))
        skip = (page - 1) * limit

        if sort:
            return await Order.find(filters).skip(skip).limit(limit).sort(sort).to_list()
        else:
            return await Order.find(filters).skip(skip).limit(limit).to_list()