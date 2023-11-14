from typing import List
from uuid import UUID
from app.models.cafe_model import Cafe, MenuItem
from app.schemas.cafe_schema import CafeCreate, CafeUpdate, MenuItemCreate, MenuItemUpdate, Role
from app.models.user_model import User
from typing import Union

class CafeService:
    """
    Service class that provides methods for CRUD operations and search functionality 
    related to Cafe and its associated MenuItems.
    """
    
    # --------------------------------------
    #               Cafe
    # --------------------------------------

    @staticmethod
    async def list_cafes(**filters) -> List[Cafe]:
        sort = None
        
        # Convert string to boolean
        if 'is_open' in filters:
            if filters['is_open'].lower() == 'true':
                filters['is_open'] = True
            elif filters['is_open'].lower() == 'false':
                filters['is_open'] = False

        if 'sort' in filters:
            sort = filters.pop('sort')

        if sort:
            return await Cafe.find(filters).sort(sort).to_list() 
        else:
            return await Cafe.find(filters).to_list()
        
    @staticmethod
    async def create_cafe(data: CafeCreate) -> Cafe:
        cafe = Cafe(**data.model_dump())
        await cafe.insert()
        return cafe

    @staticmethod
    async def retrieve_cafe(cafe_id: UUID):
        return await Cafe.find_one(Cafe.cafe_id == cafe_id)

    @staticmethod
    async def update_cafe(cafe_id: UUID, data: CafeUpdate):
        cafe = await CafeService.retrieve_cafe(cafe_id)
        await cafe.update({"$set": data.model_dump(exclude_unset=True)})
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
    async def list_menu_items(**filters) -> List[MenuItem]:
        cafe_id = filters.pop('cafe_id', None)
        sort = filters.pop('sort', None)

        # Convert string to boolean
        if 'is_available' in filters:
            if filters['is_available'].lower() == 'true':
                filters['is_available'] = True
            elif filters['is_available'].lower() == 'false':
                filters['is_available'] = False

        cafe = await CafeService.retrieve_cafe(cafe_id)
        if cafe and hasattr(cafe, 'menu_items'):
            filtered_menu = [item for item in cafe.menu_items if all(filters.get(key, getattr(item, key)) == getattr(item, key) for key in filters)]
            if sort:
                filtered_menu.sort(key=lambda item: getattr(item, sort, None))
            return filtered_menu
        return None

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
        new_item = MenuItem(**item.model_dump())
        cafe.menu_items.append(new_item)
        await cafe.save()
        return new_item
    
    @staticmethod
    async def update_menu_item(cafe_id: UUID, item_id: UUID, item_data: MenuItemUpdate):
        cafe = await CafeService.retrieve_cafe(cafe_id)
        if cafe:
            for index, item in enumerate(cafe.menu_items):
                if item.item_id == item_id:
                    for key, value in item_data.model_dump(exclude_unset=True).items():
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
    async def search_cafes_and_items(query: str, **filters):
        filter_target = filters.pop('filter_target', None)
        sort = filters.pop('sort', None)
        regex_pattern = {"$regex": query, "$options": "i"}

        # Convert string to boolean
        for key in ['is_open', 'is_available']:
            if key in filters:
                if filters[key].lower() == 'true':
                    filters[key] = True
                elif filters[key].lower() == 'false':
                    filters[key] = False

        matching_cafes = []
        matching_items = []

        # Filter cafes
        if filter_target == 'cafe' or filter_target is None:
            cafe_query = {**filters, "$or": [{"name": regex_pattern}, {"description": regex_pattern}, {"faculty": regex_pattern}, {"location": regex_pattern}]}
            matching_cafes = await Cafe.find(cafe_query).to_list()
            if sort:
                matching_cafes = await Cafe.find(cafe_query).sort(sort).to_list()
            else:
                matching_cafes = await Cafe.find(cafe_query).to_list()

        # Filter menu items
        if filter_target == 'item' or filter_target is None:
            item_query = {"menu_items": {"$elemMatch": {**filters}}}
            if query:
                item_query["menu_items"]["$elemMatch"].update({"$or": [{"name": regex_pattern}, {"description": regex_pattern}]})
            matching_cafes_temp = await Cafe.find(item_query).to_list()
            matching_items = [item for cafe in matching_cafes_temp for item in cafe.menu_items]
            if sort:
                matching_items.sort(key=lambda item: getattr(item, sort, None))

        return {"matching_cafes": matching_cafes, "matching_items": matching_items}

    # --------------------------------------
    #               Authorization
    # --------------------------------------

    @staticmethod
    async def is_authorized_for_cafe_action(cafe_id: UUID, current_user: User, required_roles: Union[Role, List[Role]]):

        # If only one role is provided, convert to a list
        if isinstance(required_roles, Role):
            required_roles = [required_roles]

        cafe = await Cafe.find_one({"cafe_id": cafe_id})
        if not cafe:
            raise ValueError("Cafe not found")

        # Check if part of staff
        user_in_staff = None
        for user in cafe.staff:
            if user.user_id == current_user.user_id:
                user_in_staff = user
                break

        # Check if appropriate role
        if user_in_staff:
            if user_in_staff.role not in [role.value for role in required_roles]:
                raise ValueError("Access forbidden")
        else:
            raise ValueError("Access forbidden")

        return True
