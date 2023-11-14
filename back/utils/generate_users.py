from app.schemas.user_schema import UserAuth
from app.services.user_service import UserService
from tqdm import tqdm
import pymongo

async def create_users(num_users, fake):
    user_ids = []
    for _ in tqdm(range(num_users), desc="Creating users"):
        while True:
            try:
                first_name = fake.first_name()
                last_name = fake.last_name()

                user_data = UserAuth(
                    first_name=first_name,
                    last_name=last_name,
                    email=fake.email(),
                    username=fake.user_name(),
                    # matricule=fake.bothify(text='??#####').lower(),
                    matricule = fake.bothify(text='########'),
                    password=first_name + last_name # For testing
                )

                user = await UserService.create_user(user_data)
                user_ids.append(user.user_id)
                break

            except pymongo.errors.DuplicateKeyError:
                continue
            
    return user_ids
