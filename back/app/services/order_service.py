from uuid import UUID
from app.models.order_model import Order as OrderModel
from app.schemas.order_schema import Order

class OrderService:

    # @staticmethod
    # async def list_orders(user_id: UUID) -> List[Order]:
    #     return await OrderModel.find(OrderModel.user_id == user_id).to_list()

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

    # @staticmethod
    # async def delete_order(order_id: UUID) -> None:
    #     order = await OrderService.retrieve_order(order_id)
    #     if order:
    #         await order.delete()
