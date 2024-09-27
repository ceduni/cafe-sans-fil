# scripts/db_seed/order_seeder.py

from app.services.order_service import OrderService
from app.schemas.order_schema import OrderCreate
from faker import Faker

fake = Faker()

class OrderSeeder:
    async def seed_orders(self, cafe_slugs, usernames, num_orders: int):
        """
        Seeds a specified number of orders for cafes.
        """
        order_data = []
        for _ in range(num_orders):
            order_data.append(
                OrderCreate(
                    cafe_slug=fake.random_element(elements=cafe_slugs),
                    user_username=fake.random_element(elements=usernames),
                    items=[fake.word() for _ in range(3)],  # Random items
                    status="PLACED",
                )
            )
        await OrderService.create_many_orders(order_data, username=fake.random_element(usernames))
        print(f"{num_orders} orders created")
