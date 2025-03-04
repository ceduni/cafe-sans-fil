"""
Event seeder module.
"""

import json
import os
import random
from datetime import UTC, datetime, timedelta
from typing import List

from beanie import PydanticObjectId
from tqdm import tqdm

from app.cafe.event.models import Event, EventCreate
from app.cafe.models import Cafe
from app.cafe.service import CafeService

random.seed(42)


class EventSeeder:
    """Event seeder class."""

    def __init__(self):
        """Initializes the EventSeeder."""
        self.events: List[Event] = []
        self.data = self._load_data()

    def _load_data(self):
        """Loads event data from a JSON file."""
        path = os.path.join(os.getcwd(), "scripts", "seed", "data", "events.json")
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)

    async def seed_events(self, num_per_cafe: int = 4) -> None:
        """Seed events for all cafes."""
        cafes: List[Cafe] = await CafeService.get_all()

        for cafe in tqdm(cafes, desc="Events"):
            admin_ids: List[PydanticObjectId] = cafe.staff.admin_ids
            if not admin_ids:
                continue

            for _ in range(num_per_cafe):
                creator_id = random.choice(admin_ids)
                event = await self._create_event(cafe, creator_id)
                self.events.append(event)

        await Event.insert_many(self.events)

    async def _create_event(self, cafe: Cafe, creator_id: PydanticObjectId) -> Event:
        """Create a single event instance."""
        data: dict = await self._random_event_data()

        return Event(
            **EventCreate(**data).model_dump(),
            cafe_id=cafe.id,
            creator_id=creator_id,
            created_at=datetime.now(UTC) - timedelta(days=random.randint(0, 30)),
            updated_at=datetime.now(UTC) - timedelta(days=random.randint(0, 30)),
        )

    async def _random_event_data(self, lang: str = "en") -> dict:
        """Generates random event data."""
        data = self.data[lang]
        components = data["name_components"]
        features = data["features"]

        # Generate compound name
        name = f"{random.choice(components['adjectives'])} {random.choice(components['types'])} {random.choice(components['formats'])}"

        # Generate description
        template: str = random.choice(data["description_templates"])
        description = (
            template.format(
                activity=random.choice(features["activities"]),
                featured_item=random.choice(features["items"]),
                skill=random.choice(["brewing", "extraction", "latte art"]),
                concept=random.choice(features["concepts"]),
            )
            if random.random() > 0.2
            else None
        )

        # Event timing
        start_date = datetime.now(UTC) + timedelta(days=random.randint(3, 60))
        end_date = start_date + timedelta(hours=random.randint(2, 6))

        return {
            "name": name,
            "description": description,
            "image_url": self._random_image_url() if random.random() > 0.2 else None,
            "location": (
                random.choice(data["locations"]) if random.random() > 0.2 else None
            ),
            "start_date": start_date,
            "end_date": end_date,
        }

    def _random_image_url(self) -> str:
        """Generates a random image URL."""
        image_urls = [
            "https://images.unsplash.com/photo-1549399905-5d1a7c094ec2",
            "https://images.pexels.com/photos/3171837/pexels-photo-3171837.jpeg",
            "https://images.pexels.com/photos/1190298/pexels-photo-1190298.jpeg",
            "https://images.pexels.com/photos/5778899/pexels-photo-5778899.jpeg",
            "https://images.pexels.com/photos/256450/pexels-photo-256450.jpeg",
            "https://images.pexels.com/photos/6347/coffee-cup-working-happy.jpg",
            "https://images.unsplash.com/photo-1551033406-611cf9a28f67",
            "https://images.pexels.com/photos/2396220/pexels-photo-2396220.jpeg",
            "https://images.unsplash.com/photo-1514432324607-a09d9b4aefdd",
            "https://images.pexels.com/photos/167636/pexels-photo-167636.jpeg",
            "https://images.pexels.com/photos/5778898/pexels-photo-5778898.jpeg",
            "https://images.unsplash.com/photo-1482517967863-00e15c9b44be",
            "https://images.pexels.com/photos/159711/books-bookstore-book-reading-159711.jpeg",
            "https://images.pexels.com/photos/33129/popcorn-movie-party-entertainment.jpg",
            "https://images.unsplash.com/photo-1542037104857-ffbb0b9155fb",
            "https://images.pexels.com/photos/3558644/pexels-photo-3558644.jpeg",
            "https://images.pexels.com/photos/4345513/pexels-photo-4345513.jpeg",
            "https://images.pexels.com/photos/1566837/pexels-photo-1566837.jpeg",
        ]
        return random.choice(image_urls)
