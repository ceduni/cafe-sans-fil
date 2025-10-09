"""
Module for handling user-related operations.
"""

from typing import List, Literal, Optional, Union, overload

from beanie import PydanticObjectId
from beanie.odm.queries.find import FindMany
from pymongo import ASCENDING, DESCENDING

from app.auth.security import get_password
from app.cafe.models import Cafe
from app.user.models import User, UserCreate, UserUpdate


class UserService:
    """Service class for User and Auth operations."""

    @staticmethod
    async def get_all(
        to_list: bool = True, **filters: dict
    ) -> Union[FindMany[User], List[User]]:
        """Get users."""
        sort_by = filters.pop("sort_by", "last_name")
        filters["is_active"] = True

        if "hashed_password" in filters:
            filters["hashed_password"] = None

        query = User.find(filters).sort(sort_by)
        return await query.to_list() if to_list else query

    @staticmethod
    async def get_by_email(email: str) -> Optional[User]:
        """Get a user by email."""
        return await User.find_one({"email": email, "is_active": True})

    @overload
    @staticmethod
    async def get_by_id(
        id: PydanticObjectId,
        aggregate: Literal[False] = False,
    ) -> Optional[User]: ...

    @overload
    @staticmethod
    async def get_by_id(
        id: PydanticObjectId,
        aggregate: Literal[True] = True,
    ) -> Optional[dict]: ...

    @staticmethod
    async def get_by_id(
        id: PydanticObjectId,
        aggregate: bool = False,
    ) -> Union[Optional[User], Optional[dict]]:
        """Get a user by id."""
        if not aggregate:
            return await User.find_one({"_id": id, "is_active": True})

        filters = {"_id": id, "is_active": True}
        pipeline = UserService._build_pipeline(filters=filters)
        result = await User.aggregate(pipeline).to_list()
        return result[0] if result else None

    @staticmethod
    async def get_by_username(username: str) -> Optional[User]:
        """Get a user by username."""
        return await User.find_one({"username": username, "is_active": True})

    @staticmethod
    async def get(username: str) -> Optional[User]:
        """Get a user."""
        return await User.find_one({"username": username, "is_active": True})

    @staticmethod
    async def create(data: UserCreate):
        """Create a new user."""
        user = User(
            email=data.email,
            matricule=data.matricule,
            username=data.username,
            hashed_password=get_password(data.password),
            first_name=data.first_name,
            last_name=data.last_name,
            photo_url=data.photo_url,
        )
        await user.insert()
        return user

    @staticmethod
    async def update(user: Union[User, dict], data: UserUpdate) -> User:
        """Update a user."""
        if isinstance(user, dict):
            user_id = user.get("id") or user.get("_id")
            user_obj = await User.get(PydanticObjectId(user_id))
            if not user_obj:
                raise ValueError("User not found")
            user = user_obj
        update_data = data.model_dump(exclude_unset=True)

        if "password" in update_data:
            user.hashed_password = get_password(update_data["password"])
            del update_data["password"]

        for field, value in update_data.items():
            setattr(user, field, value)

        await user.save()
        return user

    @staticmethod
    async def delete(user: User):
        """Delete a user."""
        # TODO: Delete user from cafe
        # if user:
        #     await Cafe.find({"staff.username": username}).update(
        #         {"$pull": {"staff": {"username": username}}}
        #     )
        #     await user.update({"$set": {"is_active": False}})

        user.is_active = False
        await user.save()

    @staticmethod
    async def delete_my_account(user: Union[User, dict]):
        """Delete my user account from the database (hard delete - permanently removes user)."""
        # Handle both User object and dict from aggregate
        if isinstance(user, dict):
            user_id = user.get("id") or user.get("_id")
            user_obj = await User.get(PydanticObjectId(user_id))
            if not user_obj:
                raise ValueError("User not found")
            user = user_obj
        
        # Permanently delete user document from the database
        await user.delete()
    
    @staticmethod
    async def add_cafe(
        user: User,
        cafe: Cafe,
    ) -> None:
        """Add a cafe to a user."""
        if cafe.id in user.cafe_ids:
            return

        user.cafe_ids.append(cafe.id)
        await user.save()

    @staticmethod
    async def remove_cafe(
        user: User,
        cafe: Cafe,
    ) -> None:
        """Remove a cafe from a user."""
        if cafe.id not in user.cafe_ids:
            return

        user.cafe_ids.remove(cafe.id)
        await user.save()

    @staticmethod
    async def create_many(datas: List[UserCreate]) -> List[PydanticObjectId]:
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

        result = await User.insert_many(users)
        return result.inserted_ids

    @staticmethod
    async def update_many(ids: List[PydanticObjectId], data: UserUpdate) -> List[User]:
        update_data = data.model_dump(exclude_unset=True)

        if "password" in update_data:
            update_data["hashed_password"] = get_password(update_data["password"])
            del update_data["password"]

        result = await User.find_many({"_id": {"$in": ids}}).update_many(
            {"$set": update_data}
        )
        if result.matched_count == 0:
            return None

        return await User.find_many({"_id": {"$in": ids}}).to_list()

    @staticmethod
    async def delete_many(ids: List[PydanticObjectId]) -> None:
        users_to_delete = await User.find_many({"_id": {"$in": ids}}).to_list()
        if not users_to_delete:
            return None

        for user in users_to_delete:
            # TODO: Delete user from cafe
            # await Cafe.find({"staff.username": user.username}).update(
            #     {"$pull": {"staff": {"username": user.username}}}
            # )
            await user.update({"$set": {"is_active": False}})

    @staticmethod
    async def check_existing_user_attributes(
        email: str, matricule: str, username: str
    ) -> Optional[str]:
        """Check if a user with the provided email, matricule, or username exists."""
        user = await User.find_one(
            {
                "$or": [
                    {"email": email},
                    {"matricule": matricule},
                    {"username": username},
                ]
            }
        )

        if user:
            if user.email == email:
                return "email"
            if user.matricule == matricule:
                return "matricule"
            if user.username == username:
                return "username"

        return None

    @staticmethod
    def _build_pipeline(
        filters: Optional[dict] = None,
        sort_by: Optional[str] = None,
    ) -> list:
        """Build aggregation pipeline."""
        pipeline = []
        filters = filters or {}

        if filters:
            pipeline.append({"$match": filters})

        pipeline.extend(
            [
                {
                    "$lookup": {
                        "from": "cafes",
                        "localField": "cafe_ids",
                        "foreignField": "_id",
                        "let": {"user_id": "$_id"},
                        "pipeline": [
                            {
                                "$project": {
                                    "_id": 0,
                                    "id": "$_id",
                                    "name": 1,
                                    "slug": 1,
                                    "logo_url": 1,
                                    "banner_url": 1,
                                    "role": {
                                        "$cond": [
                                            {"$eq": ["$owner_id", "$$user_id"]},
                                            "OWNER",
                                            {
                                                "$cond": [
                                                    {
                                                        "$in": [
                                                            "$$user_id",
                                                            "$staff.admin_ids",
                                                        ]
                                                    },
                                                    "ADMIN",
                                                    {
                                                        "$cond": [
                                                            {
                                                                "$in": [
                                                                    "$$user_id",
                                                                    "$staff.volunteer_ids",
                                                                ]
                                                            },
                                                            "VOLUNTEER",
                                                            None,
                                                        ]
                                                    },
                                                ]
                                            },
                                        ]
                                    },
                                }
                            }
                        ],
                        "as": "cafes",
                    }
                },
                # Projection
                {"$addFields": {"id": "$_id"}},
                {"$unset": ["_id", "cafe_ids"]},
            ]
        )

        # Sorting
        if sort_by:
            direction = DESCENDING if sort_by.startswith("-") else ASCENDING
            field = sort_by.lstrip("-")
            pipeline.append({"$sort": {field: direction}})

        return pipeline
