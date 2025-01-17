from typing import List, Optional
from uuid import UUID
from app.models.user_model import User
from app.models.cafe_model import Cafe
from app.schemas.user_schema import UserAuth, UserUpdate
from app.core.security import get_password, verify_password


class UserService:
    """
    Service class that provides methods for CRUD operations related to Auth and Users.
    """

    # --------------------------------------
    #               Auth
    # --------------------------------------

    @staticmethod
    async def authenticate(credential: str, password: str) -> Optional[User]:
        if "@" in credential:
            user = await UserService.get_user_by_email(email=credential)
        else:
            user = await UserService.get_user_by_username(username=credential)

        if not user:
            return None
        if not verify_password(password=password, hashed_pass=user.hashed_password):
            return None

        return user

    @staticmethod
    async def get_user_by_email(email: str) -> Optional[User]:
        user = await User.find_one({"email": email, "is_active": True})
        return user

    @staticmethod
    async def get_user_by_username(username: str) -> Optional[User]:
        user = await User.find_one({"username": username, "is_active": True})
        return user

    @staticmethod
    async def get_user_by_id(id: UUID) -> Optional[User]:
        user = await User.find_one({"_id": id, "is_active": True})
        return user

    # --------------------------------------
    #               User
    # --------------------------------------

    @staticmethod
    async def list_users(**filters):
        # Example: http://cafesansfil-api.onrender.com/api/users?sort_by=-last_name
        query_filters = {}
        query_filters["is_active"] = True  # Don't show inactive users

        # Prevent filtering on hashed_password
        if "hashed_password" in filters:
            query_filters["hashed_password"] = None

        page = int(filters.pop("page", 1))
        limit = int(filters.pop("limit", 20))

        # Convert 'is_open' string to boolean
        if "is_open" in filters:
            if filters["is_open"].lower() == "true":
                query_filters["is_open"] = True
            elif filters["is_open"].lower() == "false":
                query_filters["is_open"] = False

        sort_by = filters.pop("sort_by", "last_name")  # Default sort field
        sort_order = -1 if sort_by.startswith("-") else 1
        sort_field = sort_by[1:] if sort_order == -1 else sort_by
        sort_params = [(sort_field, sort_order)]

        users_cursor = User.aggregate(
            [
                {"$match": query_filters},
                {"$sort": dict(sort_params)},
                {"$skip": (page - 1) * limit},
                {"$limit": limit},
            ]
        )

        return await users_cursor.to_list(None)

    @staticmethod
    async def create_user(user: UserAuth):
        user_in = User(
            email=user.email,
            matricule=user.matricule,
            username=user.username,
            hashed_password=get_password(user.password),
            first_name=user.first_name,
            last_name=user.last_name,
            photo_url=user.photo_url,
        )
        await user_in.insert()
        return user_in

    @staticmethod
    async def retrieve_user(username: str):
        # Don't show inactive users
        return await User.find_one({"username": username, "is_active": True})

    @staticmethod
    async def update_user(username: str, data: UserUpdate) -> User:
        user = await UserService.retrieve_user(username)
        update_data = data.model_dump(exclude_unset=True)

        if "password" in update_data:
            update_data["hashed_password"] = get_password(update_data["password"])
            del update_data["password"]

        await user.update({"$set": update_data})
        return user

    @staticmethod
    async def delete_user(username: str):
        user = await UserService.retrieve_user(username)

        if user:
            await Cafe.find({"staff.username": username}).update(
                {"$pull": {"staff": {"username": username}}}
            )
            await user.update({"$set": {"is_active": False}})

        return user

    @staticmethod
    async def create_many_users(users_data: List[UserAuth]) -> List[User]:
        """
        Create multiple users.

        :param users_data: A list of user data to create.
        :return: A list of created User objects.
        """
        users = []
        for user_data in users_data:
            user = User(
                email=user_data.email,
                matricule=user_data.matricule,
                username=user_data.username,
                hashed_password=get_password(user_data.password),
                first_name=user_data.first_name,
                last_name=user_data.last_name,
                photo_url=user_data.photo_url,
            )
            users.append(user)

        await User.insert_many(users)
        return users

    @staticmethod
    async def update_many_users(usernames: List[str], data: UserUpdate) -> List[User]:
        """
        Update multiple users based on the provided list of usernames and data.

        :param usernames: A list of usernames of the users to update.
        :param data: The data to update the users with.
        :return: A list of updated User objects.
        """
        update_data = data.model_dump(exclude_unset=True)

        if "password" in update_data:
            update_data["hashed_password"] = get_password(update_data["password"])
            del update_data["password"]

        result = await User.find_many({"username": {"$in": usernames}}).update_many({"$set": update_data})
        if result.matched_count == 0:
            raise ValueError("No users found for the provided usernames")

        return await User.find_many({"username": {"$in": usernames}}).to_list()

    @staticmethod
    async def delete_many_users(usernames: List[str]) -> None:
        """
        Deactivate multiple users based on the provided list of usernames.

        :param usernames: A list of usernames of the users to delete.
        :return: None
        """
        users_to_delete = await User.find_many({"username": {"$in": usernames}}).to_list()
        if not users_to_delete:
            raise ValueError("No users found for the provided usernames")

        # Remove users from Cafe staff and deactivate users
        for user in users_to_delete:
            await Cafe.find({"staff.username": user.username}).update({"$pull": {"staff": {"username": user.username}}})
            await user.update({"$set": {"is_active": False}})

    @staticmethod
    async def check_existing_user_attributes(
        email: str, matricule: str, username: str
    ) -> Optional[str]:
        if await User.find_one({"email": email}):
            return "email"
        if await User.find_one({"matricule": matricule}):
            return "matricule"
        if await User.find_one({"username": username}):
            return "username"
        return None

    @staticmethod
    async def reset_password(user: User, new_password: str):
        hashed_password = get_password(new_password)
        await user.update({"$set": {"hashed_password": hashed_password}})
        return user
