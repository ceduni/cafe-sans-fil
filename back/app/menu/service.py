"""
Module for handling menu item-related operations.
"""

from typing import List

from beanie import PydanticObjectId

from app.cafe.models import Cafe
from app.menu.models import MenuItem, MenuItemCreate, MenuItemUpdate


class MenuItemService:
    """Service class for CRUD and search operations on MenuItems."""

    @staticmethod
    async def list_menu_items(**query_params) -> List[MenuItem]:
        """Retrieve a list of menu items based on the provided query parameters."""
        sort_by = query_params.pop("sort_by", "name")
        page = int(query_params.pop("page", 1))
        limit = int(query_params.pop("limit", 40))
        return (
            await MenuItem.find(query_params)
            .skip((page - 1) * limit)
            .limit(limit)
            .sort(sort_by)
            .to_list()
        )

    @staticmethod
    async def retrieve_menu_item(item_id: PydanticObjectId) -> MenuItem:
        """Retrieve a menu item by ID."""
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
        cafe.menu_item_ids.append(new_item.id)
        await cafe.save()
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

        cafe = await Cafe.find_one({"_id": item.cafe_id})
        if cafe:
            cafe.menu_item_ids.remove(item_id)
            await cafe.save()

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

        item_ids = [new_item.id for new_item in new_items]
        cafe.menu_item_ids.extend(item_ids)
        await cafe.save()

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

        for cafe in cafes:
            cafe.menu_item_ids = [
                item_id for item_id in cafe.menu_item_ids if item_id not in item_ids
            ]
            await cafe.save()

        # Delete the menu items
        await MenuItem.find_many({"_id": {"$in": item_ids}}).delete_many()
