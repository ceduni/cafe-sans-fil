"""
Interaction seeder module.
"""

import random
from datetime import UTC, datetime, timedelta, timezone
from typing import List, Optional

from faker import Faker
from tqdm import tqdm
from uuid import uuid4
from app.user.models import User, Diet, DietProfile
from app.user.service import UserService

random.seed(42)

fake = Faker("fr_FR")

# --- Sample domain data ---
categories = ["Végétarien", "Vegan", "Sans gluten", "Paleo", "Keto", "Hallal", "Casher"]
food_items = ["pain", "poulet", "tofu", "riz", "lait", "œufs", "quinoa", "tomates", "avocat", "poisson"]
cafes = [
    "Acquis de droit", "CafCom", "Café Anthropologie", "Café Beagel", 
    "Café nutri-bar", "Café-In", "CaféKine", "Holocène", "L’établi", 
    "L’Intermed", "La Brunante", "La Planck", "La Retenue", "Le Macrophage", 
    "Le Mal-aimé", "Le Triton", "Le Vivarium", "Pill Pub", "Psychic",
    "Tore et Fraction"]
health_conditions = ["diabète", "cholestérol", "intolérance au lactose", "allergie aux noix"]
nutrients = ["protéines", "glucides", "lipides", "fibres", "fer", "calcium"]
tags_pool = ["#santé", "#énergie", "#végétal", "#sport", "#digestion", "#local"]


def public_diet() -> Diet:
    nutrient_targets = {
        nutrient: round(random.uniform(10.0, 100.0), 2)
        for nutrient in random.sample(nutrients, k=random.randint(2, 4))
    }

    return Diet(
        name=fake.catch_phrase(),
        description=fake.sentence(nb_words=10),
        category= random.choice(categories),
        forbidden_foods=random.sample(food_items, k=random.randint(1, 3)),
        desired_foods=random.sample(food_items, k=random.randint(2, 4)),
        valid_cafes=random.sample(cafes, k=random.randint(1, 3)),
        suitable_for_conditions=random.sample(health_conditions, k=random.randint(0, 2)),
        nutrient_targets=nutrient_targets,
        tags=random.sample(tags_pool, k=random.randint(1, 3)),
        is_custom=False
    )
    

def user_diet(user_id: str) -> Diet:
    nutrient_targets = {
        nutrient: round(random.uniform(10.0, 100.0), 2)
        for nutrient in random.sample(nutrients, k=random.randint(2, 4))
    }

    return Diet(
        name=fake.catch_phrase(),
        description=fake.sentence(nb_words=10),
        category= random.choice(categories),
        forbidden_foods=random.sample(food_items, k=random.randint(1, 3)),
        desired_foods=random.sample(food_items, k=random.randint(2, 4)),
        valid_cafes=random.sample(cafes, k=random.randint(1, 3)),
        suitable_for_conditions=random.sample(health_conditions, k=random.randint(0, 2)),
        nutrient_targets=nutrient_targets,
        tags=random.sample(tags_pool, k=random.randint(1, 3)),
        is_custom=True,
        created_by_user_id=user_id,
    )

class DietSeeder:
    """Notification seeder class."""

    def __init__(self):
        """Initializes the NotificationSeeder."""
        self.diets: List = []
        self.users: List[User] = []
        

    async def seed_diet(self, num_diets: int = 20, num_diets_per_user:  Optional[List[int]] = None):
        """Seed diets."""
        self.users = await UserService.get_all()
        
        if num_diets_per_user is None:
            num_diets_per_user = [1, 5]
        
        for _ in tqdm(range(num_diets), desc="Diets"):
            if random.randint(0,20) < 10:
                self.diets.append(public_diet())
            else:
                self.diets.append(user_diet(random.choice(self.users).id))

        result = await Diet.insert_many(self.diets)
        diet_ids = result.inserted_ids
        
        # Get random subset of users
        users = random.sample(
            self.users,
            k=random.randint(
                int(len(self.users) * 0.2), int(len(self.users) * 0.6)
            ),
        )
        
        for user in tqdm(users, desc="User diets profile"):
            num_user_diets = random.randint(*num_diets_per_user)
            selected_ids = random.sample(diet_ids, k=min(num_user_diets, len(diet_ids)))
            
            user.diet_profile=DietProfile(
                diet_ids=selected_ids
            )
            await user.save()


    def _random_date(self) -> datetime:
        """Generate random date within last 6 months."""
        return datetime.now(UTC) - timedelta(
            days=random.randint(0, 180), hours=random.randint(0, 23)
        )
