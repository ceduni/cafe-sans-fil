"""
Staff seeder module.
"""

import random
from typing import List

from beanie import PydanticObjectId
from faker import Faker
from tqdm import tqdm

from app.cafe.models import Role
from app.cafe.service import CafeService
from app.cafe.staff.service import StaffService

random.seed(42)
Faker.seed(42)
fake = Faker("fr_FR")


class StaffSeeder:
    async def seed_staff_for_cafes(
        self, cafe_ids: List[PydanticObjectId], user_ids: List[PydanticObjectId]
    ):
        """Seeds staff members for cafes using StaffService."""
        for index, cafe_id in enumerate(tqdm(cafe_ids, desc="Seeding staff for cafes")):
            cafe = await CafeService.get(cafe_id)

            if not cafe:
                continue

            # Get staff configuration
            admin_ids, volunteer_ids = self.random_staff_members(
                user_ids=user_ids,
                is_first_cafe=(index == 0),
                exclude_first_user=(index in {1, len(cafe_ids) - 1}),
            )

            # Add staff using the service
            if admin_ids:
                await StaffService.add_many(cafe, Role.ADMIN, admin_ids)
            if volunteer_ids:
                await StaffService.add_many(cafe, Role.VOLUNTEER, volunteer_ids)

        print(f"Staff members added to {len(cafe_ids)} cafes")

    def random_staff_members(
        self,
        user_ids: List[PydanticObjectId],
        is_first_cafe: bool = False,
        exclude_first_user: bool = False,
    ) -> tuple[List[PydanticObjectId], List[PydanticObjectId]]:
        """Generates random staff members with proper role separation."""
        available_users = user_ids.copy()
        admin_ids = []
        volunteer_ids = []

        # Handle first user logic
        if is_first_cafe:
            admin_ids.append(user_ids[0])
            available_users = available_users[1:]
        elif exclude_first_user:
            available_users = available_users[1:]

        # Determine staff counts
        num_admins = random.randint(1, 6) if not is_first_cafe else 0
        num_volunteers = random.randint(12, 20)

        # Select unique users
        selected_users = random.sample(
            available_users, k=min(num_admins + num_volunteers, len(available_users))
        )

        # Split into admins and volunteers
        admin_ids += selected_users[:num_admins]
        volunteer_ids += selected_users[num_admins:]

        return admin_ids, volunteer_ids
