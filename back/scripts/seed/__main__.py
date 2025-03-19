"""
Script to seed the database.
"""

import asyncio

from beanie import init_beanie
from motor.motor_asyncio import AsyncIOMotorClient

from app.cafe.announcement.models import Announcement
from app.cafe.menu.item.models import MenuItem
from app.cafe.models import Cafe
from app.cafe.order.models import Order
from app.config import settings
from app.event.models import Event
from app.interaction.models import Interaction
from app.user.models import User
from scripts.seed.cafe import CafeSeeder
from scripts.seed.cafe.announcement import AnnouncementSeeder
from scripts.seed.cafe.menu import MenuSeeder
from scripts.seed.cafe.order import OrderSeeder
from scripts.seed.cafe.staff import StaffSeeder
from scripts.seed.event import EventSeeder
from scripts.seed.interaction import InteractionSeeder
from scripts.seed.user import UserSeeder

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

    await UserSeeder().seed_users(num_users=27)
    await CafeSeeder().seed_cafes(num_cafes=20)
    await StaffSeeder().seed_staff()
    await MenuSeeder().seed_menu(num_items=20)
    await OrderSeeder().seed_orders(num_orders_per_cafe=50)
    await AnnouncementSeeder().seed_announcements()
    await EventSeeder().seed_events()
    await InteractionSeeder().seed_interactions()


if __name__ == "__main__":
    asyncio.run(main())
