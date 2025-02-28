"""
Menu seeder module.
"""

import json
import random
from pathlib import Path
from typing import Dict

from faker import Faker
from tqdm import tqdm

from app.cafe.menu.category.models import MenuCategoryCreate
from app.cafe.menu.category.service import CategoryService
from app.cafe.menu.item.models import MenuItemCreate
from app.cafe.menu.item.service import ItemService
from app.cafe.service import CafeService

random.seed(42)
Faker.seed(42)
fake = Faker("fr_FR")


PREDEFINED_CATEGORIES = [
    {"name": "Grilled Cheese", "description": "Sandwichs grillés au fromage fondant"},
    {
        "name": "Boissons chaudes",
        "description": "Cafés, thés et autres boissons chaudes",
    },
    {
        "name": "Boissons froides",
        "description": "Rafraîchissements et boissons froides",
    },
    {"name": "Collations", "description": "En-cas et petites faims"},
]


file_path = Path(__file__).parent / "data/menu_items.json"
with open(file_path, "r", encoding="utf-8") as file:
    menu_items_data = json.load(file)


class MenuSeeder:
    def __init__(self):
        self.menu_item_ids = []
        self.category_map: Dict[str, Dict[str, str]] = {}

    async def _create_categories(self, cafe: str) -> Dict[str, str]:
        """Create predefined categories for a cafe and return name->ID mapping"""
        category_map = {}
        categories = await CategoryService.create_many_categories(
            cafe, [MenuCategoryCreate(**category) for category in PREDEFINED_CATEGORIES]
        )
        for category in categories:
            category_map[category.name] = category.id
        return category_map

    async def seed_menu_items(self, cafe_ids, num_items: int):
        """Seeds menu items for cafes with proper category mapping"""
        for cafe_id in tqdm(cafe_ids, desc="Seeding menu items for cafes"):
            cafe = await CafeService.get(cafe_id, False)
            if not cafe:
                print(f"Skipping {cafe_id}, cafe not found.")
                continue

            # Mapping categories
            category_map = await self._create_categories(cafe)
            self.category_map[cafe.id] = category_map

            randomized_menu_items = []
            for item in menu_items_data[:num_items]:
                item_copy = item.copy()
                category_name = item_copy.pop("category")

                category_id = category_map.get(category_name)
                if not category_id:
                    print(f"Skipping item with unknown category: {category_name}")
                    continue

                item_copy["category_id"] = category_id
                item_copy["in_stock"] = random.random() < 0.80
                randomized_menu_items.append(MenuItemCreate(**item_copy))

            items = await ItemService.create_many_items(cafe, randomized_menu_items)
            # self.menu_item_ids.extend([item.id for item in items])

        print(f"Menu items created")

    def get_menu_item_ids(self):
        """Returns the list of menu item IDs."""
        return self.menu_item_ids

    def get_category_map(self):
        """Returns the category name->ID mapping per cafe"""
        return self.category_map
