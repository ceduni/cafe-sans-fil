"""
Module for handling category-related operations.
"""

from typing import List

from beanie import PydanticObjectId

from app.menu.category.models import (
    MenuCategory,
    MenuCategoryCreate,
    MenuCategoryUpdate,
)
from app.cafe.models import Cafe


class CategoryService:
    """Service class for CRUD and search operations on Menu."""

    @staticmethod
    async def get_all(cafe: Cafe) -> List[MenuCategory]:
        """Get a menu category by ID."""
        return cafe.menu.categories

    @staticmethod
    async def get_by_id(cafe: Cafe, id: PydanticObjectId) -> MenuCategory:
        """Get a menu category by ID."""
        for category in cafe.menu.categories:
            if category.id == id:
                return category

        return None

    @staticmethod
    async def get_by_name(cafe: Cafe, name: str) -> MenuCategory:
        """Get a menu category by name."""
        for category in cafe.menu.categories:
            if category.name == name:
                return category

        return None

    @staticmethod
    async def create(cafe: Cafe, data: MenuCategoryCreate) -> MenuCategory:
        """Create a new menu category."""
        for category in cafe.menu.categories:
            if category.name == data.name:
                return

        category = MenuCategory(**data.model_dump())
        cafe.menu.categories.append(category)
        await cafe.save()
        return category

    @staticmethod
    async def update(
        cafe: Cafe,
        id: PydanticObjectId,
        data: MenuCategoryUpdate,
    ) -> MenuCategory:
        """Update a menu category."""
        for idx, cat in enumerate(cafe.menu.categories):
            if cat.id == id:
                category = cat.model_copy(update=data.model_dump(exclude_unset=True))
                category.id = id
                cafe.menu.categories[idx] = category
                await cafe.save()
                return category

        raise None

    @staticmethod
    async def delete(cafe: Cafe, id: PydanticObjectId) -> None:
        """Delete a menu category."""
        original_len = len(cafe.menu.categories)
        cafe.menu.categories = [c for c in cafe.menu.categories if c.id != id]

        if len(cafe.menu.categories) == original_len:
            return

        await cafe.save()

    @staticmethod
    async def create_many(
        cafe: Cafe, datas: List[MenuCategoryCreate]
    ) -> List[MenuCategory]:
        """Create multiple menu categories."""
        for data in datas:
            for category in cafe.menu.categories:
                if category.name == data.name:
                    return
            category = MenuCategory(**data.model_dump())
            cafe.menu.categories.append(category)
        await cafe.save()
        return cafe.menu.categories
