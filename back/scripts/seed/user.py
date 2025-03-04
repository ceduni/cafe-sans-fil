"""
User seeder module.
"""

import json
import os
import random
import unicodedata

from faker import Faker
from tqdm import tqdm

from app.user.models import UserCreate
from app.user.service import UserService

random.seed(42)
Faker.seed(42)
fake = Faker("fr_FR")


class UserSeeder:
    """User seeder class."""

    def __init__(self):
        """Initializes the UserSeeder class."""
        self.ids = []
        self.photo_urls = self._load_data()

    def _load_data(self):
        """Loads user data from a JSON file."""
        path = os.path.join(os.getcwd(), "scripts", "seed", "data", "photo_urls.json")
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)

    async def seed_users(self, num_users: int):
        """Seeds a specified number of users."""
        datas = []
        for i in tqdm(range(num_users), desc="Users"):
            matricule = self.generate_matricule()
            first_name = fake.first_name()
            last_name = fake.last_name()
            email = (
                self.normalize_string(first_name).replace(" ", "").lower()
                + "."
                + self.normalize_string(last_name).replace(" ", "").lower()
                + "@umontreal.ca"
            )
            password = "Cafepass1"
            photo_url = self.photo_urls[i] if random.random() <= 1.00 else None

            data = UserCreate(
                email=email,
                matricule=matricule,
                username=matricule,
                password=password,
                first_name=first_name,
                last_name=last_name,
                photo_url=photo_url,
            )
            datas.append(data)

        self.ids = await UserService.create_many(datas)
        await self.update_first_user()

    async def update_first_user(self):
        """Updates the first user to cafesansfil."""
        user = await UserService.get_by_id(self.ids[0])
        matricule = "7802085"
        data = {
            "email": "cafesansfil@umontreal.ca",
            "matricule": matricule,
            "username": matricule,
            "password": "Cafepass1",
            "first_name": "Tom",
            "last_name": "Holland",
            "photo_url": "https://i.pinimg.com/originals/50/c0/88/50c0883ae3c0e6be1213407c2b746177.jpg",
        }
        await UserService.update(user, UserCreate(**data))

    def normalize_string(self, input_str: str) -> str:
        """Normalizes a string by removing diacritics."""
        normalized_str = unicodedata.normalize("NFKD", input_str)
        ascii_str = normalized_str.encode("ascii", "ignore")
        return ascii_str.decode("ascii")

    def generate_matricule(self):
        """Generates a random matricule."""
        if random.random() < 0.95:
            # 8 digit
            matricule_num = random.randint(20000000, 20299999)
        else:
            # 6 or 7 digits
            length = random.choice([6, 7])
            matricule_num = random.randint(10 ** (length - 1), (10**length) - 1)

        return str(matricule_num)
