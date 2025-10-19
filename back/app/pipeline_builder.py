from typing import Any, Dict, List, Optional, Set, Type, Union
from beanie import PydanticObjectId
from pydantic import BaseModel


class PipelineBuilder:
    def __init__(
        self,
        model: Type[BaseModel],
        root_fields: Optional[Set[str]] = None,
        joined_prefix: str = "joined",  # used for $lookup alias
        lookup_from: Optional[str] = None,
        local_field: Optional[str] = None,
        foreign_field: Optional[str] = "_id",
    ):
        self.model = model
        self.root_fields = root_fields or set()
        self.joined_prefix = joined_prefix
        self.lookup_from = lookup_from
        self.local_field = local_field
        self.foreign_field = foreign_field

    def build_lookup(self) -> Dict[str, Any]:
        if not self.lookup_from or not self.local_field:
            return {}

        return {
            "$lookup": {
                "from": self.lookup_from,
                "localField": self.local_field,
                "foreignField": self.foreign_field,
                "as": self.joined_prefix
            }
        }

    def unwind_joined(self) -> Dict[str, Any]:
        return {"$unwind": f"${self.joined_prefix}"}

    def build_project(self) -> Dict[str, Any]:
        projection: Dict[str, Any] = {}
        for field in self.model.__annotations__:
            if field in self.root_fields:
                projection[field] = 1
            else:
                projection[field] = f"${self.joined_prefix}.{field}"
        return {"$project": projection}

    def build_match(self, filters: Dict[str, Any]) -> Dict[str, Any]:
        return {"$match": filters}

    def build_sort(self, field: str, ascending: bool = True) -> Dict[str, Any]:
        return {"$sort": {field: 1 if ascending else -1}}

    def build_paginate(self, skip: int = 0, limit: int = 20) -> List[Dict[str, Any]]:
        return [{"$skip": skip}, {"$limit": limit}]

    def build_pipeline(
        self,
        filters: Optional[Dict[str, Any]] = None,
        sort_field: str = "created_at",
        ascending: bool = False,
        skip: int = 0,
        limit: int = 20,
        include_lookup: bool = True
    ) -> List[Dict[str, Any]]:
        pipeline: List[Dict[str, Any]] = []

        if include_lookup and self.lookup_from:
            pipeline.append(self.build_lookup())
            pipeline.append(self.unwind_joined())

        if filters:
            pipeline.append(self.build_match(filters))

        pipeline.append(self.build_sort(sort_field, ascending))
        pipeline.append(self.build_project())
        pipeline.extend(self.build_paginate(skip, limit))

        return pipeline
