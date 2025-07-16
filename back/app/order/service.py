"""
Module for handling order-related operations.
"""

from datetime import UTC, datetime, timedelta
from typing import List, Optional, Union

from beanie import PydanticObjectId
from beanie.odm.queries.find import FindMany

from app.menu.item.models import MenuItem
from app.cafe.models import Cafe
from app.order.models import (
    Order,
    OrderCreate,
    OrderedItem,
    OrderStatus,
    OrderUpdate,
)
from app.user.models import User


class OrderService:
    """
    Service class that provides methods for CRUD operations related to Orders.
    """

    @staticmethod
    async def get_all(
        user_id: Optional[str] = None,
        cafe_id: Optional[str] = None,
        to_list: bool = True,
        **filters: dict
    ) -> Union[FindMany[Order], List[Order]]:
        """Get orders."""
        if user_id is not None:
            filters["user_id"] = PydanticObjectId(user_id)
        if cafe_id is not None:
            filters["cafe_id"] = PydanticObjectId(cafe_id)

        sort_by = filters.pop("sort_by", "-order_number")
        query = Order.find(filters).sort(sort_by)
        orders = await query.to_list()

        await OrderService._update_expired_orders(orders)
        return await orders if to_list else query

    @staticmethod
    async def get(id: PydanticObjectId) -> Order:
        """Get an order by its ID."""
        return await Order.get(id)

    @staticmethod
    async def create(
        user: User,
        cafe: Cafe,
        items: list[MenuItem],
        data: OrderCreate,
    ) -> Order:
        """Create a order."""
        item_map = {item.id: item for item in items}
        ordered_items = []
        for item_create in data.items:
            menu_item = item_map[item_create.item_id]
            ordered_items.append(
                OrderedItem(
                    _id=menu_item.id,
                    name=menu_item.name,
                    price=menu_item.price,
                    quantity=item_create.quantity,
                    options=item_create.options,
                )
            )

        order_number = await OrderService.get_next_order_number()

        order = Order(
            **data.model_dump(exclude={"items"}),
            user_id=user.id,
            cafe_id=cafe.id,
            cafe_name=cafe.name,
            order_number=order_number,
            items=ordered_items
        )

        await order.insert()
        return order

    @staticmethod
    async def update(order: Order, data: OrderUpdate) -> Order:
        """Update an order by its ID."""
        order.status = data.status
        await order.save()
        return order

    @staticmethod
    async def _update_expired_orders(orders: List[Order]) -> None:
        """Update status expired orders PLACED/READY."""
        now = datetime.now(UTC).replace(tzinfo=None)
        expired_order_ids: List[PydanticObjectId] = []

        for order in orders:
            if order.status in [OrderStatus.PLACED, OrderStatus.READY]:
                if order.created_at < now - timedelta(hours=1):
                    expired_order_ids.append(order.id)

        if expired_order_ids:
            await Order.find({"_id": {"$in": expired_order_ids}}).update_many(
                {
                    "$set": {
                        "status": OrderStatus.CANCELLED,
                        "updated_at": order.created_at + timedelta(hours=1),
                    }
                }
            )

    @staticmethod
    async def get_next_order_number(cafe_id: PydanticObjectId = None) -> int:
        """Get the next available order number for a cafe."""
        last_order = (
            await Order.find(
                # Order.cafe_id == cafe_id
            )
            .sort("-order_number")
            .first_or_none()
        )

        if last_order and last_order.order_number:
            return last_order.order_number + 1
        return 1  # First order
