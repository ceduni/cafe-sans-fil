import re
from typing import List
from uuid import UUID
from app.models.cafe_model import Cafe, MenuItem
from app.schemas.cafe_schema import CafeCreate, CafeUpdate, MenuItemCreate, MenuItemUpdate
from typing import Optional

class CafeService:
    """
    Service class that provides methods for CRUD operations and search functionality 
    related to Cafe and its associated MenuItems.
    """
    
    # --------------------------------------
    #               Cafe
    # --------------------------------------

    @staticmethod
    async def list_cafes(is_open: Optional[bool] = None, payment_method: Optional[str] = None) -> List[Cafe]:
        filter_criteria = {}
        if is_open is not None:
            filter_criteria["is_open"] = is_open
        if payment_method:
            filter_criteria["payment_methods.method"] = payment_method
        return await Cafe.find(filter_criteria).to_list()

    @staticmethod
    async def create_cafe(data: CafeCreate) -> Cafe:
        cafe = Cafe(**data.dict())
        await cafe.insert()
        return cafe

    @staticmethod
    async def retrieve_cafe(cafe_id: UUID):
        return await Cafe.find_one(Cafe.cafe_id == cafe_id)

    @staticmethod
    async def update_cafe(cafe_id: UUID, data: CafeUpdate):
        cafe = await CafeService.retrieve_cafe(cafe_id)
        await cafe.update({"$set": data.dict(exclude_unset=True)})
        await cafe.save()
        return cafe

    @staticmethod
    async def delete_cafe(cafe_id: UUID) -> None:
        cafe = await CafeService.retrieve_cafe(cafe_id)
        if cafe:
            await cafe.delete()

    # --------------------------------------
    #               Menu
    # --------------------------------------

    @staticmethod
    async def list_menu_items(cafe_id: UUID, category: Optional[str] = None, is_available: Optional[bool] = None) -> List[MenuItem]:
        cafe = await CafeService.retrieve_cafe(cafe_id)
        if cafe and hasattr(cafe, 'menu_items'):
            filtered_menu = []
            for item in cafe.menu_items:
                if (category is None or item.category == category) and (is_available is None or item.is_available == is_available):
                    filtered_menu.append(item)
            return filtered_menu
        return []

    @staticmethod
    async def retrieve_menu_item(cafe_id: UUID, item_id: UUID):
        cafe = await CafeService.retrieve_cafe(cafe_id)
        if cafe and hasattr(cafe, 'menu_items'):
            for item in cafe.menu_items:
                if item.item_id == item_id:
                    return item
        return None

    @staticmethod
    async def create_menu_item(cafe_id: UUID, item: MenuItemCreate) -> MenuItem:
        cafe = await CafeService.retrieve_cafe(cafe_id)
        if cafe:
            new_item = MenuItem(**item.dict())
            cafe.menu_items.append(new_item)
            await cafe.save()
            return new_item
        raise ValueError("Cafe not found")
    
    @staticmethod
    async def update_menu_item(cafe_id: UUID, item_id: UUID, item_data: MenuItemUpdate):
        cafe = await CafeService.retrieve_cafe(cafe_id)
        if cafe:
            for index, item in enumerate(cafe.menu_items):
                if item.item_id == item_id:
                    for key, value in item_data.dict(exclude_unset=True).items():
                        setattr(cafe.menu_items[index], key, value)
                    await cafe.save()
                    return cafe.menu_items[index]
        raise ValueError("Menu item not found")

    @staticmethod
    async def delete_menu_item(cafe_id: UUID, item_id: UUID) -> None:
        cafe = await CafeService.retrieve_cafe(cafe_id)
        if cafe and hasattr(cafe, 'menu_items'):
            for index, item in enumerate(cafe.menu_items):
                if item.item_id == item_id:
                    del cafe.menu_items[index]
                    await cafe.save()
                    return
        raise ValueError("Menu item not found")

    # --------------------------------------
    #               Search
    # --------------------------------------

    @staticmethod
    async def search_cafes_and_items(query: str = "", category: str = "", is_available: Optional[bool] = None, is_open: Optional[bool] = None, payment_method: str = None):

        # --- Filters ---
        regex_pattern = {"$regex": query, "$options": "i"} if query else {}
        cafe_filter = {
            "$or": [
                {"name": regex_pattern},
                {"description": regex_pattern},
                {"faculty": regex_pattern},
                {"location": regex_pattern}
            ]
        } if query else {}
        
        item_filter = {
            "$or": [
                {"name": regex_pattern},
                {"description": regex_pattern}
            ]
        } if query else {}

        if category:
            item_filter["category"] = category

        if is_available is not None:
            item_filter["is_available"] = is_available

        if is_open is not None:
            cafe_filter["is_open"] = is_open

        if payment_method:
            cafe_filter["payment_methods.method"] = payment_method

        # --- Search ---
        matching_cafes = []
        matching_items = []

        # If category or is_available filter is provided, search only menu_items
        if category or (is_available is not None):
            cafes_with_matching_items = await Cafe.find({
                "menu_items": {"$elemMatch": item_filter}
            }).to_list()
            for cafe in cafes_with_matching_items:
                matching_items.extend([item for item in cafe.menu_items if (not query or any([
                    re.search(query, item.name, re.IGNORECASE),
                    re.search(query, item.description, re.IGNORECASE)
                ]))
                and (not category or item.category == category)
                and (is_available is None or item.is_available == is_available)])

        # If is_open or payment_method filter is provided, search only cafes
        elif is_open is not None or payment_method:
            matching_cafes = await Cafe.find(cafe_filter).to_list()

        # If no filters, search cafes and menu_items
        else:
            matching_cafes = await Cafe.find(cafe_filter).to_list()
            cafes_with_matching_items = await Cafe.find({
                "menu_items": {"$elemMatch": item_filter}
            }).to_list()
            for cafe in cafes_with_matching_items:
                matching_items.extend([item for item in cafe.menu_items if not query or any([
                    re.search(query, item.name, re.IGNORECASE),
                    re.search(query, item.description, re.IGNORECASE)
                ])])

        return {
            "matching_cafes": matching_cafes,
            "matching_items": matching_items
        }