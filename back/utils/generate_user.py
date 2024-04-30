from app.schemas.user_schema import UserAuth, UserUpdate
from app.services.user_service import UserService
import json
from tqdm import tqdm
import pymongo
from faker import Faker
import unicodedata
import random

random.seed(42)
Faker.seed(42)
fake = Faker("fr_FR")


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
                matricule = generate_matricule()
                first_name = fake.first_name()
                last_name = fake.last_name()
                email = (
                    normalize_string(first_name).replace(" ", "").lower()
                    + "."
                    + normalize_string(last_name).replace(" ", "").lower()
                    + "@umontreal.ca"
                )
                password = "Cafepass1"
                photo_url = (
                    photo_urls[i] if random.random() <= 1.00 else None
                )  # chance of having a photo

                user_data = UserAuth(
                    email=email,
                    matricule=matricule,
                    username=matricule,
                    password=password,
                    first_name=first_name,
                    last_name=last_name,
                    photo_url=photo_url,
                )

                user = await UserService.create_user(user_data)
                user_usernames.append(user.username)
                break
            except pymongo.errors.DuplicateKeyError:
                continue

    # Update the first User to be cafesansfil
    cafesansfil_matricule = "7802085"
    cafesansfil_user = {
        "email": "cafesansfil@umontreal.ca",
        "matricule": cafesansfil_matricule,
        "username": cafesansfil_matricule,
        "password": "Cafepass1",
        "first_name": "Tom",
        "last_name": "Holland",
        "photo_url": "https://i.pinimg.com/originals/50/c0/88/50c0883ae3c0e6be1213407c2b746177.jpg",
    }
    await UserService.update_user(user_usernames[0], UserUpdate(**cafesansfil_user))
    user_usernames[0] = cafesansfil_matricule
    return user_usernames


# This function is used to normalize the first_name and last_name to be used as a password
# Example: "Éric" -> "Eric"
def normalize_string(input_str: str) -> str:
    normalized_str = unicodedata.normalize("NFKD", input_str)
    ascii_str = normalized_str.encode("ascii", "ignore")
    return ascii_str.decode("ascii")


def generate_matricule():
    if random.random() < 0.95:
        # 8 digit
        matricule_num = random.randint(20000000, 20299999)
    else:
        # Other digits
        length = random.choice([6, 7])
        matricule_num = random.randint(10 ** (length - 1), (10**length) - 1)

    return str(matricule_num)
