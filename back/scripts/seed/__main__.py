"""
Script to seed the database.
"""

import asyncio

from beanie import init_beanie
from motor.motor_asyncio import AsyncIOMotorClient

from app.cafe.announcement.models import Announcement
from app.cafe.event.models import Event
from app.cafe.menu.item.models import MenuItem
from app.cafe.models import Cafe
from app.cafe.order.models import Order
from app.config import settings
from app.interaction.models import Interaction
from app.user.models import User
from scripts.seed.cafe.announcement import AnnouncementSeeder
from scripts.seed.cafe.event import EventSeeder
from scripts.seed.interaction import InteractionSeeder

from .cafe import CafeSeeder
from .cafe.menu import MenuSeeder
from .cafe.order import OrderSeeder
from .cafe.staff import StaffSeeder
from .user import UserSeeder

MONGO_DB_NAME = settings.MONGO_DB_NAME
print(f"Seeding data for {MONGO_DB_NAME}")


async def main():
    """Main function to seed the database."""
    db_client = AsyncIOMotorClient(settings.MONGO_CONNECTION_STRING)
    db_client.drop_database(MONGO_DB_NAME)

    db_client = AsyncIOMotorClient(settings.MONGO_CONNECTION_STRING)[MONGO_DB_NAME]
    await init_beanie(
        database=db_client,
        document_models=[Cafe, MenuItem, Announcement, Event, User, Order, Interaction],
    )

    user_seeder = UserSeeder()
    cafe_seeder = CafeSeeder()
    staff_seeder = StaffSeeder()
    menu_seeder = MenuSeeder()
    order_seeder = OrderSeeder()
    announcement_seeder = AnnouncementSeeder()
    event_seeder = EventSeeder()
    interaction_seeder = InteractionSeeder()

    await user_seeder.seed_users(num_users=27)
    await cafe_seeder.seed_cafes(num_cafes=20, user_ids=user_seeder.get_ids())
    await staff_seeder.seed_staff(
        cafe_ids=cafe_seeder.get_ids(),
        user_ids=user_seeder.get_ids(),
    )
    await menu_seeder.seed_menu_items(cafe_ids=cafe_seeder.get_ids(), num_items=20)
    await order_seeder.seed_orders(num_orders_per_cafe=50)
    await announcement_seeder.seed_announcements()
    await event_seeder.seed_events()
    await interaction_seeder.seed_interactions()


if __name__ == "__main__":
    asyncio.run(main())
