"""
Menu seeder module.
"""

import json
import random

from faker import Faker
from tqdm import tqdm

from app.cafe.service import CafeService
from app.menu.models import MenuItemCreate
from app.menu.service import MenuItemService

random.seed(42)
Faker.seed(42)
fake = Faker("fr_FR")

with open("./scripts/db_seed/data/menu_items.json", "r", encoding="utf-8") as file:
    menu_items_data = json.load(file)


class MenuSeeder:
    def __init__(self):
        self.menu_item_ids = []

    async def seed_menu_items(self, cafe_ids, num_items: int):
        """Seeds menu items for cafes."""
        for cafe_id in tqdm(cafe_ids, desc="Seeding menu items for cafes"):
            cafe = await CafeService.retrieve_cafe(cafe_id, False)
            if not cafe:
                print(f"Skipping {cafe_id}, cafe not found.")
                continue

            randomized_menu_items = []
            for item in menu_items_data[:num_items]:
                item_copy = item.copy()
                item_copy["in_stock"] = random.random() < 0.80  # Randomly set in_stock
                randomized_menu_items.append(MenuItemCreate(**item_copy))

            created_menu_items = await MenuItemService.create_many_menu_items(
                cafe.id, randomized_menu_items
            )

            self.menu_item_ids.extend([item.id for item in created_menu_items])

        print(f"{len(self.menu_item_ids)} menu items created")

    def get_menu_item_ids(self):
        """Returns the list of menu item IDs."""
        return self.menu_item_ids
