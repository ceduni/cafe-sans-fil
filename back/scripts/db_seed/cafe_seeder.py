"""
Cafes seeder module.
"""

import json
import random
from datetime import datetime, timedelta

from faker import Faker
from tqdm import tqdm

from app.cafe.models import (
    AdditionalInfo,
    Affiliation,
    CafeCreate,
    Contact,
    DayHours,
    Location,
    PaymentMethod,
    SocialMedia,
    TimeBlock,
)
from app.cafe.service import CafeService

random.seed(42)
Faker.seed(42)
fake = Faker("fr_FR")

with open("./scripts/db_seed/data/cafes.json", "r", encoding="utf-8") as file:
    cafes_data = json.load(file)


class CafeSeeder:
    """Cafes seeder class."""

    def __init__(self):
        """Initializes the CafeSeeder class."""
        self.cafe_ids = []

    async def seed_cafes(self, num_cafes: int):
        """Seeds a specified number of cafes."""
        for cafe_info in tqdm(cafes_data[:num_cafes], desc="Seed cafes"):
            is_open, status_message = self.random_open_status_message()
            opening_hours = self.random_opening_hours()
            payment_methods = self.random_payment_methods()
            additional_info = self.random_additional_info()

            cafe_data = CafeCreate(
                name=cafe_info["name"],
                features=["Order"] if random.random() <= 0.8 else [],
                description=cafe_info["description"],
                logo_url=None,
                image_url=cafe_info["image_url"],
                affiliation=Affiliation(**cafe_info["affiliation"]),
                is_open=is_open,
                status_message=status_message,
                opening_hours=opening_hours,
                location=Location(**cafe_info["location"]),
                contact=Contact(**cafe_info["contact"]),
                social_media=SocialMedia(**cafe_info.get("social_media", {})),
                payment_methods=payment_methods,
                additional_info=additional_info,
                staff=[],
            )

            created_cafe = await CafeService.create_cafe(cafe_data)
            self.cafe_ids.append(created_cafe.id)

        print(f"{num_cafes} cafes created")

    def get_cafe_ids(self):
        """Returns the generated cafe IDs."""
        return self.cafe_ids

    # Helper functions for generating random data
    def random_open_status_message(self):
        """Generates a random open status message."""
        messages = [
            "Fermé pour la journée",
            "Fermé pour la semaine",
            "De retour dans 1 heure",
            "Temporairement fermé",
            "Fermé pour MIDIRO",
        ]
        is_open = random.random() < 0.7  # chance of being open
        status_message = random.choice(messages) if not is_open else None
        return is_open, status_message

    def random_opening_hours(self):
        """Generates random opening hours for a cafe."""
        days = ["Lundi", "Mardi", "Mercredi", "Jeudi", "Vendredi"]
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

    def random_payment_methods(self):
        """Generates random payment methods for a cafe."""
        methods = ["Carte de débit", "Carte de crédit", "Argent comptant"]
        selected_methods_count = random.randint(1, len(methods))
        selected_methods = random.sample(methods, selected_methods_count)
        payment_methods = []

        for method in selected_methods:
            minimum = (
                random.randint(3, 8)
                if method in ["Carte de débit", "Carte de crédit"]
                else None
            )
            payment_methods.append(PaymentMethod(method=method, minimum=minimum))
        return payment_methods

    def random_additional_info(self):
        """Generates random additional info for a cafe."""
        today = datetime.now()
        info_types = [
            "Événement spécial",
            "Fermeture temporaire",
            "Promotion",
            "Atelier",
            "Nouveau produit",
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
