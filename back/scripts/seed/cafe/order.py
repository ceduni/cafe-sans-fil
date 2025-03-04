"""
Order seeder module.
"""

import random
from datetime import UTC, datetime, timedelta
from typing import List

from tqdm import tqdm

from app.cafe.menu.item.models import MenuItem
from app.cafe.menu.item.service import ItemService
from app.cafe.models import Cafe
from app.cafe.order.models import Order, OrderedItem, OrderStatus
from app.cafe.service import CafeService
from app.user.models import User
from app.user.service import UserService

random.seed(42)


class OrderSeeder:
    """Order seeder class."""

    def __init__(self) -> None:
        """Initialize the OrderSeeder."""
        self.orders: List[Order] = []
        self.order_number: int = 1

    async def seed_orders(self, num_orders_per_cafe: int = 50) -> None:
        """Seed orders for all cafes."""
        cafes: List[Cafe] = await CafeService.get_all()
        users: List[User] = await UserService.get_all()

        for cafe in tqdm(cafes, desc="Orders"):
            # Get cafe-specific data
            menu_items: List[MenuItem] = await ItemService.get_all(cafe.id)
            if not menu_items:
                continue

            for _ in range(num_orders_per_cafe):
                user: User = random.choice(users)
                order: Order = await self._create_order(
                    cafe=cafe,
                    user=user,
                    menu_items=menu_items,
                    order_number=self.order_number,
                )
                self.orders.append(order)
                self.order_number += 1

        await Order.insert_many(self.orders)

    async def _create_order(
        self,
        cafe: Cafe,
        user: User,
        menu_items: List[MenuItem],
        order_number: int,
    ) -> Order:
        """Create a single order instance."""
        num_items: int = random.randint(1, 5)
        selected_items: List[MenuItem] = random.sample(menu_items, num_items)

        order = Order(
            user_id=user.id,
            cafe_id=cafe.id,
            cafe_name=cafe.name,
            order_number=(order_number % 1000),
            items=[
                OrderedItem(
                    _id=item.id,
                    name=item.name,
                    price=item.price,
                    quantity=random.randint(1, 3),
                    options=item.options if random.random() < 0.5 else [],
                )
                for item in selected_items
            ],
            status=self._random_status(),
            created_at=self._random_date(),
        )

        order.calculate_total_price()
        order.updated_at = order.created_at + timedelta(minutes=random.randint(1, 60))
        return order

    def _random_status(self) -> OrderStatus:
        """Generate a random order status."""
        return random.choice(
            [
                OrderStatus.PLACED,
                OrderStatus.READY,
                OrderStatus.COMPLETED,
                OrderStatus.CANCELLED,
            ]
        )

    def _random_date(self) -> datetime:
        """Generate a random date within the last 30 days."""
        return datetime.now(UTC) - timedelta(days=random.randint(0, 30))
