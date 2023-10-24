from uuid import UUID
from app.models.user_model import User
from app.schemas.user_schema import UserCreate, UserUpdate

class UserService:
    """
    Service class that provides methods for CRUD operations related to Users.
    """
    
    # --------------------------------------
    #               User
    # --------------------------------------

    @staticmethod
    async def create_user(data: UserCreate):
        user = User(**data.dict())
        await user.insert()
        return user

    @staticmethod
    async def retrieve_user(user_id: UUID):
        return await User.find_one(User.user_id == user_id)

    @staticmethod
    async def update_user(user_id: UUID, data: UserUpdate) -> User:
        user = await UserService.retrieve_user(user_id)
        await user.update({"$set": data.dict(exclude_unset=True)})
        return user
