# scripts/db_seed/user_seeder.py

import json
import random
import unicodedata
from faker import Faker
from tqdm import tqdm
from app.services.user_service import UserService
from app.schemas.user_schema import UserAuth
from pymongo.errors import DuplicateKeyError

# Set random seed and Faker settings
random.seed(42)
Faker.seed(42)
fake = Faker('fr_FR')

# Load photo URLs from JSON file
with open("./scripts/db_seed/data/photo_urls.json", "r", encoding="utf-8") as file:
    photo_urls = json.load(file)

class UserSeeder:
    def __init__(self):
        self.usernames = []

    async def seed_users(self, num_users: int):
        """
        Seeds a specified number of users into the database.
        """
        if len(photo_urls) < num_users:
            raise ValueError("Not enough photo URLs for the number of users")

        users_data = []
        for i in tqdm(range(num_users), desc="Seed users"):
            matricule = self.generate_matricule()
            first_name = fake.first_name()
            last_name = fake.last_name()
            email = self.normalize_string(first_name).replace(" ", "").lower() + "." + self.normalize_string(last_name).replace(" ", "").lower() + "@umontreal.ca"
            password = "Cafepass1"
            photo_url = photo_urls[i] if random.random() <= 1.00 else None  # Chance of having a photo

            user_data = UserAuth(
                email=email,
                matricule=matricule,
                username=matricule,
                password=password,
                first_name=first_name,
                last_name=last_name,
                photo_url=photo_url
            )
            users_data.append(user_data)

        # Insert all users in bulk
        created_users = await UserService.create_many_users(users_data)
        
        # Track usernames
        self.usernames = [user.username for user in created_users]

        print(f"{num_users} users created")

        await self.update_first_user_to_cafesansfil()

    async def update_first_user_to_cafesansfil(self):
        """
        Updates the first user to 'cafesansfil'.
        """
        cafesansfil_matricule = "7802085"
        cafesansfil_user = {
            "email": "cafesansfil@umontreal.ca",
            "matricule": cafesansfil_matricule,
            "username": cafesansfil_matricule,
            "password": "Cafepass1",
            "first_name": "Tom",
            "last_name": "Holland",
            "photo_url": "https://i.pinimg.com/originals/50/c0/88/50c0883ae3c0e6be1213407c2b746177.jpg"
        }
        await UserService.update_user(self.usernames[0], UserAuth(**cafesansfil_user))
        self.usernames[0] = cafesansfil_matricule

    def get_usernames(self):
        """
        Returns the list of generated usernames.
        """
        return self.usernames

    def normalize_string(self, input_str: str) -> str:
        """
        Normalizes a string by converting it to ASCII (e.g., 'Éric' -> 'Eric').
        """
        normalized_str = unicodedata.normalize('NFKD', input_str)
        ascii_str = normalized_str.encode('ascii', 'ignore')
        return ascii_str.decode('ascii')

    def generate_matricule(self):
        """
        Generates a random matricule number.
        """
        if random.random() < 0.95:
            # 8 digit matricule
            matricule_num = random.randint(20000000, 20299999)
        else:
            # Other lengths (6 or 7 digits)
            length = random.choice([6, 7])
            matricule_num = random.randint(10**(length-1), (10**length)-1)

        return str(matricule_num)
