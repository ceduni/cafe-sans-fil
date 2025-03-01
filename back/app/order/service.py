"""
Module for handling order-related operations.
"""

from datetime import UTC, datetime, timedelta
from typing import List, Optional

from beanie import PydanticObjectId
from bson import SON

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
        user_id: Optional[str] = None, cafe_id: Optional[str] = None, **filters: dict
    ):
        """Get orders."""
        if user_id is not None:
            filters["user_id"] = PydanticObjectId(user_id)
        if cafe_id is not None:
            filters["cafe_id"] = PydanticObjectId(cafe_id)

        sort_by = filters.pop("sort_by", "-order_number")
        findmany = Order.find(filters).sort(sort_by)
        # result = await Order.find(filters).sort(sort_by)
        # await OrderService.check_and_update_order_status(result)
        return findmany

    @staticmethod
    async def get(id: PydanticObjectId):
        """Get an order by its ID."""
        return await Order.get(id)

    @staticmethod
    async def create(
        user: User,
        cafe: Cafe,
        items: list[MenuItem],
        data: OrderCreate,
    ) -> Order:
        """Create a new order."""
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
    async def create_many(
        datas: List[OrderCreate], user_id: PydanticObjectId
    ) -> List[Order]:
        """Create multiple orders for a user."""
        orders = []
        for data in datas:
            order_data = data.model_dump()
            order_data["user_id"] = user_id
            order_data["order_number"] = await OrderService.get_next_order_number()
            order = Order(**order_data)
            orders.append(order)

        await Order.insert_many(orders)
        return orders

    @staticmethod
    async def update_many(
        order_ids: List[PydanticObjectId], data: OrderUpdate
    ) -> List[Order]:
        """Update multiple orders."""
        update_data = data.model_dump(exclude_unset=True)
        if not update_data:
            raise ValueError("No data to update")

        result = await Order.find_many({"order_id": {"$in": order_ids}}).update_many(
            {"$set": update_data}
        )
        if result.matched_count == 0:
            raise None

        return await Order.find_many({"order_id": {"$in": order_ids}}).to_list()

    @staticmethod
    async def delete_many(order_ids: List[PydanticObjectId]) -> None:
        """Delete multiple orders."""
        orders_to_delete = await Order.find_many(
            {"order_id": {"$in": order_ids}}
        ).to_list()
        if not orders_to_delete:
            raise None

        await Order.find_many({"order_id": {"$in": order_ids}}).delete_many()

    @staticmethod
    async def check_and_update_order_status(orders) -> None:
        """Check and update the status of orders."""
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

    @staticmethod
    async def generate_sales_report_data(
        cafe_id: PydanticObjectId,
        start_date_str: Optional[str],
        end_date_str: Optional[str],
        report_type: str = "daily",
    ) -> dict:
        """Generate sales report data for a cafe."""

        def decimal128_to_float(value):
            return float(str(value)) if value is not None else 0.0

        # Convert date strings to datetime objects
        start_date = (
            datetime.strptime(start_date_str, "%Y-%m-%d") if start_date_str else None
        )
        end_date = datetime.strptime(end_date_str, "%Y-%m-%d") if end_date_str else None

        query = {"cafe_id": cafe_id, "status": "Complétée"}
        if start_date:
            query["created_at"] = query.get("created_at", {})
            query["created_at"]["$gte"] = start_date
        if end_date:
            query["created_at"] = query.get("created_at", {})
            query["created_at"]["$lte"] = end_date

        total_revenue = await Order.find(query).sum("total_price")
        total_revenue = decimal128_to_float(total_revenue)

        total_orders = await Order.find(query).count()

        item_sales_aggregation = [
            {"$match": query},
            {"$unwind": "$items"},
            {
                "$group": {
                    "_id": "$items.item_name",
                    "item_quantity_sold": {"$sum": "$items.quantity"},
                    "item_revenue": {
                        "$sum": {"$multiply": ["$items.quantity", "$items.item_price"]}
                    },
                }
            },
            {"$sort": {"item_quantity_sold": -1}},
        ]
        item_sales_details = await Order.aggregate(item_sales_aggregation).to_list()

        date_group_format = "%Y-%m-%d"
        if report_type == "weekly":
            date_group_format = "%Y-%U"
        elif report_type == "monthly":
            date_group_format = "%Y-%m"

        item_sales_details = [
            {
                "item_name": data["_id"],
                "item_quantity_sold": data["item_quantity_sold"],
                "item_revenue": decimal128_to_float(data["item_revenue"]),
            }
            for data in item_sales_details
        ]

        sales_order_trends_aggregation = [
            {"$match": query},
            {
                "$group": {
                    "_id": {
                        "$dateToString": {
                            "format": date_group_format,
                            "date": "$created_at",
                        }
                    },
                    "order_count": {"$sum": 1},
                }
            },
            {"$sort": SON([("_id", 1)])},
            {"$project": {"time_period": "$_id", "_id": 0, "order_count": 1}},
        ]
        sales_order_trends = await Order.aggregate(
            sales_order_trends_aggregation
        ).to_list()

        sales_revenue_trends_aggregation = [
            {"$match": query},
            {
                "$group": {
                    "_id": {
                        "$dateToString": {
                            "format": date_group_format,
                            "date": "$created_at",
                        }
                    },
                    "total_revenue": {"$sum": "$total_price"},
                }
            },
            {"$sort": SON([("_id", 1)])},
            {"$project": {"time_period": "$_id", "_id": 0, "total_revenue": 1}},
        ]
        sales_revenue_trends = await Order.aggregate(
            sales_revenue_trends_aggregation
        ).to_list()
        sales_revenue_trends = [
            {
                "time_period": data["time_period"],
                "total_revenue": decimal128_to_float(data["total_revenue"]),
            }
            for data in sales_revenue_trends
        ]

        return {
            "total_revenue": total_revenue,
            "total_orders": total_orders,
            "sales_revenue_trends": sales_revenue_trends,
            "sales_order_trends": sales_order_trends,
            "item_sales_details": item_sales_details,
        }
