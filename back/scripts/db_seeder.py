"""
Script to seed the database with sample data.
"""

import asyncio

from beanie import init_beanie
from motor.motor_asyncio import AsyncIOMotorClient

from app.announcement.models import Announcement
from app.cafe.models import Cafe
from app.cafe_menu.models import MenuItem
from app.config import settings
from app.event.models import Event
from app.order.models import Order
from app.user.models import User
from scripts.db_seed import CafeSeeder, MenuSeeder, StaffSeeder, UserSeeder

MONGO_DB_NAME = settings.MONGO_DB_NAME
print(f"Seeding data for {MONGO_DB_NAME}")


async def main():
    """Main function to seed the database."""
    db_client = AsyncIOMotorClient(settings.MONGO_CONNECTION_STRING)
    db_client.drop_database(MONGO_DB_NAME)

    db_client = AsyncIOMotorClient(settings.MONGO_CONNECTION_STRING)[MONGO_DB_NAME]
    await init_beanie(
        database=db_client,
        document_models=[Cafe, MenuItem, Announcement, Event, User, Order],
    )

    user_seeder = UserSeeder()
    cafe_seeder = CafeSeeder()
    staff_seeder = StaffSeeder()
    menu_seeder = MenuSeeder()

    await user_seeder.seed_users(num_users=27)
    await cafe_seeder.seed_cafes(num_cafes=20)
    await staff_seeder.seed_staff_for_cafes(
        cafe_ids=cafe_seeder.get_cafe_ids(), usernames=user_seeder.get_usernames()
    )
    await menu_seeder.seed_menu_items(cafe_ids=cafe_seeder.get_cafe_ids(), num_items=20)


if __name__ == "__main__":
    asyncio.run(main())
