from app.schemas.user_schema import UserAuth
from app.services.user_service import UserService
from tqdm import tqdm
import pymongo
from faker import Faker
import random
random.seed(42)
Faker.seed(42)
fake = Faker('fr_FR')

async def create_users(num_users):
    user_ids = []

    for _ in tqdm(range(num_users), desc="Creating users"):
        while True:
            try:
                first_name = fake.first_name()
                last_name = fake.last_name()
                photo_url = None
                if random.random() <= 0.2:
                    photo_url = fake.image_url(width=200, height=200)

                user_data = UserAuth(
                    email=fake.email(),
                    matricule=fake.bothify(text='??#####').lower(),
                    # matricule = fake.bothify(text='########'),
                    username=fake.user_name(),
                    password=first_name + last_name, # For testing
                    first_name=first_name,
                    last_name=last_name,
                    photo_url=photo_url
                )

                user = await UserService.create_user(user_data)
                user_ids.append(user.user_id)
                break

            except pymongo.errors.DuplicateKeyError:
                continue
            
    return user_ids
