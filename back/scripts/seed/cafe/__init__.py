"""
Cafe seeder module.
"""

import json
import os
import random
from datetime import UTC, datetime, timedelta
from typing import List

from beanie import PydanticObjectId
from faker import Faker
from tqdm import tqdm

from app.cafe.enums import Days, Feature, PaymentMethod
from app.cafe.models import (
    AdditionalInfo,
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
from app.cafe.service import CafeService

random.seed(42)
Faker.seed(42)
fake = Faker("fr_FR")

file_path = os.path.join(os.getcwd(), "scripts", "seed", "data", "cafes.json")
with open(file_path, "r", encoding="utf-8") as file:
    json_datas = json.load(file)


class CafeSeeder:
    """Cafes seeder class."""

    def __init__(self):
        """Initializes the CafeSeeder class."""
        self.ids: List[PydanticObjectId] = []
        self.json_datas = json_datas

    async def seed_cafes(self, num_cafes: int, user_ids: List[PydanticObjectId] = []):
        """Seeds a specified number of cafes."""
        for idx, data in enumerate(tqdm(json_datas[:num_cafes], desc="Seed cafes")):
            photo_urls = self._random_photo_urls()
            is_open, status_message = self._random_open_status_message()
            opening_hours = self._random_opening_hours()
            payment_details = self._random_payment_details()
            additional_info = self._random_additional_info()

            data = CafeCreate(
                name=data["name"],
                features=[Feature.ORDER] if random.random() <= 0.8 else [],
                description=data["description"],
                logo_url=None,
                banner_url=data["banner_url"],
                photo_urls=photo_urls,
                affiliation=Affiliation(**data["affiliation"]),
                is_open=is_open,
                status_message=status_message,
                opening_hours=opening_hours,
                location=Location(**data["location"]),
                contact=Contact(**data["contact"]),
                social_media=SocialMedia(**data.get("social_media", {})),
                payment_details=payment_details,
                additional_info=additional_info,
            )

            user_id = user_ids[idx % len(user_ids)] if user_ids else None
            cafe: Cafe = await CafeService.create(data, user_id)
            self.ids.append(cafe.id)

        print(f"{num_cafes} cafes created")

    def get_ids(self):
        """Returns the generated cafe IDs."""
        return self.ids

    def _random_photo_urls(self):
        """Returns a random subset of photo URLs."""
        photo_urls = [
            "https://picsum.photos/id/237/200/300",  # Random dog image
            "https://picsum.photos/id/238/200/300",  # Random city image
            "https://picsum.photos/id/239/200/300",  # Random nature image
            "https://unsplash.com/photos/1J8k0qqUfYY",  # Random Unsplash image
            "https://picsum.photos/id/240/200/300",  # Random abstract image
            "https://picsum.photos/id/241/200/300",  # Random architecture image
            "https://unsplash.com/photos/3Z70SDuYs5g",  # Random Unsplash image
        ]

        k = random.randint(0, len(photo_urls))

        return random.sample(photo_urls, k=k)

    # Helper functions for generating random data
    def _random_open_status_message(self):
        """Generates a random open status message."""
        messages = [
            "Fermé pour la journée",
            "Fermé pour la semaine",
            "Fermé pour MIDIRO",
            "De retour dans 1 heure",
        ]
        is_open = random.random() < 0.7  # chance of being open
        status_message = random.choice(messages) if not is_open else None
        return is_open, status_message

    def _random_opening_hours(self):
        """Generates random opening hours for a cafe."""
        days = list(Days)
        opening_hours = []

        for day in days:
            has_break = random.choice([True, False])
            morning_start_hour = random.randint(8, 10)
            morning_start = f"{morning_start_hour:02d}:00"

            if has_break:
                morning_end_hour = random.randint(11, 13)
                morning_end = f"{morning_end_hour:02d}:00"
                afternoon_start_hour = morning_end_hour + 1
                afternoon_start = f"{afternoon_start_hour:02d}:00"
            else:
                morning_end = afternoon_start = "17:00"

            afternoon_end_hour = random.randint(16, 18)
            afternoon_end = f"{afternoon_end_hour:02d}:00"
            blocks = [TimeBlock(start=morning_start, end=morning_end)]
            if has_break:
                blocks.append(TimeBlock(start=afternoon_start, end=afternoon_end))
            opening_hours.append(DayHours(day=day, blocks=blocks))

        return opening_hours

    def _random_payment_details(self):
        """Generates random payment methods for a cafe."""
        methods = list(PaymentMethod)
        selected_methods_count = random.randint(1, len(methods))
        selected_methods = random.sample(methods, selected_methods_count)
        payment_details = []

        for method in selected_methods:
            minimum = (
                random.randint(3, 8)
                if method in [PaymentMethod.CREDIT, PaymentMethod.DEBIT]
                else None
            )
            payment_details.append(PaymentDetails(method=method, minimum=minimum))
        return payment_details

    def _random_additional_info(self):
        """Generates random additional info for a cafe."""
        today = datetime.now(UTC)
        info_types = [
            "Fermeture temporaire",
            "Offres spéciales",
            "Nouveau menu",
        ]
        additional_infos = []

        if random.random() < 0.50:
            return additional_infos

        num_infos = random.randint(0, 2)
        for _ in range(num_infos):
            event_type = random.choice(info_types)
            start = today + timedelta(days=random.randint(-3, 0))
            end = None
            date_message = today + timedelta(days=random.randint(-1, 7))
            additional_info = AdditionalInfo(
                type=event_type,
                value=(
                    f"{event_type} à {date_message.strftime('%d/%m/%Y')}"
                    if random.random() > 0.25
                    else f"{event_type}"
                ),
                start=start,
                end=end,
            )
            additional_infos.append(additional_info.model_dump())

        return additional_infos
