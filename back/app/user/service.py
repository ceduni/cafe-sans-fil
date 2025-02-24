"""
Module for handling user-related operations.
"""

from typing import List, Optional

from beanie import PydanticObjectId

from app.auth.security import get_password, verify_password
from app.cafe.models import Cafe
from app.user.models import User, UserAuth, UserUpdate


class UserService:
    """Service class for User and Auth operations."""

    # --------------------------------------
    #               Auth
    # --------------------------------------

    @staticmethod
    async def authenticate(credential: str, password: str) -> Optional[User]:
        """Authenticate a user."""
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
        """Get a user by email."""
        user = await User.find_one({"email": email, "is_active": True})
        return user

    @staticmethod
    async def get_user_by_username(username: str) -> Optional[User]:
        """Get a user by username."""
        user = await User.find_one({"username": username, "is_active": True})
        return user

    @staticmethod
    async def get_user_by_id(id: PydanticObjectId) -> Optional[User]:
        """Get a user by id."""
        user = await User.find_one({"_id": id, "is_active": True})
        return user

    # --------------------------------------
    #               User
    # --------------------------------------

    @staticmethod
    async def get_users(**filters: dict):
        """Get users."""
        sort_by = filters.pop("sort_by", "last_name")
        filters["is_active"] = True  # Don't show inactive users

        # Prevent filtering on hashed_password
        if "hashed_password" in filters:
            filters["hashed_password"] = None

        return User.find(filters).sort(sort_by)

    @staticmethod
    async def create_user(user: UserAuth):
        """Create a new user."""
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
    async def get_user(username: str):
        """Get a user by username."""
        return await User.find_one({"username": username, "is_active": True})

    @staticmethod
    async def update_user(username: str, data: UserUpdate) -> User:
        """Update a user by username."""
        user = await UserService.get_user(username)
        update_data = data.model_dump(exclude_unset=True)

        if "password" in update_data:
            update_data["hashed_password"] = get_password(update_data["password"])
            del update_data["password"]

        await user.update({"$set": update_data})
        return user

    @staticmethod
    async def delete_user(username: str):
        """Delete a user by username."""
        user = await UserService.get_user(username)

        if user:
            await Cafe.find({"staff.username": username}).update(
                {"$pull": {"staff": {"username": username}}}
            )
            await user.update({"$set": {"is_active": False}})

        return user

    @staticmethod
    async def create_many_users(users_data: List[UserAuth]) -> List[User]:
        """Create multiple users."""
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
        """Update multiple users based on the provided list of usernames."""
        update_data = data.model_dump(exclude_unset=True)

        if "password" in update_data:
            update_data["hashed_password"] = get_password(update_data["password"])
            del update_data["password"]

        result = await User.find_many({"username": {"$in": usernames}}).update_many(
            {"$set": update_data}
        )
        if result.matched_count == 0:
            raise ValueError("No users found for the provided usernames")

        return await User.find_many({"username": {"$in": usernames}}).to_list()

    @staticmethod
    async def delete_many_users(usernames: List[str]) -> None:
        """Delete multiple users based on the provided list of usernames."""
        users_to_delete = await User.find_many(
            {"username": {"$in": usernames}}
        ).to_list()
        if not users_to_delete:
            raise ValueError("No users found for the provided usernames")

        # Remove users from Cafe staff and deactivate users
        for user in users_to_delete:
            await Cafe.find({"staff.username": user.username}).update(
                {"$pull": {"staff": {"username": user.username}}}
            )
            await user.update({"$set": {"is_active": False}})

    @staticmethod
    async def check_existing_user_attributes(
        email: str, matricule: str, username: str
    ) -> Optional[str]:
        """Check if a user with the provided email, matricule, or username exists."""
        if await User.find_one({"email": email}):
            return "email"
        if await User.find_one({"matricule": matricule}):
            return "matricule"
        if await User.find_one({"username": username}):
            return "username"
        return None

    @staticmethod
    async def reset_password(user: User, new_password: str):
        """Reset a user's password."""
        hashed_password = get_password(new_password)
        await user.update({"$set": {"hashed_password": hashed_password}})
        return user
