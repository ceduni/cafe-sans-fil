"""
Cafe seeder module.
"""

import json
import os
import random
from typing import List, Optional

from slugify import slugify
from tqdm import tqdm

from app.cafe.enums import Days, Feature, PaymentMethod
from app.cafe.models import (
    Affiliation,
    Cafe,
    CafeCreate,
    Contact,
    DayHours,
    Location,
    PaymentDetails,
    SocialMedia,
    TimeBlock,
)
from app.user.models import User
from app.user.service import UserService

random.seed(42)


class CafeSeeder:
    """Cafe seeder class."""

    def __init__(self):
        """Initializes the CafeSeeder."""
        self.cafes: List[Cafe] = []
        self.data = self._load_data()

    def _load_data(self):
        """Loads cafe data from a JSON file."""
        path = os.path.join(os.getcwd(), "scripts", "seed", "data", "cafes.json")
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)

    async def seed_cafes(self, num_cafes: int) -> None:
        """Seed cafes with realistic data."""
        users = await UserService.get_all(sort_by="_id")

        for idx, cafe_data in enumerate(tqdm(self.data[:num_cafes], desc="Cafes")):
            owner = users[idx % len(users)] if users else None
            self.cafes.append(await self._create_cafe(cafe_data, owner))

        result = await Cafe.insert_many(self.cafes)
        cafe_ids = result.inserted_ids

        # Update users' cafe_ids
        for i in range(len(cafe_ids)):
            users[i].cafe_ids.append(cafe_ids[i])
            await users[i].save()

    async def _create_cafe(self, data: dict, owner: User = None) -> Cafe:
        """Build Cafe instance without inserting."""
        cafe_data = CafeCreate(
            name=data["name"],
            features=self._random_features(),
            description=data["description"],
            logo_url=None,
            banner_url=data["banner_url"],
            photo_urls=self._random_photo_urls(),
            affiliation=Affiliation(**data["affiliation"]),
            is_open=self._random_open_status(),
            status_message=self._random_status_message(),
            opening_hours=self._random_opening_hours(),
            location=Location(**data["location"]),
            contact=Contact(**data["contact"]),
            social_media=SocialMedia(**data.get("social_media", {})),
            payment_details=self._random_payment_details(),
        )

        cafe = Cafe(
            **cafe_data.model_dump(),
            owner_id=owner.id if owner else None,
            slug=slugify(data["name"]),
        )
        return cafe

    def _random_features(self) -> List[Feature]:
        """Generate realistic cafe features."""
        return random.sample(list(Feature), k=random.randint(0, len(Feature)))

    def _random_photo_urls(self) -> List[str]:
        """Curated cafe-related images"""
        return [
            "https://picsum.photos/id/237/200/300",  # Random dog image
            "https://picsum.photos/id/238/200/300",  # Random city image
            "https://picsum.photos/id/239/200/300",  # Random nature image
            "https://unsplash.com/photos/1J8k0qqUfYY",  # Random Unsplash image
            "https://picsum.photos/id/240/200/300",  # Random abstract image
            "https://picsum.photos/id/241/200/300",  # Random architecture image
            "https://unsplash.com/photos/3Z70SDuYs5g",  # Random Unsplash image
            "https://images.unsplash.com/photo-1555396273-367ea4eb4db5",
            "https://images.pexels.com/photos/302899/pexels-photo-302899.jpeg",
            "https://images.pexels.com/photos/239581/pexels-photo-239581.jpeg",
        ][: random.randint(0, 9)]

    def _random_open_status(self) -> bool:
        """80% chance of being open"""
        return random.random() < 0.8

    def _random_status_message(self) -> Optional[str]:
        """Generate status message if closed"""
        if self._random_open_status():
            return None
        return random.choice(
            [
                "Réouverture le 15 août",
                "Fermé pour rénovation",
                "Congés annuels jusqu'au 30 juillet",
                "Fermeture exceptionnelle aujourd'hui",
                "Fermé pour MIDIRO",
                "De retour dans 1 heure",
            ]
        )

    def _random_opening_hours(self) -> List[DayHours]:
        """Generate consistent opening hours"""
        hours = []
        for day in Days:
            # 20% chance of being closed on weekend days
            if day in [Days.SATURDAY, Days.SUNDAY] and random.random() < 0.2:
                hours.append(DayHours(day=day, blocks=[]))
                continue

            # Standard cafe hours
            blocks = [
                TimeBlock(
                    start=f"{random.randint(7, 8):02d}:00",
                    end=f"{random.randint(12, 13):02d}:00",
                )
            ]

            # 80% chance of afternoon opening
            if random.random() < 0.8:
                blocks.append(
                    TimeBlock(
                        start=f"{random.randint(14, 15):02d}:00",
                        end=f"{random.randint(18, 20):02d}:00",
                    )
                )

            hours.append(DayHours(day=day, blocks=blocks))
        return hours

    def _random_payment_details(self) -> List[PaymentDetails]:
        """Generate modern payment methods"""
        methods = [
            (PaymentMethod.CASH, None),
            (PaymentMethod.DEBIT, random.randint(5, 10)),
            (PaymentMethod.CREDIT, random.randint(10, 15)),
        ]
        return [
            PaymentDetails(method=m, minimum=min)
            for m, min in random.sample(methods, k=random.randint(0, 3))
        ]
