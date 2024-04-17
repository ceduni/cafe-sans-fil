from typing import List
from uuid import UUID
from app.models.cafe_model import Cafe, MenuItem, Role, StaffMember
from app.schemas.cafe_schema import CafeCreate, CafeUpdate, CafeShortOut, MenuItemCreate, MenuItemUpdate, StaffCreate, StaffUpdate
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
    async def list_cafes(**query_params) -> List[Cafe]:
        """
        List cafes based on the provided query parameters.
        
        :param query_params: Dictionary with query parameters for filtering cafes.
        :return: List of Cafe objects that match the query criteria.
        """
        sort_by = query_params.pop("sort_by", "name")
        page = int(query_params.pop("page", 1))
        limit = int(query_params.pop("limit", 40))
        return await Cafe.find(query_params).project(CafeShortOut).skip((page - 1) * limit).limit(limit).sort(sort_by).to_list()
    
    @staticmethod
    async def create_cafe(data: CafeCreate) -> Cafe:
        """
        Create a new cafe using the provided data.

        :param data: The data to create the cafe with.
        :return: The created Cafe object.
        """
        try:
            cafe = Cafe(**data.model_dump())
            await cafe.insert()
            return cafe
        except Exception as e:
            if "duplicate" in str(e).lower() and len(str(e)) < 100: 
                raise ValueError(e)
            else:
                raise ValueError("Cafe already exists")

    @staticmethod
    async def retrieve_cafe(cafe_id_or_slug: str):
        """
        Retrieve a cafe from the database based on the provided cafe UUID or slug.

        :param cafe_id_or_slug: A string representing the cafe UUID or slug.
        :return: A Cafe object if found, None otherwise.
        """
        try:
            return await Cafe.find_one({"cafe_id": UUID(cafe_id_or_slug)})
        except ValueError:
            return await Cafe.find_one({"$or": [{"slug": cafe_id_or_slug}, {"previous_slugs": cafe_id_or_slug}]})

    @staticmethod
    async def update_cafe(cafe_id_or_slug: str, data: CafeUpdate):
        """
        Update a cafe based on the provided UUID or slug and data.

        :param cafe_id_or_slug: A string representing the cafe UUID or slug.
        :param data: The data to update the cafe with.
        :return: The updated Cafe object.
        """
        try:
            cafe = await CafeService.retrieve_cafe(cafe_id_or_slug)
            for field, value in data.model_dump(exclude_unset=True).items():
                setattr(cafe, field, value)
            await cafe.save()
            return cafe
        except Exception as e:
            if "duplicate" in str(e).lower() and len(str(e)) < 100:
                raise ValueError(e)
            else:
                raise ValueError("Cafe already exists")
    
    # --------------------------------------
    #               Menu
    # --------------------------------------

    @staticmethod
    async def list_menu_items(**query_params) -> List[MenuItem]:
        """
        Retrieves a list of menu items based on the provided query parameters.

        :param query_params: Additional query parameters to apply when retrieving menu items.
        :return: A list of MenuItem objects that match the specified query parameters.
        """
        slug = query_params.pop('cafe_id_or_slug', None)  # TODO: Implement cafe_id_or_slug, not just slug
        sort_by = query_params.pop('sort_by', "nothing")
        page = int(query_params.pop("page", 1))
        limit = int(query_params.pop("limit", 40))
        query = {f"menu_items.{k}": v for k, v in query_params.items()}
        pipeline = [
            {"$match": {"slug": slug}},
            {"$unwind": "$menu_items"},
            {"$match": query},
            {"$project": {"menu_items": 1, "_id": 0}},
            {"$sort": {f"menu_items.{sort_by[1:] if sort_by[0] == '-' else sort_by}": -1 if sort_by[0] == '-' else 1}},
            {"$skip": (page - 1) * limit},
            {"$limit": limit}
        ]
        menu_items = await Cafe.aggregate(pipeline).to_list()
        return [item['menu_items'] for item in menu_items] if menu_items else None
    
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
        cafe = await Cafe.find_one({"$or": [{"slug": cafe_slug}, {"previous_slugs": cafe_slug}]})
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
