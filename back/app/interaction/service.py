"""
Module for handling interaction-related operations.
"""

from typing import Any, Dict, List, Union

from beanie import PydanticObjectId
from beanie.odm.queries.find import AggregationQuery

from app.cafe.announcement.models import Announcement
from app.cafe.event.models import Event
from app.cafe.menu.item.models import MenuItem
from app.interaction.models import (
    AnnouncementInteraction,
    EventInteraction,
    Interaction,
    InteractionType,
    ItemInteraction,
)
from app.user.models import User


class InteractionService:
    """Service for handling interaction-related operations."""

    @staticmethod
    async def get_all(
        to_list: bool = True,
        **filters: dict,
    ) -> Union[AggregationQuery[List[Dict[str, Any]]], List[Dict[str, Any]]]:
        """Get users who interacted using a single aggregation query."""
        pipeline = [
            {"$match": filters},
            {
                "$lookup": {
                    "from": "users",
                    "localField": "user_id",
                    "foreignField": "_id",
                    "as": "user",
                }
            },
            {"$unwind": "$user"},
            {"$group": {"_id": "$user._id", "user": {"$first": "$user"}}},
            {"$replaceRoot": {"newRoot": "$user"}},
            {
                "$project": {
                    "id": {"$toString": "$_id"},
                    "username": 1,
                    "email": 1,
                    "matricule": 1,
                    "first_name": 1,
                    "last_name": 1,
                    "photo_url": 1,
                    "_id": 0,
                }
            },
        ]

        query = Interaction.aggregate(pipeline)
        return await query.to_list() if to_list else query

    @staticmethod
    async def get(
        user: User,
        type: InteractionType,
        item: MenuItem = None,
        event: Event = None,
        announcement: Announcement = None,
    ) -> Interaction:
        """Get an interaction."""
        if item:
            return await ItemInteraction.find_one(
                {"user_id": user.id, "item_id": item.id, "type": type}
            )
        if announcement:
            return await AnnouncementInteraction.find_one(
                {"user_id": user.id, "announcement_id": announcement.id, "type": type}
            )
        if event:
            return await EventInteraction.find_one(
                {"user_id": user.id, "event_id": event.id, "type": type}
            )
        return None

    @staticmethod
    async def create(
        user: User,
        type: InteractionType,
        item: MenuItem = None,
        event: Event = None,
        announcement: Announcement = None,
    ) -> None:
        """Create an interaction."""
        if item:
            await InteractionService._handle_mutual_exclusivity(
                user,
                item.id,
                ItemInteraction,
                "item_id",
                type,
            )

            interaction = ItemInteraction(
                user_id=user.id,
                item_id=item.id,
                type=type,
            )
            await interaction.insert()
        if announcement:
            await InteractionService._handle_mutual_exclusivity(
                user,
                announcement.id,
                AnnouncementInteraction,
                "announcement_id",
                type,
            )

            interaction = AnnouncementInteraction(
                user_id=user.id,
                announcement_id=announcement.id,
                type=type,
            )
            await interaction.insert()
        if event:
            await InteractionService._handle_mutual_exclusivity(
                user,
                event.id,
                EventInteraction,
                "event_id",
                type,
            )

            interaction = EventInteraction(
                user_id=user.id,
                event_id=event.id,
                type=type,
            )
            await interaction.insert()

    @staticmethod
    async def delete(interaction: Interaction) -> None:
        """Delete an interaction."""
        await interaction.delete()

    @staticmethod
    async def _get_opposite_type(
        interaction_type: InteractionType,
    ) -> Union[InteractionType, None]:
        """Get mutually exclusive opposite reaction type."""
        return {
            InteractionType.LIKE: InteractionType.DISLIKE,
            InteractionType.DISLIKE: InteractionType.LIKE,
        }.get(interaction_type)

    @staticmethod
    async def _handle_mutual_exclusivity(
        user: User,
        entity_id: PydanticObjectId,
        model: type[Interaction],
        id_field: str,
        interaction_type: InteractionType,
    ) -> None:
        """Handle mutually exclusive reactions."""
        opposite_type = await InteractionService._get_opposite_type(interaction_type)

        if opposite_type:
            opposite_interaction = await model.find_one(
                {id_field: entity_id, "user_id": user.id, "type": opposite_type}
            )
            if opposite_interaction:
                await opposite_interaction.delete()
