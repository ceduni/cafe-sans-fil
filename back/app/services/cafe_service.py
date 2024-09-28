from typing import List
from uuid import UUID
from app.models.cafe_model import Cafe, Role, StaffMember
from app.schemas.cafe_schema import (
    CafeCreate,
    CafeUpdate,
    CafeShortOut,
    StaffCreate,
    StaffUpdate,
)
from app.models.user_model import User


class CafeService:
    """
    Service class that provides methods for CRUD operations and search functionality
    related to Cafe.
    """

    # --------------------------------------
    #               Cafe
    # --------------------------------------

    @staticmethod
    async def list_cafes(**query_params) -> List[CafeShortOut]:
        """
        List cafes based on the provided query parameters.

        :param query_params: Dictionary with query parameters for filtering cafes.
        :return: List of Cafe objects that match the query criteria.
        """
        sort_by = query_params.pop("sort_by", "name")
        page = int(query_params.pop("page", 1))
        limit = int(query_params.pop("limit", 40))
        return (
            await Cafe.find(query_params)
            .project(CafeShortOut)
            .skip((page - 1) * limit)
            .limit(limit)
            .sort(sort_by)
            .to_list()
        )

    @staticmethod
    async def retrieve_cafe(cafe_slug_or_id):
        """
        Retrieve a cafe from the database based on the provided cafe slug or UUID.

        :param cafe_slug_or_id: A string representing the cafe slug or UUID, or a UUID.
        :return: A Cafe object if found, None otherwise.
        """
        if isinstance(cafe_slug_or_id, UUID):
            return await Cafe.find_one({"_id": cafe_slug_or_id})

        try:
            cafe_id = UUID(cafe_slug_or_id)
            return await Cafe.find_one({"_id": cafe_id})
        except ValueError:
            return await Cafe.find_one(
                {
                    "$or": [
                        {"slug": cafe_slug_or_id},
                        {"previous_slugs": cafe_slug_or_id},
                    ]
                }
            )
        
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
    async def update_cafe(cafe_id: UUID, data: CafeUpdate):
        """
        Update a cafe based on the provided UUID and data.

        :param cafe_id: A UUID representing the cafe.
        :param data: The data to update the cafe with.
        :return: The updated Cafe object.
        """
        try:
            cafe = await Cafe.find_one({"_id": cafe_id})
            if not cafe:
                raise ValueError("Cafe not found")

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
    #               Staff
    # --------------------------------------

    @staticmethod
    async def list_staff_members(cafe_id: UUID):
        """
        List staff members of the cafe identified by cafe_id.

        :param cafe_id: The UUID of the cafe.
        :return: List of StaffMember objects.
        """
        cafe = await Cafe.find_one({"_id": cafe_id})
        if not cafe:
            raise ValueError("Cafe not found")
        return cafe.staff

    @staticmethod
    async def retrieve_staff_member(cafe_id: UUID, username: str):
        """
        Retrieve a staff member by username from the cafe identified by cafe_id.

        :param cafe_id: The UUID of the cafe.
        :param username: The username of the staff member to retrieve.
        :return: A StaffMember object if found.
        """
        cafe = await Cafe.find_one({"_id": cafe_id})
        if not cafe:
            raise ValueError("Cafe not found")
        
        for member in cafe.staff:
            if member.username == username:
                return member
        
        raise ValueError("Staff member not found")
    
    @staticmethod
    async def create_staff_member(cafe_id: UUID, staff_data: StaffCreate):
        cafe = await Cafe.find_one({"_id": cafe_id})
        if not cafe:
            raise ValueError("Cafe not found")

        new_staff_member = StaffMember(**staff_data.model_dump())
        cafe.staff.append(new_staff_member)
        await cafe.save()
        return new_staff_member

    @staticmethod
    async def update_staff_member(cafe_id: UUID, username: str, staff_data: StaffUpdate):
        cafe = await Cafe.find_one({"_id": cafe_id})
        if not cafe:
            raise ValueError("Cafe not found")

        for member in cafe.staff:
            if member.username == username:
                for key, value in staff_data.model_dump(exclude_unset=True).items():
                    setattr(member, key, value)
                await cafe.save()
                return member

        raise ValueError("Staff member not found")

    @staticmethod
    async def delete_staff_member(cafe_id: UUID, username: str):
        cafe = await Cafe.find_one({"_id": cafe_id})
        if not cafe:
            raise ValueError("Cafe not found")

        if any(member.username == username for member in cafe.staff):
            # Remove the staff member
            cafe.staff = [
                member for member in cafe.staff if member.username != username
            ]
            await cafe.save()
        else:
            raise ValueError("Staff member not found")

    @staticmethod
    async def create_many_staff_members(cafe_id: UUID, staff_data_list: List[StaffCreate]) -> List[StaffMember]:
        """
        Create multiple staff members for a cafe.

        :param cafe_id: The UUID of the cafe.
        :param staff_data_list: A list of staff data to create.
        :return: A list of created StaffMember objects.
        """
        cafe = await Cafe.find_one({"_id": cafe_id})
        if not cafe:
            raise ValueError("Cafe not found")

        new_staff_members = [StaffMember(**staff_data.model_dump()) for staff_data in staff_data_list]
        cafe.staff.extend(new_staff_members)
        await cafe.save()
        return new_staff_members

    @staticmethod
    async def update_many_staff_members(cafe_id: UUID, usernames: List[str], staff_data: StaffUpdate) -> List[StaffMember]:
        """
        Update multiple staff members based on the provided usernames.

        :param cafe_id: The UUID of the cafe.
        :param usernames: A list of usernames of the staff members to update.
        :param staff_data: The data to update the staff members with.
        :return: A list of updated StaffMember objects.
        """
        cafe = await Cafe.find_one({"_id": cafe_id})
        if not cafe:
            raise ValueError("Cafe not found")

        updated_members = []
        for member in cafe.staff:
            if member.username in usernames:
                for key, value in staff_data.model_dump(exclude_unset=True).items():
                    setattr(member, key, value)
                updated_members.append(member)

        if not updated_members:
            raise ValueError("No staff members found for the provided usernames")

        await cafe.save()
        return updated_members

    @staticmethod
    async def delete_many_staff_members(cafe_id: UUID, usernames: List[str]) -> None:
        """
        Delete multiple staff members based on the provided usernames.

        :param cafe_id: The UUID of the cafe.
        :param usernames: A list of usernames of the staff members to delete.
        :return: None
        """
        cafe = await Cafe.find_one({"_id": cafe_id})
        if not cafe:
            raise ValueError("Cafe not found")

        # Filter out the staff members whose usernames are not in the provided list
        cafe.staff = [member for member in cafe.staff if member.username not in usernames]
        await cafe.save()

    # --------------------------------------
    #               Authorization
    # --------------------------------------

    @staticmethod
    async def is_authorized_for_cafe_action(
        cafe_id: UUID, current_user: User, required_roles: List[Role]
    ):
        cafe = await Cafe.find_one({"_id": cafe_id})
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
