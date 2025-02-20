from typing import List

from beanie import PydanticObjectId

from app.cafe.models import Cafe
from app.menu.models import MenuItem
from app.menu.schemas import MenuItemCreate, MenuItemUpdate


class MenuItemService:
    """
    Service class that provides methods for CRUD operations and search functionality
    related to MenuItems.
    """

    @staticmethod
    async def list_menu_items(**query_params) -> List[MenuItem]:
        """
        Retrieves a list of menu items based on the provided query parameters.

        :param query_params: Additional query parameters to apply when retrieving menu items.
        :return: A list of MenuItem objects that match the specified query parameters.
        """
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
        """
        Retrieve a menu item from the database based on the provided PydanticObjectId.

        :param item_id: A PydanticObjectId representing the menu item ID.
        :return: A MenuItem object if found, None otherwise.
        """
        return await MenuItem.find_one({"_id": item_id})

    @staticmethod
    async def create_menu_item(
        cafe_id: PydanticObjectId, item_data: MenuItemCreate
    ) -> MenuItem:
        """
        Create a new menu item and associate it with a cafe.

        :param cafe_id: The PydanticObjectId of the cafe to associate the menu item with.
        :param item_data: The data to create the menu item with.
        :return: The created MenuItem object.
        """
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
        """
        Update a menu item based on the provided PydanticObjectId and data.

        :param item_id: The PydanticObjectId of the menu item to update.
        :param item_data: The data to update the menu item with.
        :return: The updated MenuItem object.
        """
        item = await MenuItem.find_one({"_id": item_id})
        if not item:
            raise ValueError("Menu item not found")

        for field, value in item_data.model_dump(exclude_unset=True).items():
            setattr(item, field, value)
        await item.save()
        return item

    @staticmethod
    async def delete_menu_item(item_id: PydanticObjectId) -> None:
        """
        Delete a menu item based on the provided PydanticObjectId.

        :param item_id: The PydanticObjectId of the menu item to delete.
        :return: None
        """
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
        """
        Create multiple menu items and associate them with a cafe.

        :param cafe_id: The PydanticObjectId of the cafe to associate the menu items with.
        :param items_data: A list of data to create the menu items with.
        :return: A list of created MenuItem objects.
        """
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
        """
        Update multiple menu items based on the provided list of PydanticObjectIds and data.

        :param item_ids: A list of IDs of the menu items to update.
        :param item_data: The data to update the menu items with.
        :return: A list of updated MenuItem objects.
        """
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
        """
        Delete multiple menu items based on the provided list of PydanticObjectIds.

        :param item_ids: A list of IDs of the menu items to delete.
        :return: None
        """
        items_to_delete = await MenuItem.find_many({"_id": {"$in": item_ids}}).to_list()
        if not items_to_delete:
            raise ValueError("No menu items found for the provided IDs")

        # Remove references to the menu items in associated cafes
        cafe_ids = {item.cafe_id for item in items_to_delete}
        cafes = await Cafe.find_many({"_id": {"$in": list(cafe_ids)}}).to_list()

        for cafe in cafes:
            cafe.menu_item_ids = [
                item_id for item_id in cafe.menu_item_ids if item_id not in item_ids
            ]
            await cafe.save()

        # Delete the menu items
        await MenuItem.find_many({"_id": {"$in": item_ids}}).delete_many()
