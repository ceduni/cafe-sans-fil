from app.schemas.user_schema import UserAuth, UserUpdate
from app.services.user_service import UserService
from app.models.user_model import DietProfile
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

                diet_profile = generate_diet_profile()
                likes = []

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

                user_update = UserUpdate(
                    diet_profile=diet_profile,
                    likes=likes,
                )
                await UserService.update_user(user.username, user_update)

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

def generate_diet_profile():
    cafes = ["le-mozza", "pill-pub", "cafekine", "la-planck", "acquis-de-droit", "cafcom", "tore-et-fraction", "cafe-anthropologie",
            "cafe-beagel", "holocene", "la-brunante", "la-retenue"]
    diets = [
        {
            "name": "Végétarien",
            "description": "Le végétarisme est une pratique alimentaire qui consiste à ne pas consommer de viande, de poisson, d'œufs, de lait ou de produits laitiers.",
            "forbidden_foods": ["viande", "poisson", "œuf", "lait", "miel"],
            "valid_cafes": random.sample(cafes, random.randint(0, len(cafes))),
            "checked": True,
        },
        {
            "name": "Végan",
            "description": "Le véganisme est une pratique alimentaire qui consiste à ne pas consommer de viande, de poisson, d'œufs, de lait ou de produits laitiers.",
            "forbidden_foods": ["viande", "poisson", "œuf", "lait"],
            "valid_cafes": random.sample(cafes, random.randint(0, len(cafes))),
            "checked": False,
        },
        {
            "name": "Sans Gluten",
            "description": "Le sans-gluten est une pratique alimentaire qui consiste à ne pas consommer de gluten.",
            "forbidden_foods": ["ble", "pain", "croissant", "chocolatine"],
            "valid_cafes": random.sample(cafes, random.randint(0, len(cafes))),
            "checked": True,
        },
        {
            "name": "Sans Lait",
            "description": "Le sans-lait est une pratique alimentaire qui consiste à ne pas consommer de produits laitiers.",
            "forbidden_foods": ["lait", "fromage", "œuf"],
            "valid_cafes": random.sample(cafes, random.randint(0, len(cafes))),
            "checked": False,
        },
        {
            "name": "Sans Huile de Colza",
            "description": "Le sans-huile de colza est une pratique alimentaire qui consiste à ne pas consommer d'huile de colza.",
            "forbidden_foods": ["arachides", "huile de colza"],
            "valid_cafes": random.sample(cafes, random.randint(0, len(cafes))),
            "checked": True,
        },
    ]

    nutrients = ["proteins", "fiber", "vitaminA", "vitaminC", "vitaminE", "vitaminD", "vitaminK", "vitaminB6", "vitaminB12", 
                 "minerals", "carbohydrates", "saturated_fat", "sodium", "lipids"]
    
    allergens = ["lactose", "poisson", "oeuf", "soja", "crustacés", "fruits-de-mer", "arachides", "noix", "huile de colza"]

    diet_profile = DietProfile(
        # diets=random.sample(diets, random.randint(0, len(diets))),
        diets=[],
        # prefered_nutrients={nutrient: random.randint(1, 3) for nutrient in random.sample(nutrients, random.randint(0, len(nutrients)))},
        prefered_nutrients={},
        # allergens={allergen: random.randint(1, 3) for allergen in random.sample(allergens, random.randint(0, len(allergens)))}
        allergens={}
    )
    return diet_profile

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