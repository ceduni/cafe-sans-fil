import datetime
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
        # Example: http://cafesansfil-api.onrender.com/api/orders?sort_by=-order_number&page=1&limit=10
        query_filters = {}
        page = int(filters.pop('page', 1))
        limit = int(filters.pop('limit', 20))

        # Convert 'is_open' string to boolean
        if 'is_open' in filters:
            if filters['is_open'].lower() == 'true':
                query_filters['is_open'] = True
            elif filters['is_open'].lower() == 'false':
                query_filters['is_open'] = False


        sort_by = filters.pop('sort_by', '-order_number')  # Default sort field
        sort_order = -1 if sort_by.startswith('-') else 1
        sort_field = sort_by[1:] if sort_order == -1 else sort_by
        sort_params = [(sort_field, sort_order)]

        orders_cursor = Order.aggregate([
            {"$match": query_filters},
            {"$sort": dict(sort_params)},
            {"$skip": (page - 1) * limit},
            {"$limit": limit}
        ])

        return await orders_cursor.to_list(None)
        
    @staticmethod
    async def create_order(data: OrderCreate, username: str) -> Order:
        order_data = data.model_dump()
        order_data['user_username'] = username
        order_data['order_number'] = await OrderService.get_next_order_number()
        order = Order(**order_data)
        await order.insert()
        return order
    
    @staticmethod
    async def create_order_test(data: OrderCreate, username: str, created_at: datetime = None, updated_at: datetime = None, status: str = "Placée") -> Order:
        order_data = data.model_dump()
        order_data['user_username'] = username
        order_data['order_number'] = await OrderService.get_next_order_number()
        order_data['created_at'] = created_at # For Test
        order_data['updated_at'] = updated_at # For Test
        order_data['status'] = status # For Test
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
    async def list_orders_for_user(username: str, **filters) -> List[Order]:
        query_filters = {}
        query_filters["user_username"] = username
        page = int(filters.pop('page', 1))
        limit = int(filters.pop('limit', 20))

        # Convert 'is_open' string to boolean
        if 'is_open' in filters:
            if filters['is_open'].lower() == 'true':
                query_filters['is_open'] = True
            elif filters['is_open'].lower() == 'false':
                query_filters['is_open'] = False


        sort_by = filters.pop('sort_by', '-order_number')  # Default sort field
        sort_order = -1 if sort_by.startswith('-') else 1
        sort_field = sort_by[1:] if sort_order == -1 else sort_by
        sort_params = [(sort_field, sort_order)]

        orders_cursor = Order.aggregate([
            {"$match": query_filters},
            {"$sort": dict(sort_params)},
            {"$skip": (page - 1) * limit},
            {"$limit": limit}
        ])

        return await orders_cursor.to_list(None)

    @staticmethod
    async def list_orders_for_cafe(cafe_slug: str, **filters) -> List[Order]:
        query_filters = {}
        query_filters["cafe_slug"] = cafe_slug
        page = int(filters.pop('page', 1))
        limit = int(filters.pop('limit', 20))

        # Convert 'is_open' string to boolean
        if 'is_open' in filters:
            if filters['is_open'].lower() == 'true':
                query_filters['is_open'] = True
            elif filters['is_open'].lower() == 'false':
                query_filters['is_open'] = False


        sort_by = filters.pop('sort_by', '-order_number')  # Default sort field
        sort_order = -1 if sort_by.startswith('-') else 1
        sort_field = sort_by[1:] if sort_order == -1 else sort_by
        sort_params = [(sort_field, sort_order)]

        orders_cursor = Order.aggregate([
            {"$match": query_filters},
            {"$sort": dict(sort_params)},
            {"$skip": (page - 1) * limit},
            {"$limit": limit}
        ])

        return await orders_cursor.to_list(None)

        
    @staticmethod
    async def get_next_order_number():
        highest_order = await Order.aggregate([
            {"$sort": {"order_number": -1}},
            {"$limit": 1}
        ]).to_list(None)
        if highest_order:
            return (highest_order[0]["order_number"]) + 1
        else:
            return 1