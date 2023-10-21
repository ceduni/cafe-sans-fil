from uuid import UUID
from app.models.user_model import User as UserModel
from app.schemas.user_schema import User

class UserService:
    """
    Service class that provides methods for CRUD operations related to Users.
    """
    
    # --------------------------------------
    #               User
    # --------------------------------------

    @staticmethod
    async def create_user(data: User) -> UserModel:
        user = UserModel(**data.dict())
        await user.insert()
        return user

    @staticmethod
    async def retrieve_user(user_id: UUID) -> UserModel:
        return await UserModel.find_one(UserModel.user_id == user_id)

    @staticmethod
    async def update_user(user_id: UUID, data: User) -> UserModel:
        user = await UserService.retrieve_user(user_id)
        await user.update({"$set": data.dict(exclude_unset=True)})
        return user
