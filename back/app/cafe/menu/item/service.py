"""
Module for handling item-related operations.
"""

from typing import List, Union

from beanie import PydanticObjectId
from beanie.odm.queries.find import FindMany

from app.cafe.menu.item.models import MenuItem, MenuItemCreate, MenuItemUpdate
from app.cafe.models import Cafe
from app.service import set_attributes


class ItemService:
    """Service class for CRUD and search operations on Menu."""

    @staticmethod
    async def get_all(to_list: bool = True, **filters: dict) -> Union[FindMany[MenuItem], List[MenuItem]]:
        """Get menu items."""
        sort_by = filters.pop("sort_by", "name")
        query = MenuItem.find(filters).sort(sort_by)
        
        return await query.to_list() if to_list else query

    @staticmethod
    async def get_by_ids_and_cafe_id(
        ids: List[PydanticObjectId], cafe_id: PydanticObjectId
    ) -> list[MenuItem]:
        return await MenuItem.find({"cafe_id": cafe_id, "_id": {"$in": ids}}).to_list()

    @staticmethod
    async def get_by_id_and_cafe_id(id: PydanticObjectId, cafe_id: PydanticObjectId):
        """Get a menu item by ID and cafe ID."""
        return await MenuItem.find_one({"_id": id, "cafe_id": cafe_id})

    @staticmethod
    async def get(id: PydanticObjectId) -> MenuItem:
        """Get a menu item by ID."""
        return await MenuItem.get(id)

    @staticmethod
    async def create(cafe: Cafe, data: MenuItemCreate) -> MenuItem:
        """Create a new menu item."""
        item = MenuItem(**data.model_dump(), cafe_id=cafe.id)
        await item.insert()
        return item

    @staticmethod
    async def update(item: MenuItem, data: MenuItemUpdate) -> MenuItem:
        """Update a menu item."""
        set_attributes(item, data)
        await item.save()
        return item

    @staticmethod
    async def delete(item: MenuItem) -> None:
        """Delete a menu item."""
        await item.delete()

    @staticmethod
    async def create_many(cafe: Cafe, data: List[MenuItemCreate]) -> List[MenuItem]:
        """Create multiple menu items."""
        items = [
            MenuItem(**item_data.model_dump(), cafe_id=cafe.id) for item_data in data
        ]
        await MenuItem.insert_many(items)
        return items

    @staticmethod
    async def update_many(
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
    async def delete_many(ids: List[PydanticObjectId]) -> None:
        """Delete multiple menu items."""
        await MenuItem.find_many({"_id": {"$in": ids}}).delete_many()
