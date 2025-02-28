"""
Module for handling menu-related operations.
"""

from typing import List

from beanie import PydanticObjectId

from app.cafe.menu.models import (
    MenuCategory,
    MenuCategoryCreate,
    MenuCategoryUpdate,
    MenuItem,
    MenuItemCreate,
    MenuItemUpdate,
)
from app.cafe.models import Cafe
from app.service import set_attributes


class MenuService:
    """Service class for CRUD and search operations on Menu."""

    @staticmethod
    async def get_category_by_id(cafe: Cafe, id: PydanticObjectId) -> MenuCategory:
        """Get a menu category by ID."""
        for category in cafe.menu.categories:
            if category.id == id:
                return category

        return None

    @staticmethod
    async def get_category_by_name(cafe: Cafe, name: str) -> MenuCategory:
        """Get a menu category by name."""
        for category in cafe.menu.categories:
            if category.name == name:
                return category

        return None

    @staticmethod
    async def create_category(cafe: Cafe, data: MenuCategoryCreate) -> MenuCategory:
        """Create a new menu category."""
        for category in cafe.menu.categories:
            if category.name == data.name:
                return

        category = MenuCategory(**data.model_dump())
        cafe.menu.categories.append(category)
        await cafe.save()
        return category

    @staticmethod
    async def update_category(
        cafe: Cafe,
        id: PydanticObjectId,
        data: MenuCategoryUpdate,
    ) -> MenuCategory:
        """Update a menu category."""
        for idx, cat in enumerate(cafe.menu.categories):
            if cat.id == id:
                category = cat.model_copy(update=data.model_dump(exclude_unset=True))
                category.id = id
                cafe.menu.categories[idx] = category
                await cafe.save()
                return category

        raise None

    @staticmethod
    async def delete_category(cafe: Cafe, id: PydanticObjectId) -> None:
        """Delete a menu category."""
        original_len = len(cafe.menu.categories)
        cafe.menu.categories = [c for c in cafe.menu.categories if c.id != id]

        if len(cafe.menu.categories) == original_len:
            return

        await cafe.save()

    @staticmethod
    async def get_items(**filters: dict):
        """Get menu items."""
        sort_by = filters.pop("sort_by", "name")
        return MenuItem.find(filters).sort(sort_by)

    @staticmethod
    async def get_item_by_id_and_cafe_id(
        id: PydanticObjectId, cafe_id: PydanticObjectId
    ):
        """Get a menu item by ID and cafe ID."""
        return await MenuItem.find_one({"_id": id, "cafe_id": cafe_id})

    @staticmethod
    async def get_item(id: PydanticObjectId) -> MenuItem:
        """Get a menu item by ID."""
        return await MenuItem.get(id)

    @staticmethod
    async def create_item(cafe: Cafe, data: MenuItemCreate) -> MenuItem:
        """Create a new menu item."""
        item = MenuItem(**data.model_dump(), cafe_id=cafe.id)
        await item.insert()
        return item

    @staticmethod
    async def update_item(item: MenuItem, data: MenuItemUpdate) -> MenuItem:
        """Update a menu item."""
        set_attributes(item, data)
        await item.save()
        return item

    @staticmethod
    async def delete_item(item: MenuItem) -> None:
        """Delete a menu item."""
        await item.delete()

    @staticmethod
    async def create_many_categories(
        cafe: Cafe, datas: List[MenuCategoryCreate]
    ) -> List[MenuCategory]:
        """Create multiple menu categories."""
        for data in datas:
            for category in cafe.menu.categories:
                if category.name == data.name:
                    return
            category = MenuCategory(**data.model_dump())
            cafe.menu.categories.append(category)
        await cafe.save()
        return cafe.menu.categories

    @staticmethod
    async def create_many_items(
        cafe: Cafe, data: List[MenuItemCreate]
    ) -> List[MenuItem]:
        """Create multiple menu items."""
        items = [
            MenuItem(**item_data.model_dump(), cafe_id=cafe.id) for item_data in data
        ]
        await MenuItem.insert_many(items)
        return items

    @staticmethod
    async def update_many_items(
        ids: List[PydanticObjectId], data: MenuItemUpdate
    ) -> List[MenuItem]:
        """Update multiple menu items."""
        result = await MenuItem.find_many({"_id": {"$in": ids}}).update_many(
            {"$set": data.model_dump(exclude_unset=True)}
        )
        if result.matched_count == 0:
            return None

        return await MenuItem.find_many({"_id": {"$in": ids}}).to_list()

    @staticmethod
    async def delete_many_items(ids: List[PydanticObjectId]) -> None:
        """Delete multiple menu items."""
        await MenuItem.find_many({"_id": {"$in": ids}}).delete_many()
