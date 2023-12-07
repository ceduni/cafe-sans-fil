from typing import List
from uuid import UUID
from app.models.cafe_model import Cafe, MenuItem, Role, StaffMember
from app.schemas.cafe_schema import CafeCreate, CafeUpdate, MenuItemCreate, MenuItemUpdate, StaffCreate, StaffUpdate
from app.models.user_model import User

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
        # Example: http://cafesansfil-api.onrender.com/api/cafes?is_open=true&sort_by=-name&page=1&limit=10
        query_filters = {}
        page = int(filters.pop('page', 1))
        limit = int(filters.pop('limit', 40))

        # Convert 'is_open' string to boolean
        if 'is_open' in filters:
            if filters['is_open'].lower() == 'true':
                query_filters['is_open'] = True
            elif filters['is_open'].lower() == 'false':
                query_filters['is_open'] = False


        sort_by = filters.pop('sort_by', 'name')  # Default sort field
        sort_order = -1 if sort_by.startswith('-') else 1
        sort_field = sort_by[1:] if sort_order == -1 else sort_by
        sort_params = [(sort_field, sort_order)]

        cafes_cursor = Cafe.aggregate([
            {"$match": query_filters},
            {"$sort": dict(sort_params)},
            {"$skip": (page - 1) * limit},
            {"$limit": limit}
        ])

        return await cafes_cursor.to_list(None)
    
    @staticmethod
    async def create_cafe(data: CafeCreate) -> Cafe:
        try:
            cafe = Cafe(**data.model_dump())
            await cafe.insert()
            return cafe
        except Exception as e:
            if "duplicate" or "'type': 'model_attributes_type', 'loc': ('response',), 'msg': 'Input should be a valid dictionary or object to extract fields from'" in str(e):
                raise ValueError("Cafe already exists")

    @staticmethod
    async def retrieve_cafe(cafe_slug: str):
        return await Cafe.find_one(Cafe.slug == cafe_slug)
    
    @staticmethod
    async def update_cafe(cafe_slug: str, data: CafeUpdate):
        try:
            cafe = await CafeService.retrieve_cafe(cafe_slug)
            
            for field, value in data.model_dump(exclude_unset=True).items():
                setattr(cafe, field, value)

            await cafe.save()

            return cafe
        except Exception as e:
            if "duplicate" or "'type': 'model_attributes_type', 'loc': ('response',), 'msg': 'Input should be a valid dictionary or object to extract fields from'" in str(e):
                raise ValueError("Cafe already exists")

    # --------------------------------------
    #               Menu
    # --------------------------------------

    @staticmethod
    async def list_menu_items(**filters) -> List[MenuItem]:
        # Currently not used
        cafe_slug = filters.pop('slug', None)
        sort = filters.pop('sort', None)

        # Convert string to boolean
        if 'in_stock' in filters:
            if filters['in_stock'].lower() == 'true':
                filters['in_stock'] = True
            elif filters['in_stock'].lower() == 'false':
                filters['in_stock'] = False

        cafe = await CafeService.retrieve_cafe(cafe_slug)
        if cafe and hasattr(cafe, 'menu_items'):
            filtered_menu = [item for item in cafe.menu_items if all(filters.get(key, getattr(item, key)) == getattr(item, key) for key in filters)]
            if sort:
                filtered_menu.sort(key=lambda item: getattr(item, sort, None))
            return filtered_menu
        return None

    @staticmethod
    async def retrieve_menu_item(cafe_slug: str, item_slug: str):
        cafe = await CafeService.retrieve_cafe(cafe_slug)
        if cafe and hasattr(cafe, 'menu_items'):
            for item in cafe.menu_items:
                if item.slug == item_slug:
                    return item
        return None

    @staticmethod
    async def create_menu_item(cafe_slug: str, item: MenuItemCreate) -> MenuItem:
        cafe = await CafeService.retrieve_cafe(cafe_slug)
        new_item = MenuItem(**item.model_dump())
        cafe.menu_items.append(new_item)
        await cafe.save()
        return new_item
    
    @staticmethod
    async def update_menu_item(cafe_slug: str, item_slug: str, item_data: MenuItemUpdate):
        cafe = await CafeService.retrieve_cafe(cafe_slug)
        if cafe:
            for index, item in enumerate(cafe.menu_items):
                if item.slug == item_slug:
                    for key, value in item_data.model_dump(exclude_unset=True).items():
                        setattr(cafe.menu_items[index], key, value)
                    await cafe.save()
                    return cafe.menu_items[index]
        raise ValueError("Menu item not found")

    @staticmethod
    async def delete_menu_item(cafe_slug: str, item_slug: str) -> None:
        cafe = await CafeService.retrieve_cafe(cafe_slug)
        if cafe and hasattr(cafe, 'menu_items'):
            for index, item in enumerate(cafe.menu_items):
                if item.slug == item_slug:
                    del cafe.menu_items[index]
                    await cafe.save()
                    return
        raise ValueError("Menu item not found")

    # --------------------------------------
    #               Staff
    # --------------------------------------

    @staticmethod
    async def list_staff_members(cafe_slug: str):
        cafe = await CafeService.retrieve_cafe(cafe_slug)
        if cafe and hasattr(cafe, 'staff'):
            return cafe.staff
        raise ValueError("Cafe not found")

    @staticmethod
    async def retrieve_staff_member(cafe_slug: str, username: str):
        cafe = await CafeService.retrieve_cafe(cafe_slug)
        if cafe and hasattr(cafe, 'staff'):
            for member in cafe.staff:
                if member.username == username:
                    return member
        else:
            raise ValueError(f"Cafe not found")

    @staticmethod
    async def create_staff_member(cafe_slug: str, staff_data: StaffCreate):
        cafe = await CafeService.retrieve_cafe(cafe_slug)
        if cafe:
            new_staff_member = StaffMember(**staff_data.dict())
            cafe.staff.append(new_staff_member)
            await cafe.save()
            return new_staff_member
        raise ValueError("Cafe not found")

    @staticmethod
    async def update_staff_member(cafe_slug: str, username: str, staff_data: StaffUpdate):
        cafe = await CafeService.retrieve_cafe(cafe_slug)
        if cafe and hasattr(cafe, 'staff'):
            for member in cafe.staff:
                if member.username == username:
                    for key, value in staff_data.dict(exclude_unset=True).items():
                        setattr(member, key, value)
                    await cafe.save()
                    return member
            raise ValueError("Staff member not found")
        raise ValueError("Cafe not found")

    @staticmethod
    async def delete_staff_member(cafe_slug: str, username: str):
        cafe = await CafeService.retrieve_cafe(cafe_slug)
        if cafe and hasattr(cafe, 'staff'):
            # Check if the staff member exists in the cafe
            if any(member.username == username for member in cafe.staff):
                # Remove the staff member
                cafe.staff = [member for member in cafe.staff if member.username != username]
                await cafe.save()
            else:
                raise ValueError("Staff member not found")
        else:
            raise ValueError(f"Cafe not found")
        
    # --------------------------------------
    #               Search
    # --------------------------------------

    @staticmethod
    async def search_cafes_and_items(query: str, **filters):
        # Currently not used, filter in frontend instead
        # TODO: Text search and autocomplete with MongoDB

        filter_target = filters.pop('filter_target', None)
        sort = filters.pop('sort', None)
        regex_pattern = {"$regex": query, "$options": "i"}

        # Convert string to boolean
        for key in ['is_open', 'in_stock']:
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
    async def is_authorized_for_cafe_action_by_id(cafe_id: UUID, current_user: User, required_roles: List[Role]):
        cafe = await Cafe.find_one({"cafe_id": cafe_id})
        if not cafe:
            raise ValueError("Cafe not found")

        # Check if part of staff
        user_in_staff = None
        for user in cafe.staff:
            if user.username == current_user.username:
                user_in_staff = user
                break

        # Check if appropriate role
        if user_in_staff:
            if user_in_staff.role not in [role.value for role in required_roles]:
                raise ValueError("Access forbidden")
        else:
            raise ValueError("Access forbidden")

        return True

    @staticmethod
    async def is_authorized_for_cafe_action_by_slug(cafe_slug: str, current_user: User, required_roles: List[Role]):
        cafe = await Cafe.find_one({"slug": cafe_slug})
        if not cafe:
            raise ValueError("Cafe not found")

        # Check if part of staff
        user_in_staff = None
        for user in cafe.staff:
            if user.username == current_user.username:
                user_in_staff = user
                break

        # Check if appropriate role
        if user_in_staff:
            if user_in_staff.role not in [role.value for role in required_roles]:
                raise ValueError("Access forbidden")
        else:
            raise ValueError("Access forbidden")

        return True
