# scripts/db_seed/menu_seeder.py

import json
import random
from faker import Faker
from tqdm import tqdm
from app.services.cafe_service import CafeService
from app.services.menu_service import MenuItemService
from app.schemas.menu_schema import MenuItemCreate

fake = Faker()

# Load menu items data from JSON file
with open("./scripts/db_seed/data/menu_items.json", "r", encoding="utf-8") as file:
    menu_items_data = json.load(file)

class MenuSeeder:
    def __init__(self):
        self.menu_item_ids = []

    async def seed_menu_items(self, cafe_slugs, num_items: int):
        for cafe_slug in tqdm(cafe_slugs, desc="Seeding menu items for cafes"):
            cafe = await CafeService.retrieve_cafe(cafe_slug)
            if not cafe:
                print(f"Skipping {cafe_slug}, cafe not found.")
                continue

            randomized_menu_items = []
            for item in menu_items_data[:num_items]:
                item_copy = item.copy()
                item_copy["in_stock"] = random.random() < 0.80  # Randomly set in_stock
                randomized_menu_items.append(MenuItemCreate(**item_copy))

            # Bulk create menu items for each cafe
            created_menu_items = await MenuItemService.create_many_menu_items(cafe.cafe_id, randomized_menu_items)

            # Append the created menu item IDs
            self.menu_item_ids.extend([item.item_id for item in created_menu_items])

        print(f"{len(self.menu_item_ids)} menu items created")

    def get_menu_item_ids(self):
        return self.menu_item_ids
