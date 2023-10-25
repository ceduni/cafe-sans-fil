from typing import Optional
from uuid import UUID
from app.models.user_model import User
from app.schemas.user_schema import UserAuth, UserUpdate
from app.core.security import get_password, verify_password

class UserService:
    """
    Service class that provides methods for CRUD operations related to Auth and Users.
    """

    # --------------------------------------
    #               Auth
    # --------------------------------------

    @staticmethod
    async def authenticate(credential: str, password: str) -> Optional[User]:
        if '@' in credential:
            user = await UserService.get_user_by_email(email=credential)
        else:
            user = await UserService.get_user_by_username(username=credential)

        if not user:
            return None
        if not verify_password(password=password, hashed_pass=user.hashed_password):
            return None

        return user
    
    @staticmethod
    async def authenticateByUsername(username: str, password: str) -> Optional[User]:
        user = await UserService.get_user_by_username(username=username)
        if not user:
            return None
        if not verify_password(password=password, hashed_pass=user.hashed_password):
            return None
        
        return user
    
    @staticmethod
    async def authenticateByEmail(email: str, password: str) -> Optional[User]:
        user = await UserService.get_user_by_email(email=email)
        if not user:
            return None
        if not verify_password(password=password, hashed_pass=user.hashed_password):
            return None
        
        return user

    @staticmethod
    async def get_user_by_email(email: str) -> Optional[User]:
        user = await User.find_one(User.email == email)
        return user
    
    @staticmethod
    async def get_user_by_username(username: str) -> Optional[User]:
        user = await User.find_one(User.username == username)
        return user

    @staticmethod
    async def get_user_by_id(id: UUID) -> Optional[User]:
        user = await User.find_one(User.user_id == id)
        return user

    # --------------------------------------
    #               User
    # --------------------------------------

    @staticmethod
    async def list_users():
        return await User.find().to_list()
    
    @staticmethod
    async def create_user(user: UserAuth):
        user_in = User(
            email=user.email,
            matricule=user.matricule,
            username=user.username,
            hashed_password=get_password(user.password),
            first_name=user.first_name,
            last_name=user.last_name,
        )
        await user_in.save()
        return user_in
    
    @staticmethod
    async def retrieve_user(user_id: UUID):
        return await User.find_one(User.user_id == user_id)

    @staticmethod
    async def update_user(user_id: UUID, data: UserUpdate) -> User:
        user = await UserService.retrieve_user(user_id)
        await user.update({"$set": data.dict(exclude_unset=True)})
        return user

