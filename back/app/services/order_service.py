from datetime import datetime, timedelta
from uuid import UUID
from typing import List, Optional
from app.models.cafe_model import Cafe
from app.models.order_model import Order, OrderStatus
from app.schemas.order_schema import OrderCreate, OrderUpdate
from bson import SON


class OrderService:
    """
    Service class that provides methods for CRUD operations related to Orders.
    """

    # --------------------------------------
    #               Order
    # --------------------------------------

    @staticmethod
    async def list_orders(**filters) -> List[Order]:
        # Example: http://cafesansfil-api.onrender.com/api/orders?sort_by=-order_number&page=1&limit=10
        query_filters = {}
        page = int(filters.pop("page", 1))
        limit = int(filters.pop("limit", 20))

        # Convert 'is_open' string to boolean
        if "is_open" in filters:
            if filters["is_open"].lower() == "true":
                query_filters["is_open"] = True
            elif filters["is_open"].lower() == "false":
                query_filters["is_open"] = False

        sort_by = filters.pop("sort_by", "-order_number")  # Default sort field
        sort_order = -1 if sort_by.startswith("-") else 1
        sort_field = sort_by[1:] if sort_order == -1 else sort_by
        sort_params = [(sort_field, sort_order)]

        orders_cursor = Order.aggregate(
            [
                {"$match": query_filters},
                {"$sort": dict(sort_params)},
                {"$skip": (page - 1) * limit},
                {"$limit": limit},
            ]
        )

        return await orders_cursor.to_list(None)

    @staticmethod
    async def create_order(data: OrderCreate, username: str) -> Order:
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
    async def retrieve_order(order_id: UUID):
        return await Order.find_one(Order.order_id == order_id)

    @staticmethod
    async def update_order(order_id: UUID, data: OrderUpdate):
        order = await OrderService.retrieve_order(order_id)
        await order.update({"$set": data.model_dump(exclude_unset=True)})
        return order

    @staticmethod
    async def create_many_orders(orders_data: List[OrderCreate], username: str) -> List[Order]:
        """
        Create multiple orders for a user.

        :param orders_data: A list of order data to create.
        :param username: The username of the user creating the orders.
        :return: A list of created Order objects.
        """
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
    async def update_many_orders(order_ids: List[UUID], data: OrderUpdate) -> List[Order]:
        """
        Update multiple orders based on the provided list of UUIDs and data.

        :param order_ids: A list of IDs of the orders to update.
        :param data: The data to update the orders with.
        :return: A list of updated Order objects.
        """
        update_data = data.model_dump(exclude_unset=True)
        if not update_data:
            raise ValueError("No data to update")

        result = await Order.find_many({"order_id": {"$in": order_ids}}).update_many({"$set": update_data})
        if result.matched_count == 0:
            raise ValueError("No orders found for the provided IDs")

        return await Order.find_many({"order_id": {"$in": order_ids}}).to_list()

    @staticmethod
    async def delete_many_orders(order_ids: List[UUID]) -> None:
        """
        Delete multiple orders based on the provided list of UUIDs.

        :param order_ids: A list of IDs of the orders to delete.
        :return: None
        """
        orders_to_delete = await Order.find_many({"order_id": {"$in": order_ids}}).to_list()
        if not orders_to_delete:
            raise ValueError("No orders found for the provided IDs")

        await Order.find_many({"order_id": {"$in": order_ids}}).delete_many()

    @staticmethod
    async def check_and_update_order_status(orders):
        now = datetime.utcnow()
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
    async def list_orders_for_user(username: str, **filters) -> List[Order]:
        query_filters = {}
        query_filters["user_username"] = username
        page = int(filters.pop("page", 1))
        limit = int(filters.pop("limit", 20))

        # Convert 'is_open' string to boolean
        if "is_open" in filters:
            if filters["is_open"].lower() == "true":
                query_filters["is_open"] = True
            elif filters["is_open"].lower() == "false":
                query_filters["is_open"] = False

        sort_by = filters.pop("sort_by", "-order_number")  # Default sort field
        sort_order = -1 if sort_by.startswith("-") else 1
        sort_field = sort_by[1:] if sort_order == -1 else sort_by
        sort_params = [(sort_field, sort_order)]

        orders_cursor = Order.aggregate(
            [
                {"$match": query_filters},
                {"$sort": dict(sort_params)},
                {"$skip": (page - 1) * limit},
                {"$limit": limit},
            ]
        )

        orders = await orders_cursor.to_list(None)
        await OrderService.check_and_update_order_status(orders)
        return orders

    @staticmethod
    async def list_orders_for_cafe(cafe_slug: str, **filters) -> List[Order]:
        query_filters = {}

        cafe = await Cafe.find_one({"slug": cafe_slug})
        if not cafe:
            return None
        slug_list = [cafe.slug] + getattr(cafe, "previous_slugs", [])

        query_filters["cafe_slug"] = {"$in": slug_list}
        page = int(filters.pop("page", 1))
        limit = int(filters.pop("limit", 20))

        # Convert 'is_open' string to boolean
        if "is_open" in filters:
            if filters["is_open"].lower() == "true":
                query_filters["is_open"] = True
            elif filters["is_open"].lower() == "false":
                query_filters["is_open"] = False

        sort_by = filters.pop("sort_by", "-order_number")  # Default sort field
        sort_order = -1 if sort_by.startswith("-") else 1
        sort_field = sort_by[1:] if sort_order == -1 else sort_by
        sort_params = [(sort_field, sort_order)]

        orders_cursor = Order.aggregate(
            [
                {"$match": query_filters},
                {"$sort": dict(sort_params)},
                {"$skip": (page - 1) * limit},
                {"$limit": limit},
            ]
        )

        orders = await orders_cursor.to_list(None)
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
        cafe_slug: str,
        start_date_str: Optional[str],
        end_date_str: Optional[str],
        report_type: str = "daily",
    ):
        def decimal128_to_float(value):
            return float(str(value)) if value is not None else 0.0

        # Convert date strings to datetime objects
        start_date = (
            datetime.strptime(start_date_str, "%Y-%m-%d") if start_date_str else None
        )
        end_date = datetime.strptime(end_date_str, "%Y-%m-%d") if end_date_str else None

        cafe = await Cafe.find_one({"slug": cafe_slug})
        if not cafe:
            return None
        slug_list = [cafe.slug] + getattr(cafe, "previous_slugs", [])

        query = {"cafe_slug": {"$in": slug_list}, "status": "Complétée"}
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
