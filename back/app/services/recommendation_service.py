from typing import List
from app.schemas.recommendation_schema import RecommendationUpdate
from back.app.models.user_recommendation_model import UserRecommendation
from back.app.models.public_recommendation_model import PublicRecommendation
from back.app.models.bot_recommendation_model import BotRecommendation

class RecommendationService:

    @staticmethod
    async def get_recommendations_by_id(user_id: str, cafe_slug: str):
        return await UserRecommendation.find_one({ "user_id": user_id, "cafe_slug": cafe_slug })

    @staticmethod
    async def update_user_recommendations(user_id: str, cafe_slug: str, data: RecommendationUpdate):
        update_data = data.model_dump(exclude_unset=True)
        recommendations = await RecommendationService.get_recommendations_by_id(user_id, cafe_slug)
        await recommendations.update(update_data)
        return recommendations

    @staticmethod
    async def get_public_recommendations(cafe_slug: str):
        return await PublicRecommendation.find_one({ "cafe_slug": cafe_slug })

    @staticmethod
    async def update_public_recommendations(cafe_slug: str, data: RecommendationUpdate):
        update_data = data.model_dump(exclude_unset=True)
        recommendations = await RecommendationService.get_public_recommendations(cafe_slug)
        await recommendations.update(update_data)
        return recommendations

    @staticmethod
    async def get_bot_recommendations(cafe_slug: str):
        return await BotRecommendation.find_one({ "cafe_slug": cafe_slug })

    @staticmethod
    async def update_bot_recommendations(cafe_slug: str, data: RecommendationUpdate):
        update_data = data.model_dump(exclude_unset=True)
        recommendations = await RecommendationService.get_bot_recommendations(cafe_slug)
        await recommendations.update(update_data)
        return recommendations

