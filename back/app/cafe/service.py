"""
Module for handling cafe-related operations.
"""

from typing import List, Literal, Optional, Union, overload

from beanie import PydanticObjectId
from beanie.odm.queries.find import FindMany
from bson.errors import InvalidId
from pymongo import ASCENDING, DESCENDING

from app.menu.models import MenuUpdate
from app.cafe.models import Cafe, CafeCreate, CafeUpdate
from app.service import set_attributes


class CafeService:
    """Service for CRUD operations and search on Cafe."""

    @staticmethod
    async def get_all(
        to_list: bool = True,
        **filters: dict,
    ) -> Union[FindMany[Cafe], List[Cafe]]:
        """Get cafes."""
        sort_by = filters.pop("sort_by", "name")
        query = Cafe.find(filters).sort(sort_by)
        return await query.to_list() if to_list else query

    @overload
    @staticmethod
    async def get(
        cafe_slug_or_id: str,
        aggregate: Literal[False] = False,
        current_user_id: Optional[PydanticObjectId] = None,
    ) -> Optional[Cafe]: ...

    @overload
    @staticmethod
    async def get(
        cafe_slug_or_id: str,
        aggregate: Literal[True] = True,
        current_user_id: Optional[PydanticObjectId] = None,
    ) -> Optional[dict]: ...

    @staticmethod
    async def get(
        cafe_slug_or_id: str,
        aggregate: bool = False,
        current_user_id: Optional[PydanticObjectId] = None,
    ) -> Union[Optional[Cafe], Optional[dict]]:
        """Get a cafe by slug or ID."""
        if not aggregate:
            try:
                cafe_id = PydanticObjectId(cafe_slug_or_id)
                return await Cafe.find_one({"_id": cafe_id})
            except InvalidId:
                return await Cafe.find_one(
                    {
                        "$or": [
                            {"slug": cafe_slug_or_id},
                            {"previous_slugs": cafe_slug_or_id},
                        ]
                    }
                )

        try:
            cafe_id = PydanticObjectId(cafe_slug_or_id)
            filters = {"_id": cafe_id}
        except InvalidId:
            filters = {
                "$or": [{"slug": cafe_slug_or_id}, {"previous_slugs": cafe_slug_or_id}]
            }

        pipeline = CafeService._build_pipeline(
            filters=filters, current_user_id=current_user_id
        )
        result = await Cafe.aggregate(pipeline).to_list()
        return result[0] if result else None

    @staticmethod
    async def create(
        data: CafeCreate,
        owner_id: PydanticObjectId,
    ) -> Cafe:
        """Create a new cafe."""
        cafe = Cafe(**data.model_dump(), owner_id=owner_id)
        return await cafe.insert()

    @staticmethod
    async def update(
        cafe: Cafe,
        data: CafeUpdate,
    ) -> Cafe:
        """Update a cafe."""
        set_attributes(cafe, data)
        await cafe.save()
        return cafe

    @staticmethod
    async def update_menu(cafe: Cafe, data: MenuUpdate) -> Cafe:
        """Update a cafe menu."""
        cafe.menu.layout = data.layout
        await cafe.save()

    @staticmethod
    def _build_pipeline(
        filters: Optional[dict] = None,
        sort_by: Optional[str] = None,
        current_user_id: Optional[PydanticObjectId] = None,
    ) -> list:
        """Build aggregation pipeline."""
        pipeline = []
        filters = filters or {}

        if filters:
            pipeline.append({"$match": filters})

        pipeline.extend(
            [
                # Lookup owner
                {
                    "$lookup": {
                        "from": "users",
                        "localField": "owner_id",
                        "foreignField": "_id",
                        "pipeline": [
                            {
                                "$project": {
                                    "_id": 0,
                                    "id": "$_id",
                                    "username": 1,
                                    "email": 1,
                                    "matricule": 1,
                                    "first_name": 1,
                                    "last_name": 1,
                                    "photo_url": 1,
                                }
                            }
                        ],
                        "as": "owner",
                    }
                },
                # Lookup items
                {
                    "$lookup": {
                        "from": "items",
                        "localField": "_id",
                        "foreignField": "cafe_id",
                        "as": "menu_items",
                    }
                },
                # Lookup interactions
                {
                    "$lookup": {
                        "from": "interactions",
                        "localField": "menu_items._id",
                        "foreignField": "item_id",
                        "as": "all_item_interactions",
                    }
                },
                # Lookup admins
                {
                    "$lookup": {
                        "from": "users",
                        "localField": "staff.admin_ids",
                        "foreignField": "_id",
                        "pipeline": [
                            {
                                "$project": {
                                    "_id": 0,
                                    "id": "$_id",
                                    "username": 1,
                                    "email": 1,
                                    "matricule": 1,
                                    "first_name": 1,
                                    "last_name": 1,
                                    "photo_url": 1,
                                }
                            }
                        ],
                        "as": "admins",
                    }
                },
                # Lookup volunteers
                {
                    "$lookup": {
                        "from": "users",
                        "localField": "staff.volunteer_ids",
                        "foreignField": "_id",
                        "pipeline": [
                            {
                                "$project": {
                                    "_id": 0,
                                    "id": "$_id",
                                    "username": 1,
                                    "email": 1,
                                    "matricule": 1,
                                    "first_name": 1,
                                    "last_name": 1,
                                    "photo_url": 1,
                                }
                            }
                        ],
                        "as": "volunteers",
                    }
                },
                # Add owner, menu, and staff
                {
                    "$addFields": {
                        "owner": {"$arrayElemAt": ["$owner", 0]},
                        "staff": {"admins": "$admins", "volunteers": "$volunteers"},
                        "menu": {
                            "layout": "$menu.layout",
                            "categories": {
                                "$concatArrays": [
                                    # Group uncategorized items in General by default
                                    {
                                        "$cond": [
                                            # Check if there are uncategorized items
                                            {
                                                "$gt": [
                                                    {
                                                        "$size": {
                                                            "$filter": {
                                                                "input": "$menu_items",
                                                                "as": "item",
                                                                "cond": {
                                                                    "$eq": [
                                                                        {
                                                                            "$size": "$$item.category_ids"
                                                                        },
                                                                        0,
                                                                    ]
                                                                },
                                                            }
                                                        }
                                                    },
                                                    0,
                                                ]
                                            },
                                            # If true: Add "General" category
                                            [
                                                {
                                                    "id": None,
                                                    "name": "General",
                                                    "description": None,
                                                    "items": {
                                                        "$map": {
                                                            "input": {
                                                                "$filter": {
                                                                    "input": "$menu_items",
                                                                    "as": "item",
                                                                    "cond": {
                                                                        "$eq": [
                                                                            {
                                                                                "$size": "$$item.category_ids"
                                                                            },
                                                                            0,
                                                                        ]
                                                                    },
                                                                }
                                                            },
                                                            "as": "item",
                                                            "in": {
                                                                "id": "$$item._id",
                                                                "name": "$$item.name",
                                                                "description": "$$item.description",
                                                                "tags": "$$item.tags",
                                                                "image_url": "$$item.image_url",
                                                                "price": "$$item.price",
                                                                "in_stock": "$$item.in_stock",
                                                                "options": "$$item.options",
                                                                "interactions": {
                                                                    "$let": {
                                                                        "vars": {
                                                                            "item_interactions": {
                                                                                "$filter": {
                                                                                    "input": "$all_item_interactions",
                                                                                    "cond": {
                                                                                        "$eq": [
                                                                                            "$$this.item_id",
                                                                                            "$$item._id",
                                                                                        ]
                                                                                    },
                                                                                }
                                                                            }
                                                                        },
                                                                        "in": {
                                                                            "$map": {
                                                                                "input": {
                                                                                    "$setUnion": "$$item_interactions.type"
                                                                                },
                                                                                "as": "type",
                                                                                "in": {
                                                                                    "type": "$$type",
                                                                                    "count": {
                                                                                        "$size": {
                                                                                            "$filter": {
                                                                                                "input": "$$item_interactions",
                                                                                                "cond": {
                                                                                                    "$eq": [
                                                                                                        "$$this.type",
                                                                                                        "$$type",
                                                                                                    ]
                                                                                                },
                                                                                            }
                                                                                        }
                                                                                    },
                                                                                    "me": {
                                                                                        "$cond": [
                                                                                            {
                                                                                                "$ifNull": [
                                                                                                    current_user_id,
                                                                                                    False,
                                                                                                ]
                                                                                            },
                                                                                            {
                                                                                                "$in": [
                                                                                                    current_user_id,
                                                                                                    {
                                                                                                        "$map": {
                                                                                                            "input": {
                                                                                                                "$filter": {
                                                                                                                    "input": "$$item_interactions",
                                                                                                                    "cond": {
                                                                                                                        "$eq": [
                                                                                                                            "$$this.type",
                                                                                                                            "$$type",
                                                                                                                        ]
                                                                                                                    },
                                                                                                                }
                                                                                                            },
                                                                                                            "in": "$$this.user_id",
                                                                                                        }
                                                                                                    },
                                                                                                ]
                                                                                            },
                                                                                            False,
                                                                                        ]
                                                                                    },
                                                                                },
                                                                            }
                                                                        },
                                                                    }
                                                                },
                                                            },
                                                        }
                                                    },
                                                }
                                            ],
                                            # If false: Return empty array (no "General" category)
                                            [],
                                        ]
                                    },
                                    # Group categorized items
                                    {
                                        "$map": {
                                            "input": "$menu.categories",
                                            "as": "cat",
                                            "in": {
                                                "id": "$$cat._id",
                                                "name": "$$cat.name",
                                                "description": "$$cat.description",
                                                "items": {
                                                    "$map": {
                                                        "input": {
                                                            "$filter": {
                                                                "input": "$menu_items",
                                                                "as": "item",
                                                                "cond": {
                                                                    "$in": [
                                                                        "$$cat._id",
                                                                        "$$item.category_ids",
                                                                    ]
                                                                },
                                                            }
                                                        },
                                                        "as": "item",
                                                        "in": {
                                                            "id": "$$item._id",
                                                            "name": "$$item.name",
                                                            "description": "$$item.description",
                                                            "tags": "$$item.tags",
                                                            "image_url": "$$item.image_url",
                                                            "price": "$$item.price",
                                                            "in_stock": "$$item.in_stock",
                                                            "options": "$$item.options",
                                                            "interactions": {
                                                                "$let": {
                                                                    "vars": {
                                                                        "item_interactions": {
                                                                            "$filter": {
                                                                                "input": "$all_item_interactions",
                                                                                "cond": {
                                                                                    "$eq": [
                                                                                        "$$this.item_id",
                                                                                        "$$item._id",
                                                                                    ]
                                                                                },
                                                                            }
                                                                        }
                                                                    },
                                                                    "in": {
                                                                        "$map": {
                                                                            "input": {
                                                                                "$setUnion": "$$item_interactions.type"
                                                                            },
                                                                            "as": "type",
                                                                            "in": {
                                                                                "type": "$$type",
                                                                                "count": {
                                                                                    "$size": {
                                                                                        "$filter": {
                                                                                            "input": "$$item_interactions",
                                                                                            "cond": {
                                                                                                "$eq": [
                                                                                                    "$$this.type",
                                                                                                    "$$type",
                                                                                                ]
                                                                                            },
                                                                                        }
                                                                                    }
                                                                                },
                                                                                "me": {
                                                                                    "$cond": [
                                                                                        {
                                                                                            "$ifNull": [
                                                                                                current_user_id,
                                                                                                False,
                                                                                            ]
                                                                                        },
                                                                                        {
                                                                                            "$in": [
                                                                                                current_user_id,
                                                                                                {
                                                                                                    "$map": {
                                                                                                        "input": {
                                                                                                            "$filter": {
                                                                                                                "input": "$$item_interactions",
                                                                                                                "cond": {
                                                                                                                    "$eq": [
                                                                                                                        "$$this.type",
                                                                                                                        "$$type",
                                                                                                                    ]
                                                                                                                },
                                                                                                            }
                                                                                                        },
                                                                                                        "in": "$$this.user_id",
                                                                                                    }
                                                                                                },
                                                                                            ]
                                                                                        },
                                                                                        False,
                                                                                    ]
                                                                                },
                                                                            },
                                                                        }
                                                                    },
                                                                }
                                                            },
                                                        },
                                                    }
                                                },
                                            },
                                        }
                                    },
                                ]
                            },
                        },
                    }
                },
                {"$addFields": {"id": "$_id"}},
                # Clean up temporary fields
                {
                    "$unset": [
                        "_id",
                        "owner_id",
                        "menu_items",
                        "admins",
                        "volunteers",
                        "staff.admin_ids",
                        "staff.volunteer_ids",
                        "all_item_interactions",
                    ]
                },
            ]
        )

        # Sorting
        if sort_by:
            direction = DESCENDING if sort_by.startswith("-") else ASCENDING
            field = sort_by.lstrip("-")
            pipeline.append({"$sort": {field: direction}})

        return pipeline
