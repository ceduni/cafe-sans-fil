from typing import List
from app.schemas.recommendation_schema import RecommendationUpdate

#TODO
class RecommendationService:

    @staticmethod
    def get_recommendations_by_id(user_id: str, cafe_slug: str):
        pass

    @staticmethod
    def update_user_recommendations(user_id: str, cafe_slug: str, data: RecommendationUpdate):
        pass

    @staticmethod
    def get_public_recommendations(cafe_slug: str):
        pass

    @staticmethod
    def update_public_recommendations(cafe_slug: str, data: RecommendationUpdate):
        pass

    @staticmethod
    def get_bot_recommendations(cafe_slug: str):
        pass

    @staticmethod
    def update_bot_recommendations(cafe_slug: str, data: RecommendationUpdate):
        pass

