"""
Interaction seeder module.
"""

import random
from datetime import UTC, datetime, timedelta
from typing import List

from tqdm import tqdm

from app.cafe.announcement.models import Announcement
from app.cafe.announcement.service import AnnouncementService
from app.cafe.menu.item.models import MenuItem
from app.cafe.menu.item.service import ItemService
from app.event.models import Event
from app.event.service import EventService
from app.interaction.models import (
    AnnouncementInteraction,
    EventInteraction,
    Interaction,
    InteractionType,
    ItemInteraction,
)
from app.user.models import User
from app.user.service import UserService

random.seed(42)


class InteractionSeeder:
    """Interaction seeder class."""

    def __init__(self):
        """Initializes the InteractionSeeder."""
        self.interactions: List = []
        self.users: List[User] = []
        self.items: List[MenuItem] = []
        self.announcements: List[Announcement] = []
        self.events: List[Event] = []

    async def seed_interactions(self):
        """Seed all interaction types."""
        self.users = await UserService.get_all()
        self.items = await ItemService.get_all()
        self.announcements = await AnnouncementService.get_all()
        self.events = await EventService.get_all()

        await self._seed_item_interactions()
        await self._seed_announcement_interactions()
        await self._seed_event_interactions()
        # Split into chunks for bulk insert
        chunk_size = 1000
        for i in range(0, len(self.interactions), chunk_size):
            chunk = self.interactions[i : i + chunk_size]
            await Interaction.insert_many(chunk)

    async def _seed_item_interactions(self):
        """Seed item likes/dislikes."""
        for item in tqdm(self.items, desc="Item Interactions"):
            # 70% chance item has interactions
            if random.random() > 0.3:
                # Get random subset of users
                users = random.sample(
                    self.users,
                    k=random.randint(
                        int(len(self.users) * 0.2), int(len(self.users) * 0.6)
                    ),
                )

                for user in users:
                    # 80% like, 20% dislike
                    interaction_type = random.choices(
                        [InteractionType.LIKE, InteractionType.DISLIKE],
                        weights=[0.8, 0.2],
                    )[0]

                    self.interactions.append(
                        ItemInteraction(
                            user_id=user.id,
                            item_id=item.id,
                            type=interaction_type,
                            created_at=self._random_date(),
                        )
                    )

    async def _seed_announcement_interactions(self):
        """Seed announcement likes/dislikes."""
        for announcement in tqdm(self.announcements, desc="Announcement Interactions"):
            if random.random() > 0.4:  # 60% chance
                users = random.sample(
                    self.users,
                    k=random.randint(
                        int(len(self.users) * 0.1), int(len(self.users) * 0.3)
                    ),
                )

                for user in users:
                    interaction_type = random.choices(
                        [InteractionType.LIKE, InteractionType.DISLIKE],
                        weights=[0.85, 0.15],
                    )[0]

                    self.interactions.append(
                        AnnouncementInteraction(
                            user_id=user.id,
                            announcement_id=announcement.id,
                            type=interaction_type,
                            created_at=self._random_date(),
                        )
                    )

    async def _seed_event_interactions(self):
        """Seed event interactions (attend/support/like)."""
        for event in tqdm(self.events, desc="Event Interactions"):
            if random.random() > 0.2:  # 80% chance
                users = random.sample(
                    self.users,
                    k=random.randint(
                        int(len(self.users) * 0.3), int(len(self.users) * 0.7)
                    ),
                )

                for user in users:
                    # Higher probability for attending
                    interaction_type = random.choices(
                        [
                            InteractionType.ATTEND,
                            InteractionType.SUPPORT,
                            InteractionType.LIKE,
                        ],
                        weights=[0.5, 0.3, 0.2],
                    )[0]

                    self.interactions.append(
                        EventInteraction(
                            user_id=user.id,
                            event_id=event.id,
                            type=interaction_type,
                            created_at=self._random_date(),
                        )
                    )

    def _random_date(self) -> datetime:
        """Generate random date within last 6 months."""
        return datetime.now(UTC) - timedelta(
            days=random.randint(0, 180), hours=random.randint(0, 23)
        )
