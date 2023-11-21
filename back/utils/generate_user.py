from app.schemas.user_schema import UserAuth
from app.services.user_service import UserService
import json
from tqdm import tqdm
import pymongo
from faker import Faker
import unicodedata
import random
random.seed(42)
Faker.seed(42)
fake = Faker('fr_FR')

async def create_users(num_users):
    user_usernames = []

    # Read URLs from JSON file
    with open("./utils/templates/photo_urls.json", "r", encoding="utf-8") as file:
        photo_urls = json.load(file)

    if len(photo_urls) < num_users:
        raise ValueError("Not enough photo URLs for the number of users")

    for i in tqdm(range(num_users), desc="Creating users"):
        while True:
            try:
                email = fake.email()
                matricule = fake.bothify(text='??#####').lower()
                username = fake.user_name()
                first_name = fake.first_name()
                last_name = fake.last_name()
                password = normalize_string(first_name).replace(" ", "") + normalize_string(last_name).replace(" ", "") + "1" # password is first_name+last_name+"1" (For Test)
                photo_url = photo_urls[i] if random.random() <= 1.00 else None # chance of having a photo

                user_data = UserAuth(
                    email=email,
                    matricule=matricule,
                    username=username,
                    password=password,
                    first_name=first_name,
                    last_name=last_name,
                    photo_url=photo_url
                )

                user = await UserService.create_user(user_data)
                user_usernames.append(user.username)
                break
            except pymongo.errors.DuplicateKeyError:
                continue

    # Update the first User to be cafesansfil
    cafesansfil_user = {
        "email": "cafesansfil@example.com",
        "matricule": "cs12345",
        "username": "cafesansfil",
        "password": "Cafesansfil1",
        "first_name": "Tom",
        "last_name": "Holland",
        "photo_url": "https://i.pinimg.com/originals/50/c0/88/50c0883ae3c0e6be1213407c2b746177.jpg"
    }
    await UserService.update_user(user_usernames[0], UserAuth(**cafesansfil_user))
    user_usernames[0] = "cafesansfil"
    return user_usernames

# This function is used to normalize the first_name and last_name to be used as a password
# Example: "Éric" -> "Eric"
def normalize_string(input_str: str) -> str:
    normalized_str = unicodedata.normalize('NFKD', input_str)
    ascii_str = normalized_str.encode('ascii', 'ignore')
    return ascii_str.decode('ascii')