"""
Menu seeder module.
"""

import json
import os
import random
from typing import Dict

from tqdm import tqdm

from app.cafe.menu.category.models import MenuCategoryCreate
from app.cafe.menu.category.service import CategoryService
from app.cafe.menu.item.models import MenuItemCreate
from app.cafe.menu.item.service import ItemService
from app.cafe.service import CafeService

random.seed(42)


class MenuSeeder:
    """Menu seeder class."""

    def __init__(self):
        """Initializes the MenuSeeder."""
        self.menu_data = self._load_data()

    def _load_data(self):
        """Loads menu data from a JSON file."""
        path = os.path.join(os.getcwd(), "scripts", "seed", "data", "menu.json")
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)

    async def seed_menu(self, num_items: int):
        """Seeds menu items for cafes."""
        cafes = await CafeService.get_all()

        for cafe in tqdm(cafes, desc="Menu"):
            # Mapping categories
            category_map = await self._create_categories(cafe)

            randomized_menu_items = []
            for item in self.menu_data[:num_items]:
                item_copy = item.copy()
                category_name = item_copy.pop("category")

                category_id = category_map.get(category_name)
                if not category_id:
                    print(f"Skipping item with unknown category: {category_name}")
                    continue

                item_copy["category_ids"] = [category_id]
                item_copy["in_stock"] = random.random() < 0.80
                randomized_menu_items.append(MenuItemCreate(**item_copy))

            await ItemService.create_many(cafe, randomized_menu_items)

    async def _create_categories(self, cafe: str) -> Dict[str, str]:
        """Create predefined categories for a cafe and return name->ID mapping"""
        category_map = {}
        categories = await CategoryService.create_many(
            cafe,
            [
                MenuCategoryCreate(**category)
                for category in self._predefined_categories()
            ],
        )
        for category in categories:
            category_map[category.name] = category.id
        return category_map

    def _predefined_categories(self):
        return [
            {
                "name": "Grilled Cheese",
                "description": "Sandwichs grillés au fromage fondant",
            },
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
