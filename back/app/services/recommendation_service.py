from app.models.user_recommendations_model import UserRecommendation
from app.models.cafe_recommendations_model import CafeForRecommendation
from app.schemas.recommendation_schema import CafeUpdate
class RecommendationService:

    #-------------------------- 
    #          Utils
    #--------------------------

    @staticmethod
    async def get_user(user_id: str):
        return await UserRecommendation.find_one({ "user_id": user_id })
    
    @staticmethod
    async def get_cafe(cafe_slug: str):
        return await CafeForRecommendation.find_one({ "slug": cafe_slug })
    
    @staticmethod
    async def update_cafe(cafe_slug: str, data: CafeUpdate):
        cafe = await RecommendationService.get_cafe(cafe_slug)
        if cafe:
            for key, value in data.model_dump(exclude_unset=True).items():
                setattr(cafe, key, value)
            await cafe.save()
        else:
            cafe_data = data.model_dump(exclude_unset=True)
            cafe_data["slug"] = cafe_slug
            cafe = CafeForRecommendation(**cafe_data)
            await cafe.insert()
        return cafe
    

    # @staticmethod
    # async def get_user_recommendations(user_id: str):
    #     user = await UserRecommendation.find_one({ "user_id": user_id })
    #     return user

    # @staticmethod
    # async def get_user_recommendations_by_id(user_id: str, cafe_slug: str):
    #     user = await RecommendationService.get_user(user_id)
    #     cafe_list = user.personnal_recommendations
    #     selected_cafe = list( filter(lambda x: x.slug == cafe_slug, cafe_list) )[0]
    #     return selected_cafe.items_recommended
    
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
#         Bot recommendations
# --------------------------------------
    @staticmethod
    async def get_bot_recommendations(cafe_slug: str):
        cafe = await RecommendationService.get_cafe(cafe_slug)
        if cafe:
            return cafe.bot_recommendations
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

