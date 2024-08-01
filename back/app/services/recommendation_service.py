from app.models.user_recommendations_model import UserRecommendation
from app.models.cafe_recommendations_model import CafeForRecommendation
from app.models.item_model import Item
from app.models.item_model import Item
from app.schemas.recommendation_schema import (
    CafeUpdate, 
    UserRecommendationUpdate,
    ItemUpdate
)
from uuid import UUID

class RecommendationService:

    #-------------------------- 
    #          Utils
    #--------------------------

    @staticmethod
    async def get_user(user_id: str):
        return await UserRecommendation.find_one({ "user_id": UUID(user_id) })
    
    @staticmethod
    async def get_user_by_username(username: str):
        return await UserRecommendation.find_one({ "username": username })
    
    @staticmethod
    async def get_cafe(cafe_slug: str):
        return await CafeForRecommendation.find_one({ "slug": cafe_slug })
    
    @staticmethod
    async def get_item(item_id: str):
        return await Item.find_one({ "item_id": UUID(item_id) })
    
    @staticmethod
    async def update_item(item_id: str, data: ItemUpdate):
        item = await RecommendationService.get_item(item_id)
        if not item:
            item_data = data.model_dump(exclude_unset=True)
            item_data["item_id"] = item_id
            item = Item(**item_data)
            await item.save()
            return item
        else:
            for key, value in data.model_dump(exclude_unset=True).items():
                setattr(item, key, value)
            await item.save()
            return item
    
    @staticmethod
    async def update_cafe(cafe_slug: str, data: CafeUpdate):
        cafe = await RecommendationService.get_cafe(cafe_slug)
        if not cafe:
            cafe_data = data.model_dump(exclude_unset=True)
            cafe_data["slug"] = cafe_slug
            cafe = CafeForRecommendation(**cafe_data)
            await cafe.save()
            return cafe
        else:
            for key, value in data.model_dump(exclude_unset=True).items():
                setattr(cafe, key, value)
            await cafe.save()
            return cafe

    @staticmethod
    async def get_user_personnal_recommendations_by_id(user_id: str, cafe_slug: str):
        user = await RecommendationService.get_user(user_id)
        if not user:
            raise ValueError("User not found")
        personnal_recommendations = user.personnal_recommendations
        cafe = list(filter(lambda x: x.cafe_slug == cafe_slug, personnal_recommendations))
        if cafe:
            return cafe[0].recommendation
        raise ValueError("Cafe not found")
    
    @staticmethod
    async def update_user(user_id: str, data: UserRecommendationUpdate):
        user = await RecommendationService.get_user(user_id)
        if not user:
            user_data = data.model_dump(exclude_unset=True)
            user_data["user_id"] = user_id
            user = UserRecommendation(**user_data)
            await user.save()
            return user
        else:
            for key, value in data.model_dump(exclude_unset=True).items():
                setattr(user, key, value)
            await user.save()
            return user
        
    @staticmethod
    async def get_user_cafe_recommendations(user_id: str):
        user = await RecommendationService.get_user(user_id)
        if not user:
            raise ValueError("User not found")
        return user.cafe_recommendations
    
    #-------------------------- 
    #          Public
    #--------------------------

    @staticmethod
    async def get_public_recommendations(cafe_slug: str):
        cafe = await RecommendationService.get_cafe(cafe_slug)
        if cafe:
            return cafe.public_recommendations
        raise ValueError("Cafe not found")
    
# --------------------------------------
#         Cafe recommendations
# --------------------------------------

    # @staticmethod
    # async def get_user_cafe_recommendations(user_id: str):
    #     return await CafeRecommendation.find_one({ "user_id": user_id })
    
    # @staticmethod
    # async def update_user_cafe_recommendations(user_id: str, data: CafeRecommendationUpdate):
    #     update_data = data.model_dump(exclude_unset=True)
    #     recommendations = await RecommendationService.get_user_cafe_recommendations(user_id)
    #     if recommendations:
    #         await recommendations.update(update_data)
    #     else:
    #         raise ValueError("Recommendation not found")
    #     return recommendations
