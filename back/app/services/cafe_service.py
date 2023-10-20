import re
from typing import List
from uuid import UUID
from app.models.cafe_model import Cafe as CafeModel
from app.models.cafe_model import MenuItem as MenuItemModel 
from app.schemas.cafe_schema import Cafe
from app.schemas.cafe_schema import MenuItem
from typing import Optional

class CafeService:
    # --------------------------------------
    #               Cafe
    # --------------------------------------
    @staticmethod
    async def list_cafes() -> List[Cafe]:
        return await CafeModel.all().to_list()
    
    @staticmethod
    async def create_cafe(data: Cafe) -> CafeModel:
        cafe = CafeModel(**data.dict())
        await cafe.insert()
        return cafe

    @staticmethod
    async def retrieve_cafe(cafe_id: UUID) -> CafeModel:
        return await CafeModel.find_one(CafeModel.cafe_id == cafe_id)

    @staticmethod
    async def update_cafe(cafe_id: UUID, data: Cafe) -> CafeModel:
        cafe = await CafeService.retrieve_cafe(cafe_id)
        await cafe.update({"$set": data.dict(exclude_unset=True)})
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
    async def retrieve_cafe_menu(cafe_id: UUID) -> List[MenuItem]:
        cafe = await CafeService.retrieve_cafe(cafe_id)
        if cafe and hasattr(cafe, 'menu_items'):
            return cafe.menu_items
        return []

    @staticmethod
    async def retrieve_menu_item(cafe_id: UUID, item_id: UUID) -> Optional[MenuItem]:
        cafe = await CafeService.retrieve_cafe(cafe_id)
        if cafe and hasattr(cafe, 'menu_items'):
            for item in cafe.menu_items:
                if item.item_id == item_id:
                    return item
        return None

    @staticmethod
    async def create_menu_item(cafe_id: UUID, item: MenuItem) -> MenuItem:
        cafe = await CafeService.retrieve_cafe(cafe_id)
        if cafe:
            new_item = MenuItemModel(**item.dict())
            cafe.menu_items.append(new_item)
            await cafe.save()
            return new_item
        raise ValueError("Cafe not found")
    
    @staticmethod
    async def update_menu_item(cafe_id: UUID, item_id: UUID, item_data: MenuItem) -> MenuItem:
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
    async def search_cafes_and_items(query: str):
        # Search for cafes
        matching_cafes = await CafeModel.find({"name": {"$regex": query, "$options": "i"}}).to_list()
        
        # Search for menu_items
        cafes = await CafeModel.find({"menu_items": {"$elemMatch": {"name": {"$regex": query, "$options": "i"}}}}).to_list()
        matching_items = []
        for cafe in cafes:
            for item in cafe.menu_items:
                if re.search(query, item.name, re.IGNORECASE):
                    matching_items.append(item)

        return {
            "matching_cafes": matching_cafes,
            "matching_items": matching_items
        }
