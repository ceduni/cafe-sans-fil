"""
Module for handling user-related operations.
"""

from typing import List, Optional

from beanie import PydanticObjectId

from app.auth.security import get_password
from app.cafe.models import Cafe
from app.user.models import User, UserCreate, UserUpdate


class UserService:
    """Service class for User and Auth operations."""

    @staticmethod
    async def get_all(**filters: dict):
        """Get users."""
        sort_by = filters.pop("sort_by", "last_name")
        filters["is_active"] = True

        if "hashed_password" in filters:
            filters["hashed_password"] = None

        return User.find(filters).sort(sort_by)

    @staticmethod
    async def get_by_email(email: str) -> Optional[User]:
        """Get a user by email."""
        user = await User.find_one({"email": email, "is_active": True})
        return user

    @staticmethod
    async def get_by_id(id: PydanticObjectId) -> Optional[User]:
        """Get a user by id."""
        user = await User.find_one({"_id": id, "is_active": True})
        return user

    @staticmethod
    async def get_by_username(username: str) -> Optional[User]:
        """Get a user by username."""
        user = await User.find_one({"username": username, "is_active": True})
        return user

    @staticmethod
    async def get(username: str):
        """Get a user."""
        return await User.find_one({"username": username, "is_active": True})

    @staticmethod
    async def create(data: UserCreate):
        """Create a new user."""
        user_in = User(
            email=data.email,
            matricule=data.matricule,
            username=data.username,
            hashed_password=get_password(data.password),
            first_name=data.first_name,
            last_name=data.last_name,
            photo_url=data.photo_url,
        )
        await user_in.insert()
        return user_in

    @staticmethod
    async def update(username: str, data: UserUpdate) -> User:
        """Update a user by username."""
        user = await UserService.get(username)
        update_data = data.model_dump(exclude_unset=True)

        if "password" in update_data:
            update_data["hashed_password"] = get_password(update_data["password"])
            del update_data["password"]

        await user.update({"$set": update_data})
        return user

    @staticmethod
    async def delete(username: str):
        """Delete a user by username."""
        user = await UserService.get(username)

        if user:
            await Cafe.find({"staff.username": username}).update(
                {"$pull": {"staff": {"username": username}}}
            )
            await user.update({"$set": {"is_active": False}})

        return user

    @staticmethod
    async def create_many(datas: List[UserCreate]) -> List[User]:
        """Create multiple users."""
        users = []
        for data in datas:
            user = User(
                email=data.email,
                matricule=data.matricule,
                username=data.username,
                hashed_password=get_password(data.password),
                first_name=data.first_name,
                last_name=data.last_name,
                photo_url=data.photo_url,
            )
            users.append(user)

        await User.insert_many(users)
        return users

    @staticmethod
    async def update_many(usernames: List[str], data: UserUpdate) -> List[User]:
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
    async def delete_many(usernames: List[str]) -> None:
        """Delete multiple users based on the provided list of usernames."""
        users_to_delete = await User.find_many(
            {"username": {"$in": usernames}}
        ).to_list()
        if not users_to_delete:
            raise ValueError("No users found for the provided usernames")

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
