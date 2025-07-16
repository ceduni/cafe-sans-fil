"""
Script to seed the database.
"""

import asyncio

from beanie import init_beanie
from motor.motor_asyncio import AsyncIOMotorClient

from app.cafe.announcement.models import Announcement
from app.menu.item.models import MenuItem
from app.cafe.models import Cafe
from app.order.models import Order
from app.config import settings
from app.event.models import Event
from app.interaction.models import Interaction
from app.notification.models import NotificationMessage, NotificationStatus
from app.user.models import User, Diet
from scripts.seed.cafe import CafeSeeder
from scripts.seed.cafe.announcement import AnnouncementSeeder
from scripts.seed.cafe.menu import MenuSeeder
from scripts.seed.cafe.order import OrderSeeder
from scripts.seed.cafe.staff import StaffSeeder
from scripts.seed.event import EventSeeder
from scripts.seed.interaction import InteractionSeeder
from scripts.seed.notification import NotificationSeeder
from scripts.seed.user import UserSeeder
from scripts.seed.diet import DietSeeder

MONGO_DB_NAME = settings.MONGO_DB_NAME
print(f"Seeding data for {MONGO_DB_NAME}")


async def main():
    """Main function to seed the database."""
    db_client = AsyncIOMotorClient(settings.MONGO_CONNECTION_STRING)
    db_client.drop_database(MONGO_DB_NAME)

    db_client = AsyncIOMotorClient(settings.MONGO_CONNECTION_STRING)[MONGO_DB_NAME]
    await init_beanie(
        database=db_client,
        document_models=[Cafe, MenuItem, Announcement, Event, User, Diet, Order, Interaction, NotificationMessage, NotificationStatus],
    )

    await UserSeeder().seed_users(num_users=20)
    await CafeSeeder().seed_cafes(num_cafes=20)
    await StaffSeeder().seed_staff()
    await MenuSeeder().seed_menu(num_items=10)
    await DietSeeder().seed_diet(num_diets=10)
    await OrderSeeder().seed_orders(num_orders_per_cafe=30)
    await AnnouncementSeeder().seed_announcements()
    await EventSeeder().seed_events()
    await InteractionSeeder().seed_interactions()
    await NotificationSeeder().seed_notifications(num_notifications=100, num_notifications_per_user=[5, 10])


if __name__ == "__main__":
    asyncio.run(main())
