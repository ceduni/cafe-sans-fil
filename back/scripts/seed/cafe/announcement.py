"""
Announcement seeder module.
"""

import json
import os
import random
from datetime import UTC, datetime, timedelta
from typing import List

from beanie import PydanticObjectId
from faker import Faker
from tqdm import tqdm

from app.cafe.announcement.models import Announcement, AnnouncementCreate
from app.cafe.models import Cafe
from app.cafe.service import CafeService

random.seed(42)
fake = Faker("fr_FR")


class AnnouncementSeeder:
    """Announcement seeder class."""

    def __init__(self):
        self.announcements: List[Announcement] = []
        self.data = self._load_data()

    def _load_data(self):
        path = os.path.join(
            os.getcwd(), "scripts", "seed", "data", "announcements.json"
        )
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)

    async def seed_announcements(self, num_per_cafe: int = 10) -> None:
        """Seed announcements for all cafes."""
        cafes: List[Cafe] = await CafeService.get_all()

        for cafe in tqdm(cafes, desc="Seeding announcements"):
            # Get random staff members from this cafe
            admin_ids: List[PydanticObjectId] = cafe.staff.admin_ids
            if not admin_ids:
                continue

            for _ in range(num_per_cafe):
                author_id = random.choice(admin_ids)
                announcement = await self._create_announcement(cafe, author_id)
                self.announcements.append(announcement)

        await Announcement.insert_many(self.announcements)
        print(f"Created {len(self.announcements)} announcements")

    async def _create_announcement(
        self, cafe: Cafe, author_id: PydanticObjectId
    ) -> Announcement:
        """Create a single announcement instance."""
        data: dict = await self._random_announcement_data()

        return Announcement(
            **AnnouncementCreate(**data).model_dump(),
            cafe_id=cafe.id,
            author_id=author_id,
            created_at=datetime.now(UTC) - timedelta(days=random.randint(0, 30)),
            updated_at=datetime.now(UTC) - timedelta(days=random.randint(0, 30)),
        )

    async def _random_announcement_data(self, lang: str = "en") -> dict:
        """Generates random announcement data."""
        data = self.data[lang]
        components = data["title_components"]

        # Build compound title
        title = f"{random.choice(components['prefix'])} {random.choice(components['subject'])} {random.choice(components['suffix'])}"

        # Generate content
        template: str = random.choice(data["content_templates"])
        content = template.format(
            adjective=random.choice(data["adjectives"]),
            subject=random.choice(data["subjects"]),
            event_type=random.choice(["workshop", "tasting", "seminar"]),
            date_context=fake.future_date(end_date="+30d").strftime("%B %d"),
            details=fake.paragraph(nb_sentences=2),
        )

        # Generate active_until
        active_until = datetime.now(UTC) + timedelta(days=random.randint(1, 14))

        # Handle optional tags
        tags = (
            random.sample(data["tags"], k=random.randint(0, 20))
            if random.random() > 0.2
            else []
        )

        return {
            "title": title,
            "content": content,
            "active_until": active_until,
            "tags": tags,
        }
