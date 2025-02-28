"""
Staff seeder module.
"""

import random
from typing import List

from beanie import PydanticObjectId
from faker import Faker
from tqdm import tqdm

from app.cafe.service import CafeService
from app.cafe.staff.enums import Role
from app.cafe.staff.service import StaffService

random.seed(42)
Faker.seed(42)
fake = Faker("fr_FR")


class StaffSeeder:
    async def seed_staff(
        self, cafe_ids: List[PydanticObjectId], user_ids: List[PydanticObjectId]
    ):
        """Seeds staff members for cafes using StaffService."""
        for index, cafe_id in enumerate(tqdm(cafe_ids, desc="Seeding staff for cafes")):
            cafe = await CafeService.get(cafe_id)
            if not cafe:
                continue

            # Get the cafe's owner ID to exclude from staff roles
            owner_id = cafe.owner_id

            # Determine special case flags
            is_second_cafe = index == 1
            is_third_cafe = index == 2
            is_last_cafe = index == len(cafe_ids) - 1

            # Generate staff members
            admin_ids, volunteer_ids = self.random_staff_members(
                user_ids=user_ids,
                owner_id=owner_id,
                is_second_cafe=is_second_cafe,
                is_third_cafe=is_third_cafe,
                is_last_cafe=is_last_cafe,
            )

            # Add roles to cafe
            if admin_ids:
                await StaffService.add_many(cafe, Role.ADMIN, admin_ids)
            if volunteer_ids:
                await StaffService.add_many(cafe, Role.VOLUNTEER, volunteer_ids)

        print(f"Staff members added to {len(cafe_ids)} cafes")

    def random_staff_members(
        self,
        user_ids: List[PydanticObjectId],
        owner_id: PydanticObjectId,
        is_second_cafe: bool,
        is_third_cafe: bool,
        is_last_cafe: bool,
    ) -> tuple[List[PydanticObjectId], List[PydanticObjectId]]:
        """Generates staff members ensuring owner exclusion and special cases."""
        # Exclude owner from available users
        available_users = [uid for uid in user_ids if uid != owner_id]
        admin_ids = []
        volunteer_ids = []
        first_user = user_ids[0] if user_ids else None

        # Handle special cases for first user
        if first_user and first_user != owner_id:
            if is_second_cafe:
                admin_ids.append(first_user)
                available_users.remove(first_user)
            elif is_third_cafe:
                volunteer_ids.append(first_user)
                available_users.remove(first_user)
            elif is_last_cafe and first_user in available_users:
                available_users.remove(first_user)

        # Determine staff counts
        num_admins = random.randint(1, 6)
        num_volunteers = random.randint(12, 20)
        total_needed = num_admins + num_volunteers

        # Select unique users from remaining pool
        selected_users = random.sample(
            available_users, k=min(total_needed, len(available_users))
        )

        # Split into roles ensuring no overlap
        admin_ids += selected_users[:num_admins]
        volunteer_ids += selected_users[num_admins:]

        return list(set(admin_ids)), list(set(volunteer_ids))
