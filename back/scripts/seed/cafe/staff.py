"""
Staff seeder module.
"""

import random
from typing import List, Tuple

from beanie import PydanticObjectId
from faker import Faker
from tqdm import tqdm

from app.cafe.models import Cafe
from app.cafe.service import CafeService
from app.cafe.staff.enums import Role
from app.cafe.staff.service import StaffService
from app.user.models import User
from app.user.service import UserService

random.seed(42)
Faker.seed(42)
fake = Faker("fr_FR")


class StaffSeeder:
    """Staff seeder class."""

    async def seed_staff(self) -> None:
        """Seeds staff members for cafes."""
        cafes: List[Cafe] = await CafeService.get_all()
        users: List[User] = await UserService.get_all(sort_by="_id")

        for index, cafe in enumerate(tqdm(cafes, desc="Staff")):
            if not cafe:
                continue

            # Generate staff members using pre-loaded users
            admins, volunteers = self.random_staff_members(
                users=users,
                owner_id=cafe.owner_id,
                is_second_cafe=index == 1,
                is_third_cafe=index == 2,
                is_last_cafe=index == len(cafes) - 1,
            )

            # Add roles to cafe
            if admins:
                await StaffService.add_many(cafe, Role.ADMIN, [u.id for u in admins])
            if volunteers:
                await StaffService.add_many(
                    cafe, Role.VOLUNTEER, [u.id for u in volunteers]
                )

            # Update users' cafe_ids
            for user in admins + volunteers:
                if cafe.id not in user.cafe_ids:
                    user.cafe_ids.append(cafe.id)
                    await user.save()

    def random_staff_members(
        self,
        users: List[User],
        owner_id: PydanticObjectId,
        is_second_cafe: bool,
        is_third_cafe: bool,
        is_last_cafe: bool,
    ) -> Tuple[List[User], List[User]]:
        """Generates staff members using pre-loaded user objects."""
        # Exclude owner and create working copy
        available_users = [u for u in users if u.id != owner_id]
        admins = []
        volunteers = []

        # Handle special cases for first user
        if available_users:
            first_user = available_users[0]
            if is_second_cafe:
                admins.append(first_user)
                available_users.remove(first_user)
            elif is_third_cafe:
                volunteers.append(first_user)
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

        # Split into roles and deduplicate
        admins += selected_users[:num_admins]
        volunteers += selected_users[num_admins:]

        # Remove duplicates using dictionary (preserves order)
        return (
            list({u.id: u for u in admins}.values()),
            list({u.id: u for u in volunteers}.values()),
        )
