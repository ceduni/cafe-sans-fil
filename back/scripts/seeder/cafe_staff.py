"""
Staff seeder module.
"""

import random
from typing import List

from beanie import PydanticObjectId
from faker import Faker
from tqdm import tqdm

from app.cafe.models import Role, StaffCreate
from app.cafe.service import CafeService

random.seed(42)
Faker.seed(42)
fake = Faker("fr_FR")


class StaffSeeder:
    async def seed_staff_for_cafes(
        self, cafe_ids: List[PydanticObjectId], user_ids: List[PydanticObjectId]
    ):
        """Seeds staff members for cafes."""
        for index, cafe_id in enumerate(tqdm(cafe_ids, desc="Seeding staff for cafes")):
            if index == 0:
                # First cafe, make cafesansfil an admin
                staff = self.random_staff_members(user_ids, first_user_admin=True)
            elif index == 1 or index == len(cafe_ids) - 1:
                # Second and last cafe, exclude cafesansfil
                staff = self.random_staff_members(user_ids, exclude_first_user=True)
            else:
                # Randomly assign staff for other cafes
                staff = self.random_staff_members(user_ids)

            cafe = await CafeService.get(cafe_id)
            await CafeService.create_many_staff(cafe, staff)

        print(f"Staff members added to cafes")

    def random_staff_members(
        self,
        user_ids: List[PydanticObjectId],
        first_user_admin=False,
        exclude_first_user=False,
    ):
        """Generates random staff members."""
        staff_members = []
        selected_users = user_ids.copy()

        # Always choose first user (cafesansfil) as admin in first cafe
        if first_user_admin:
            staff_members.append(StaffCreate(id=user_ids[0], role=Role.ADMIN))
            selected_users = selected_users[1:]

        # Exclude first user (cafesansfil) for certain cafes
        if exclude_first_user:
            selected_users = selected_users[1:]

        # Randomly assign remaining users to admin and volunteer roles
        num_admins = random.randint(1, 6) - len(staff_members)
        num_volunteers = random.randint(12, 20)
        selected_users = random.sample(selected_users, num_admins + num_volunteers)

        for id in selected_users[:num_admins]:
            staff_members.append(StaffCreate(id=id, role=Role.ADMIN))
        for id in selected_users[num_admins:]:
            staff_members.append(StaffCreate(id=id, role=Role.VOLUNTEER))

        return staff_members
