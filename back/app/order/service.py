"""
Module for handling order-related operations.
"""

from datetime import UTC, datetime, timedelta
from typing import List, Optional, Union

from beanie import PydanticObjectId
from beanie.odm.queries.find import FindMany

from app.cafe.menu.item.models import MenuItem
from app.cafe.models import Cafe
from app.order.models import Order, OrderCreate, OrderedItem, OrderStatus, OrderUpdate
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
        # result = await Order.find(filters).sort(sort_by)
        # await OrderService.update_status(result)
        return await query.to_list() if to_list else query

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
                    item_id=menu_item.id,
                    item_name=menu_item.name,
                    item_price=menu_item.price,
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
    async def update_status(orders) -> None:
        """Update the status of orders."""
        now = datetime.now(UTC).replace(tzinfo=None)
        for order_dict in orders:
            order = Order(**order_dict)
            if (
                order.status in [OrderStatus.PLACED, OrderStatus.READY]
                and order.created_at + timedelta(hours=1) < now
            ):
                order.status = OrderStatus.CANCELLED
                order.updated_at = order.created_at + timedelta(hours=1)
                await order.save()

    @staticmethod
    async def get_next_order_number() -> int:
        """Get the next available order number."""
        highest_order = await Order.aggregate(
            [{"$sort": {"order_number": -1}}, {"$limit": 1}]
        ).to_list(None)
        if highest_order:
            return (highest_order[0]["order_number"]) + 1
        else:
            return 1
