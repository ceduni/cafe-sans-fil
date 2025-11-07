"""
Module for handling announcement-related operations.
"""

from typing import List, Literal, Optional, Union, overload

from beanie import PydanticObjectId
from beanie.odm.queries.find import AggregationQuery, FindMany
from pymongo import ASCENDING, DESCENDING

from app.cafe.announcement.models import (
    Announcement,
    AnnouncementCreate,
    AnnouncementUpdate,
)
from app.cafe.models import Cafe
from app.service import set_attributes
from app.user.models import User


class AnnouncementService:
    """Service class for announcement operations."""

    @overload
    @staticmethod
    async def get_all(
        to_list: Literal[True] = True,
        aggregate: Literal[False] = False,
        current_user_id: Optional[PydanticObjectId] = None,
        **filters: dict,
    ) -> List[Announcement]: ...

    @overload
    @staticmethod
    async def get_all(
        to_list: Literal[False] = False,
        aggregate: Literal[False] = False,
        current_user_id: Optional[PydanticObjectId] = None,
        **filters: dict,
    ) -> FindMany[Announcement]: ...

    @overload
    @staticmethod
    async def get_all(
        to_list: Literal[True] = True,
        aggregate: Literal[True] = True,
        current_user_id: Optional[PydanticObjectId] = None,
        **filters: dict,
    ) -> List[dict]: ...

    @overload
    @staticmethod
    async def get_all(
        to_list: Literal[False] = False,
        aggregate: Literal[True] = True,
        current_user_id: Optional[PydanticObjectId] = None,
        **filters: dict,
    ) -> AggregationQuery[dict]: ...

    @staticmethod
    async def get_all(
        to_list: bool = True,
        aggregate: bool = False,
        current_user_id: Optional[PydanticObjectId] = None,
        **filters: dict,
    ) -> Union[
        List[Announcement], FindMany[Announcement], List[dict], AggregationQuery[dict]
    ]:
        """Get announcements."""
        sort_by = filters.pop("sort_by", "-updated_at")

        if aggregate:
            pipeline = AnnouncementService._build_pipeline(
                filters=filters,
                sort_by=sort_by,
                current_user_id=current_user_id,
            )
            query = Announcement.aggregate(pipeline)
            return await query.to_list() if to_list else query
        else:
            query = Announcement.find(filters).sort(sort_by)
            return await query.to_list() if to_list else query

    @overload
    @staticmethod
    async def get(
        id: PydanticObjectId,
        aggregate: Literal[False] = False,
    ) -> Optional[Announcement]: ...

    @overload
    @staticmethod
    async def get(
        id: PydanticObjectId,
        aggregate: Literal[True] = True,
    ) -> Optional[dict]: ...

    @staticmethod
    async def get(
        id: PydanticObjectId,
        aggregate: bool = False,
    ) -> Union[Optional[Announcement], Optional[dict]]:
        """Get an announcement by ID."""
        if not aggregate:
            return await Announcement.get(id)

        pipeline = AnnouncementService._build_pipeline(announcement_id=id)
        result = await Announcement.aggregate(pipeline).to_list()
        return result[0] if result else None

    @overload
    @staticmethod
    async def get_by_id_and_cafe_id(
        id: PydanticObjectId,
        cafe_id: PydanticObjectId,
        aggregate: Literal[False] = False,
    ) -> Optional[Announcement]: ...

    @overload
    @staticmethod
    async def get_by_id_and_cafe_id(
        id: PydanticObjectId,
        cafe_id: PydanticObjectId,
        aggregate: Literal[True] = True,
    ) -> Optional[dict]: ...

    @staticmethod
    async def get_by_id_and_cafe_id(
        id: PydanticObjectId,
        cafe_id: PydanticObjectId,
        aggregate: bool = False,
    ) -> Union[Optional[Announcement], Optional[dict]]:
        """Get an announcement by ID and cafe ID."""
        if not aggregate:
            return await Announcement.find_one({"_id": id, "cafe_id": cafe_id})

        pipeline = AnnouncementService._build_pipeline(
            filters={"_id": id, "cafe_id": cafe_id}
        )
        result = await Announcement.aggregate(pipeline).to_list()
        return result[0] if result else None

    @staticmethod
    async def create(
        current_user: User,
        cafe: Cafe,
        data: AnnouncementCreate,
    ) -> Announcement:
        """Create an announcement."""
        announcement = Announcement(
            **data.model_dump(), cafe_id=cafe.id, author_id=current_user.id
        )
        await announcement.insert()
        return announcement

    @staticmethod
    async def update(
        announcement: Announcement,
        data: AnnouncementUpdate,
    ) -> Announcement:
        """Update an announcement."""
        set_attributes(announcement, data)
        await announcement.save()
        return announcement

    @staticmethod
    async def delete(announcement: Announcement) -> None:
        """Delete an announcement."""
        await announcement.delete()

    @staticmethod
    def _build_pipeline(
        filters: Optional[dict] = None,
        sort_by: Optional[str] = None,
        announcement_id: Optional[PydanticObjectId] = None,
        current_user_id: Optional[PydanticObjectId] = None,
    ) -> list:
        """Build aggregation pipeline."""
        pipeline = []
        filters = filters or {}

        # Initial match stage
        if announcement_id:
            pipeline.append({"$match": {"_id": announcement_id}})
        elif filters:
            pipeline.append({"$match": filters})

        # Author lookup
        pipeline.extend(
            [
                {
                    "$lookup": {
                        "from": "users",
                        "localField": "author_id",
                        "foreignField": "_id",
                        "pipeline": [
                            {
                                "$project": {
                                    "_id": 0,
                                    "id": "$_id",
                                    "username": 1,
                                    "email": 1,
                                    "first_name": 1,
                                    "last_name": 1,
                                    "photo_url": 1,
                                }
                            }
                        ],
                        "as": "author",
                    }
                },
                {"$addFields": {"author": {"$arrayElemAt": ["$author", 0]}}},
            ]
        )

        # Interaction
        pipeline.extend(
            [
                {
                    "$lookup": {
                        "from": "interactions",
                        "localField": "_id",
                        "foreignField": "announcement_id",
                        "as": "all_interactions",
                    }
                },
                {
                    "$addFields": {
                        "interactions": {
                            "$map": {
                                "input": {"$setUnion": "$all_interactions.type"},
                                "as": "type",
                                "in": {
                                    "type": "$$type",
                                    "count": {
                                        "$size": {
                                            "$filter": {
                                                "input": "$all_interactions",
                                                "as": "ia",
                                                "cond": {
                                                    "$eq": ["$$ia.type", "$$type"]
                                                },
                                            }
                                        }
                                    },
                                    "me": {
                                        "$cond": [
                                            {"$ifNull": [current_user_id, False]},
                                            {
                                                "$anyElementTrue": {
                                                    "$map": {
                                                        "input": "$all_interactions",
                                                        "as": "ia",
                                                        "in": {
                                                            "$and": [
                                                                {
                                                                    "$eq": [
                                                                        "$$ia.user_id",
                                                                        current_user_id,
                                                                    ]
                                                                },
                                                                {
                                                                    "$eq": [
                                                                        "$$ia.type",
                                                                        "$$type",
                                                                    ]
                                                                },
                                                            ]
                                                        },
                                                    }
                                                }
                                            },
                                            False,
                                        ]
                                    },
                                },
                            }
                        }
                    }
                },
            ]
        )

        # Projection
        pipeline.extend(
            [
                {"$addFields": {"id": "$_id"}},
                {"$unset": ["_id", "author_id", "all_interactions"]},
            ]
        )

        # Sorting
        if sort_by and not announcement_id:
            direction = DESCENDING if sort_by.startswith("-") else ASCENDING
            field = sort_by.lstrip("-")
            pipeline.append({"$sort": {field: direction}})

        return pipeline
