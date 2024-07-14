from app.schemas.recommendation_schema import ItemRecommendationUpdate, CafeRecommendationUpdate, ItemUpdate
from app.models.recommendations.user_recommendation_model import UserRecommendation
from app.models.recommendations.public_recommendation_model import PublicRecommendation
from app.models.recommendations.bot_recommendation_model import BotRecommendation
from app.models.recommendations.cafe_recommendation_model import CafeRecommendation

class RecommendationService:

    @staticmethod
    async def get_recommendations_by_id(user_id: str, cafe_slug: str):
        return await UserRecommendation.find_one({ "user_id": user_id, "cafe_slug": cafe_slug })

    @staticmethod
    async def update_user_recommendations(user_id: str, cafe_slug: str, data: ItemRecommendationUpdate):
        update_data = data.model_dump(exclude_unset=True)
        recommendations = await RecommendationService.get_recommendations_by_id(user_id, cafe_slug)
        await recommendations.update(update_data)
        return recommendations

    @staticmethod
    async def get_public_recommendations(cafe_slug: str):
        return await PublicRecommendation.find_one({ "cafe_slug": cafe_slug })

    @staticmethod
    async def update_public_recommendations(cafe_slug: str, data: ItemRecommendationUpdate):
        update_data = data.model_dump(exclude_unset=True)
        recommendations = await RecommendationService.get_public_recommendations(cafe_slug)
        await recommendations.update(update_data)
        return recommendations

    @staticmethod
    async def get_bot_recommendations(cafe_slug: str):
        return await BotRecommendation.find_one({ "cafe_slug": cafe_slug })

    @staticmethod
    async def update_bot_recommendations(cafe_slug: str, data: ItemRecommendationUpdate):
        recommendations = BotRecommendation(cafe_slug=cafe_slug, **data.model_dump(exclude_unset=True))
        print(recommendations)
        await recommendations.save()
        return recommendations

    @staticmethod
    async def get_user_cafe_recommendations(user_id: str):
        return await CafeRecommendation.find_one({ "user_id": user_id })
    
    @staticmethod
    async def update_user_cafe_recommendations(user_id: str, data: CafeRecommendationUpdate):
        update_data = data.model_dump(exclude_unset=True)
        recommendations = await RecommendationService.get_user_cafe_recommendations(user_id)
        if recommendations:
            await recommendations.update(update_data)
        else:
            raise ValueError("Recommendation not found")
        return recommendations
    
    @staticmethod
    async def get_all_items():
        pass

    @staticmethod
    async def update_item_cluster(item_slug: str, data: ItemUpdate):
        pass

