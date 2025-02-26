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
        datas = []
        for _ in range(num_orders):
            datas.append(
                OrderCreate(
                    cafe_slug=fake.random_element(elements=cafe_slugs),
                    user_username=fake.random_element(elements=usernames),
                    items=[fake.word() for _ in range(3)],  # Random items
                    status="PLACED",
                )
            )
        await OrderService.create_many(datas, username=fake.random_element(usernames))
        print(f"{num_orders} orders created")
