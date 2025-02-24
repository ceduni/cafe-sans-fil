"""
Module for handling menu-related operations.
"""

from typing import List

from beanie import PydanticObjectId

from app.cafe.models import Cafe
from app.cafe_menu.models import (
    MenuCategory,
    MenuCategoryCreate,
    MenuCategoryOut,
    MenuCategoryUpdate,
    MenuItem,
    MenuItemCreate,
    MenuItemUpdate,
)


class MenuService:
    """Service class for CRUD and search operations on Menu."""

    @staticmethod
    async def create_menu_category(
        cafe_id: PydanticObjectId, category_data: MenuCategoryCreate
    ) -> MenuCategoryOut:
        """Create a new menu category for a cafe."""
        cafe = await Cafe.find_one({"_id": cafe_id})
        if not cafe:
            raise ValueError("Cafe not found")

        new_category = MenuCategory(**category_data.model_dump())
        print(new_category.model_dump())
        cafe.menu_categories.append(new_category)
        await cafe.save()
        return MenuCategoryOut(**new_category.model_dump())

    @staticmethod
    async def update_menu_category(
        cafe_id: PydanticObjectId,
        category_id: PydanticObjectId,
        update_data: MenuCategoryUpdate,
    ) -> MenuCategoryOut:
        """Update a menu category for a cafe."""
        cafe = await Cafe.find_one({"_id": cafe_id})
        if not cafe:
            raise ValueError("Cafe not found")

        for idx, category in enumerate(cafe.menu_categories):
            if category.id == category_id:
                updated_data = category.model_dump() | update_data.model_dump(
                    exclude_unset=True
                )
                cafe.menu_categories[idx] = MenuCategory(**updated_data)
                await cafe.save()
                return MenuCategoryOut(**cafe.menu_categories[idx].model_dump())

        raise ValueError("Category not found")

    @staticmethod
    async def delete_menu_category(
        cafe_id: PydanticObjectId, category_id: PydanticObjectId
    ) -> None:
        """Delete a menu category for a cafe."""
        cafe = await Cafe.find_one({"_id": cafe_id})
        if not cafe:
            raise ValueError("Cafe not found")

        original_length = len(cafe.menu_categories)
        cafe.menu_categories = [c for c in cafe.menu_categories if c.id != category_id]

        if len(cafe.menu_categories) == original_length:
            raise ValueError("Category not found")

        await cafe.save()

    @staticmethod
    async def get_menu_items(**filters: dict):
        """Get menu items."""
        sort_by = filters.pop("sort_by", "name")
        return MenuItem.find(filters).sort(sort_by)

    @staticmethod
    async def get_menu_item(item_id: PydanticObjectId) -> MenuItem:
        """Get a menu item by ID."""
        return await MenuItem.find_one({"_id": item_id})

    @staticmethod
    async def create_menu_item(
        cafe_id: PydanticObjectId, item_data: MenuItemCreate
    ) -> MenuItem:
        """Create a new menu item for a cafe."""
        cafe = await Cafe.find_one({"_id": cafe_id})
        if not cafe:
            raise ValueError("Cafe not found")

        new_item = MenuItem(**item_data.model_dump(), cafe_id=cafe_id)
        await new_item.insert()
        return new_item

    @staticmethod
    async def update_menu_item(
        item_id: PydanticObjectId, item_data: MenuItemUpdate
    ) -> MenuItem:
        """Update a menu item."""
        item = await MenuItem.find_one({"_id": item_id})
        if not item:
            raise ValueError("Menu item not found")

        for field, value in item_data.model_dump(exclude_unset=True).items():
            setattr(item, field, value)
        await item.save()
        return item

    @staticmethod
    async def delete_menu_item(item_id: PydanticObjectId) -> None:
        """Delete a menu item."""
        item = await MenuItem.find_one({"_id": item_id})
        if not item:
            raise ValueError("Menu item not found")

        await item.delete()

    @staticmethod
    async def create_many_menu_items(
        cafe_id: PydanticObjectId, items_data: List[MenuItemCreate]
    ) -> List[MenuItem]:
        """Create multiple menu items for a cafe."""
        cafe = await Cafe.find_one({"_id": cafe_id})
        if not cafe:
            raise ValueError("Cafe not found")

        new_items = [
            MenuItem(**item_data.model_dump(), cafe_id=cafe_id)
            for item_data in items_data
        ]
        await MenuItem.insert_many(new_items)
        return new_items

    @staticmethod
    async def update_many_menu_items(
        item_ids: List[PydanticObjectId], item_data: MenuItemUpdate
    ) -> List[MenuItem]:
        """Update multiple menu items."""
        update_data = item_data.model_dump(exclude_unset=True)
        if not update_data:
            raise ValueError("No data to update")

        result = await MenuItem.find_many({"_id": {"$in": item_ids}}).update_many(
            {"$set": update_data}
        )
        if result.matched_count == 0:
            raise ValueError("No menu items found for the provided IDs")

        return await MenuItem.find_many({"_id": {"$in": item_ids}}).to_list()

    @staticmethod
    async def delete_many_menu_items(item_ids: List[PydanticObjectId]) -> None:
        """Delete multiple menu items."""
        items_to_delete = await MenuItem.find_many({"_id": {"$in": item_ids}}).to_list()
        if not items_to_delete:
            raise ValueError("No menu items found for the provided IDs")

        cafe_ids = {item.cafe_id for item in items_to_delete}
        cafes = await Cafe.find_many({"_id": {"$in": list(cafe_ids)}}).to_list()

        # Delete the menu items
        await MenuItem.find_many({"_id": {"$in": item_ids}}).delete_many()
