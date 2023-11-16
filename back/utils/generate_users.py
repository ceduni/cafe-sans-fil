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
                email=fake.email()
                matricule=fake.bothify(text='??#####').lower()
                username=fake.user_name()
                first_name = fake.first_name()
                last_name = fake.last_name()
                photo_url = fake.image_url(width=200, height=200) if random.random() <= 0.2 else None

                user_data = UserAuth(
                    email=email,
                    matricule=matricule,
                    username=username,
                    password=first_name + last_name, # Password is first_name+last_name for testing
                    first_name=first_name,
                    last_name=last_name,
                    photo_url=photo_url
                )

                user = await UserService.create_user(user_data)
                user_ids.append(user.user_id)
                break
            except pymongo.errors.DuplicateKeyError:
                continue
    
    # Update one User to be cafesansfil
    cafesansfil_user = {
        "email": "keanu@johnwick.com",
        "matricule": "JW12345",
        "username": "cafesansfil",
        "password": "cafesansfil",
        "first_name": "Keanu",
        "last_name": "Reeves",
        "photo_url": "https://external-content.duckduckgo.com/iu/?u=https%3A%2F%2Fwww.dreshare.com%2Fwp-content%2Fuploads%2F2019%2F11%2FKeanu-Reeves-300x275.jpg&f=1&nofb=1&ipt=7f7c2f67827bd70578e888fbdba4d77fabc59fb2cb489f35b5854d6b74d3c81e&ipo=images"
    }
    await UserService.update_user(user_ids[0], UserAuth(**cafesansfil_user))
    
    return user_ids
