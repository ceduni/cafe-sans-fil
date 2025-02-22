"""
Order seeder module.
"""

from faker import Faker

from app.order.models import OrderCreate
from app.order.service import OrderService

# random.seed(42)
Faker.seed(42)
fake = Faker("fr_FR")


class OrderSeeder:
    async def seed_orders(self, cafe_slugs, usernames, num_orders: int):
        """Seeds a specified number of orders."""
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
        await OrderService.create_many_orders(
            order_data, username=fake.random_element(usernames)
        )
        print(f"{num_orders} orders created")
