"""
Module for handling event-related operations.
"""

from typing import List, Literal, Optional, Union, overload

from beanie import PydanticObjectId
from beanie.odm.queries.find import AggregationQuery, FindMany
from pymongo import ASCENDING, DESCENDING

from app.event.models import Event, EventCreate, EventUpdate
from app.service import set_attributes
from app.user.models import User


class EventService:
    """Service class for Event operations."""

    @overload
    @staticmethod
    async def get_all(
        to_list: Literal[True] = True,
        aggregate: Literal[False] = False,
        current_user_id: Optional[PydanticObjectId] = None,
        **filters: dict,
    ) -> List[Event]: ...

    @overload
    @staticmethod
    async def get_all(
        to_list: Literal[False] = False,
        aggregate: Literal[False] = False,
        current_user_id: Optional[PydanticObjectId] = None,
        **filters: dict,
    ) -> FindMany[Event]: ...

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
    ) -> Union[List[Event], FindMany[Event], List[dict], AggregationQuery[dict]]:
        """Get events."""
        sort_by = filters.pop("sort_by", "-start_date")

        if aggregate:
            pipeline = EventService._build_pipeline(
                filters=filters,
                sort_by=sort_by,
                current_user_id=current_user_id,
            )
            query = Event.aggregate(pipeline)
            return await query.to_list() if to_list else query
        else:
            query = Event.find(filters).sort(sort_by)
            return await query.to_list() if to_list else query

    @staticmethod
    async def get_all_for_user(
        to_list: bool = True,
        aggregate: bool = False,
        current_user_id: PydanticObjectId = None,
        **filters: dict,
    ) -> Union[List[Event], FindMany[Event], List[dict], AggregationQuery[dict]]:
        """Get all events where user is creator or editor."""
        sort_by = filters.pop("sort_by", "-start_date")

        user_filter = {
            "$or": [
                {"creator_id": current_user_id},
            ]
        }

        # Merge with additional filters if needed
        final_filter = {**user_filter, **filters}

        if aggregate:
            pipeline = EventService._build_pipeline(
                filters=user_filter,
                sort_by=sort_by,
                current_user_id=current_user_id,
            )
            query = Event.aggregate(pipeline)
            return await query.to_list() if to_list else query
        else:
            query = Event.find(final_filter).sort(sort_by)
            return await query.to_list() if to_list else query

    @overload
    @staticmethod
    async def get(
        id: PydanticObjectId,
        aggregate: Literal[False] = False,
        current_user_id: Optional[PydanticObjectId] = None,
    ) -> Optional[Event]: ...

    @overload
    @staticmethod
    async def get(
        id: PydanticObjectId,
        aggregate: Literal[True] = True,
        current_user_id: Optional[PydanticObjectId] = None,
    ) -> Optional[dict]: ...

    @staticmethod
    async def get(
        id: PydanticObjectId,
        aggregate: bool = False,
        current_user_id: Optional[PydanticObjectId] = None,
    ) -> Union[Optional[Event], Optional[dict]]:
        """Get an event by ID."""
        if not aggregate:
            return await Event.get(id)

        pipeline = EventService._build_pipeline(event_id=id)
        result = await Event.aggregate(pipeline).to_list()
        return result[0] if result else None

    @overload
    @staticmethod
    async def get_by_id_and_cafe_id(
        id: PydanticObjectId,
        cafe_id: PydanticObjectId,
        aggregate: Literal[False] = False,
    ) -> Optional[Event]: ...

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
    ) -> Union[Optional[Event], Optional[dict]]:
        """Get an event by ID and cafe ID."""
        if not aggregate:
            return await Event.find_one({"_id": id, "cafe_id": cafe_id})

        pipeline = EventService._build_pipeline(filters={"_id": id, "cafe_id": cafe_id})
        result = await Event.aggregate(pipeline).to_list()
        return result[0] if result else None

    @staticmethod
    async def create(
        current_user: User,
        data: EventCreate,
    ) -> Event:
        """Create an event."""
        event = Event(**data.model_dump(), creator_id=current_user.id)
        await event.insert()
        return event

    @staticmethod
    async def update(
        event: Event,
        data: EventUpdate,
    ) -> Event:
        """Update an event."""
        set_attributes(event, data)
        await event.save()
        return event

    @staticmethod
    async def delete(event: Event) -> None:
        """Delete an event."""
        await event.delete()
        return event

    @staticmethod
    def _build_pipeline(
        filters: Optional[dict] = None,
        sort_by: Optional[str] = None,
        event_id: Optional[PydanticObjectId] = None,
        current_user_id: Optional[PydanticObjectId] = None,
    ) -> list:
        """Build aggregation pipeline."""
        pipeline = []
        filters = filters or {}

        if event_id:
            pipeline.append({"$match": {"_id": event_id}})
        elif filters:
            pipeline.append({"$match": filters})

        # Cafes lookup
        pipeline.extend(
            [
                {
                    "$lookup": {
                        "from": "cafes",
                        "localField": "cafe_ids",
                        "foreignField": "_id",
                        "pipeline": [
                            {
                                "$project": {
                                    "_id": 0,
                                    "id": "$_id",
                                    "name": 1,
                                    "slug": 1,
                                    "logo_url": 1,
                                    "banner_url": 1,
                                }
                            }
                        ],
                        "as": "cafes",
                    }
                },
            ]
        )

        # Creator lookup
        pipeline.extend(
            [
                {
                    "$lookup": {
                        "from": "users",
                        "localField": "creator_id",
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
                        "as": "creator",
                    }
                },
                {"$addFields": {"creator": {"$arrayElemAt": ["$creator", 0]}}},
            ]
        )
        # Editors lookup
        pipeline.extend(
            [
                {
                    "$lookup": {
                        "from": "users",
                        "localField": "editor_ids",
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
                        "as": "editors",
                    }
                }
            ]
        )

        # Interaction
        pipeline.extend(
            [
                {
                    "$lookup": {
                        "from": "interactions",
                        "localField": "_id",
                        "foreignField": "event_id",
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
                {"$unset": ["_id", "cafe_ids", "creator_id", "all_interactions"]},
            ]
        )

        # Sorting
        if sort_by and not event_id:
            direction = DESCENDING if sort_by.startswith("-") else ASCENDING
            field = sort_by.lstrip("-")
            pipeline.append({"$sort": {field: direction}})

        return pipeline
