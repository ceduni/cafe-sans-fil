"""
Module for handling order-related operations.
"""

from datetime import UTC, datetime, timedelta
from typing import List, Optional

from beanie import PydanticObjectId
from bson import SON

from app.cafe.models import Cafe
from app.order.models import Order, OrderCreate, OrderStatus, OrderUpdate


class OrderService:
    """
    Service class that provides methods for CRUD operations related to Orders.
    """

    # --------------------------------------
    #               Order
    # --------------------------------------

    @staticmethod
    async def get_orders(**filters: dict):
        """Get orders."""
        sort_by = filters.pop("sort_by", "-order_number")
        return Order.find(filters).sort(sort_by)

    @staticmethod
    async def create_order(data: OrderCreate, username: str) -> Order:
        """Create a new order for a user."""
        order_data = data.model_dump()
        order_data["user_username"] = username
        order_data["order_number"] = await OrderService.get_next_order_number()
        order = Order(**order_data)
        await order.insert()
        return order

    @staticmethod
    async def create_order_test(
        data: OrderCreate,
        username: str,
        created_at: datetime = None,
        updated_at: datetime = None,
        status: str = "Placée",
    ) -> Order:
        """Create a new order for a user."""
        order_data = data.model_dump()
        order_data["user_username"] = username
        order_data["order_number"] = await OrderService.get_next_order_number()
        order_data["created_at"] = created_at  # For Test
        order_data["updated_at"] = updated_at  # For Test
        order_data["status"] = status  # For Test
        order = Order(**order_data)
        await order.insert()
        return order

    @staticmethod
    async def get_order(order_id: PydanticObjectId):
        """Get an order by its ID."""
        return await Order.find_one(Order.id == order_id)

    @staticmethod
    async def update_order(order_id: PydanticObjectId, data: OrderUpdate):
        """Update an order by its ID."""
        order = await OrderService.get_order(order_id)
        await order.update({"$set": data.model_dump(exclude_unset=True)})
        return order

    @staticmethod
    async def create_many_orders(
        orders_data: List[OrderCreate], username: str
    ) -> List[Order]:
        """Create multiple orders for a user."""
        orders = []
        for data in orders_data:
            order_data = data.model_dump()
            order_data["user_username"] = username
            order_data["order_number"] = await OrderService.get_next_order_number()
            order = Order(**order_data)
            orders.append(order)

        await Order.insert_many(orders)
        return orders

    @staticmethod
    async def update_many_orders(
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
            raise ValueError("No orders found for the provided IDs")

        return await Order.find_many({"order_id": {"$in": order_ids}}).to_list()

    @staticmethod
    async def delete_many_orders(order_ids: List[PydanticObjectId]) -> None:
        """Delete multiple orders."""
        orders_to_delete = await Order.find_many(
            {"order_id": {"$in": order_ids}}
        ).to_list()
        if not orders_to_delete:
            raise ValueError("No orders found for the provided IDs")

        await Order.find_many({"order_id": {"$in": order_ids}}).delete_many()

    @staticmethod
    async def check_and_update_order_status(orders):
        """Check and update the status of orders."""
        now = datetime.now(UTC)
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
    async def get_orders_for_user(username: str, **filters: dict):
        """Get orders for a user."""
        sort_by = filters.pop("sort_by", "-order_number")
        filters["user_username"] = username
        orders = Order.find(filters).sort(sort_by)
        await OrderService.check_and_update_order_status(orders)
        return orders

    @staticmethod
    async def get_orders_for_cafe(cafe_slug: str, **filters: dict):
        """Get orders for a cafe."""
        cafe = await Cafe.find_one(Cafe.slug == cafe_slug)
        if not cafe:
            return None

        sort_by = filters.pop("sort_by", "-order_number")
        filters["cafe_slug"] = cafe_slug
        orders = Order.find(filters).sort(sort_by)
        await OrderService.check_and_update_order_status(orders)
        return orders

    @staticmethod
    async def get_next_order_number():
        highest_order = await Order.aggregate(
            [{"$sort": {"order_number": -1}}, {"$limit": 1}]
        ).to_list(None)
        if highest_order:
            return (highest_order[0]["order_number"]) + 1
        else:
            return 1

    # --------------------------------------
    #              Sales Report
    # --------------------------------------

    @staticmethod
    async def generate_sales_report_data(
        cafe_id: PydanticObjectId,
        start_date_str: Optional[str],
        end_date_str: Optional[str],
        report_type: str = "daily",
    ):
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
