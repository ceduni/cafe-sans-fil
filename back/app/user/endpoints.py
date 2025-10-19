"""
Module for handling user-related routes.
"""

from typing import Optional, TypeVar, List

from beanie import PydanticObjectId
from fastapi import APIRouter, Depends, HTTPException, Path, Query, Request, status
from fastapi_pagination import Params
from fastapi_pagination.customization import CustomizedPage, UseParams
from fastapi_pagination.ext.beanie import paginate
from fastapi_pagination.links import Page
from pymongo.errors import DuplicateKeyError

from app.auth.dependencies import get_current_user, get_current_user_aggregate
from app.models import ErrorConflictResponse, ErrorResponse
from app.service import parse_query_params
from app.user.models import User, UserAggregateOut, UserOut, UserUpdate, FavoriteRequest, FavoriteType, BulkFavoriteRequest, FavoriteResponse
from app.user.service import UserService

T = TypeVar("T")


class UserParams(Params):
    """Custom pagination parameters."""

    size: int = Query(20, ge=1, le=100, description="Page size")
    page: int = Query(1, ge=1, description="Page number")
    sort_by: Optional[str] = Query(None, description="Sort by a specific field")


UserPage = CustomizedPage[
    Page[T],
    UseParams(UserParams),
]


user_router = APIRouter()


@user_router.get(
    "/users/@me",
    response_model=UserAggregateOut,
    responses={
        401: {"model": ErrorResponse},
    },
)
async def get_current_user(
    current_user: User = Depends(get_current_user_aggregate),
):
    """Get current user. (`MEMBER`)"""
    return current_user


@user_router.get(
    "/users/@me/favorites",
    summary="Get current user's favorite cafes or items",
    response_model=List[PydanticObjectId],
    responses={ 401: {"model": ErrorResponse} },
)
async def get_current_user_favorites(
    type: FavoriteType = Query(..., description="Type of favorite to retrieve"),
    current_user: User = Depends(get_current_user_aggregate),
):
    if type == FavoriteType.CAFE:
        return current_user.favorite_cafes
    if type == FavoriteType.ITEM:
        return current_user.favorite_items

@user_router.post(
    "/users/@me/favorites",
    summary="Add a single favorite",
    response_model=FavoriteResponse,
    responses={401: {"model": ErrorResponse}},
)
async def add_favorites(
    data: FavoriteRequest,
    current_user: User = Depends(get_current_user_aggregate),
):
    if data.type == FavoriteType.CAFE:
        await UserService.add_favorite_cafe(current_user, [data.id])
    if data.type == FavoriteType.ITEM:
        await UserService.add_favorite_item(current_user, [data.id])
    else:
        raise HTTPException(status_code=400, detail="Invalid favorite type.")

    return FavoriteResponse(
        type = data.type,
        ids = [data.id],
        status="added"
    )

@user_router.delete(
    "/users/@me/favorites",
    response_model=FavoriteResponse,
    responses={401: {"model": ErrorResponse}},
)
async def remove_favorites(
    data: FavoriteRequest,
    current_user: User = Depends(get_current_user_aggregate),
):
    if data.type == FavoriteType.CAFE:
        await UserService.remove_favorite_cafe(current_user, [data.id])
    if data.type == FavoriteType.ITEM:
        await UserService.remove_favorite_item(current_user, [data.id])
    else:
        raise HTTPException(status_code=400, detail="Invalid favorite type.")

    return FavoriteResponse(
        type = data.type,
        ids = [data.id],
        status="removed"
    )


@user_router.patch(
    "/users/@me/favorites",
    response_model=FavoriteResponse,
    summary="Toggle a favorite item or cafe",
)
async def toggle_user_favorite(
    data: FavoriteRequest,
    current_user: User = Depends(get_current_user_aggregate),
):
    if data.type == FavoriteType.CAFE:
        result = await UserService.toggle_favorite_cafe(current_user, data.id)
    if data.type == FavoriteType.ITEM:
        result = await UserService.toggle_favorite_item(current_user, data.id)
    else:
        raise HTTPException(status_code=400, detail="Invalid favorite type.")

    return FavoriteResponse(
        type = data.type,
        ids = [data.id],
        status = result.action
    )
    
    
@user_router.post(
    "/users/@me/favorites/bulk",
    response_model=FavoriteResponse,
)
async def add_bulk_favorites(
    data: BulkFavoriteRequest,
    current_user: User = Depends(get_current_user_aggregate),
):
    if data.type == FavoriteType.CAFE:
        await UserService.add_favorite_cafe(current_user, data.ids)
    if data.type == FavoriteType.ITEM:
        await UserService.add_favorite_item(current_user, data.ids)
    else:
        raise HTTPException(status_code=400, detail="Invalid favorite type.")
    
    return FavoriteResponse(
        type = data.type,
        ids = data.ids,
        status="added"
    )

@user_router.delete(
    "/users/@me/favorites/bulk",
    response_model=FavoriteResponse,
)
async def remove_bulk_favorites(
    data: BulkFavoriteRequest,
    current_user: User = Depends(get_current_user_aggregate),
):
    if data.type == FavoriteType.CAFE:
        await UserService.remove_favorite_cafe(current_user, data.ids)
    if data.type == FavoriteType.ITEM:
        await UserService.remove_favorite_item(current_user, data.ids)
    else:
        raise HTTPException(status_code=400, detail="Invalid favorite type.")
    
    return FavoriteResponse(
        type = data.type,
        ids = data.ids,
        status="removed"
    )


@user_router.put(
    "/users/@me",
    response_model=UserOut,
    responses={
        401: {"model": ErrorResponse},
        409: {"model": ErrorConflictResponse},
    },
)
async def update_current_user(
    data: UserUpdate,
    current_user: User = Depends(get_current_user),
):
    """Update current user. (`MEMBER`)"""
    try:
        return await UserService.update(current_user, data)
    except DuplicateKeyError as e:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=[
                {
                    "msg": "User with these fields already exists.",
                    "fields": list(e.details.get("keyPattern", {}).keys()),
                }
            ],
        )


@user_router.delete(
    "/users/@me",
    status_code=status.HTTP_204_NO_CONTENT,
    responses={
        401: {"model": ErrorResponse},
    },
)
async def delete_my_account(
    current_user: User = Depends(get_current_user),
):
    """Delete my account permanently from the database. (`MEMBER`)"""
    await UserService.delete_my_account(current_user)


@user_router.get(
    "/users/{id}",
    response_model=UserAggregateOut,
    responses={
        401: {"model": ErrorResponse},
        404: {"model": ErrorResponse},
    },
)
async def get_user(
    id: PydanticObjectId = Path(..., description="ID of the user"),
):
    """Get a user. (`MEMBER`)"""
    user = await UserService.get_by_id(
        id=id,
        aggregate=True,
    )

    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=[{"msg": "User with this ID does not exist."}],
        )
    return user

@user_router.put(
    "/users/@me/cafes",
    response_model=UserAggregateOut,
    responses={
        401: {"model": ErrorResponse},
        403: {"model": ErrorResponse},
        404: {"model": ErrorResponse},
        409: {"model": ErrorConflictResponse},
    },
)
async def update_my_cafes(
    cafe_id: str = Query(..., description="ID of the cafe to add to favorites"),
    current_user: User = Depends(get_current_user),
):
    """Add a cafe to my favorites. (`MEMBER`)"""
    try:
        updated_user = await UserService.add_favorite_cafe(current_user, cafe_id)
        # Fetch aggregated user with populated cafes
        return await UserService.get_by_id(updated_user.id, aggregate=True)
    except DuplicateKeyError as e:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=[
                {
                    "msg": "User with these fields already exists.",
                    "fields": list(e.details.get("keyPattern", {}).keys()),
                }
            ],
        )

@user_router.delete(
    "/users/@me/cafes",
    response_model=UserAggregateOut,
    responses={
        401: {"model": ErrorResponse},
        403: {"model": ErrorResponse},
        404: {"model": ErrorResponse},
        409: {"model": ErrorConflictResponse},
    },
)
async def delete_my_cafes(
    cafe_id: str = Query(..., description="ID of the cafe to remove from favorites"),
    current_user: User = Depends(get_current_user),
):
    """Remove a cafe from my favorites. (`MEMBER`)"""
    try:
        updated_user = await UserService.remove_favorite_cafe(current_user, cafe_id)
        # Fetch aggregated user with populated cafes
        return await UserService.get_by_id(updated_user.id, aggregate=True)
    except DuplicateKeyError as e:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=[
                {
                    "msg": "User with these fields already exists.",
                    "fields": list(e.details.get("keyPattern", {}).keys()),
                }
            ],
        )


@user_router.put(
    "/users/@me/articles",
    response_model=UserAggregateOut,
    responses={
        401: {"model": ErrorResponse},
        403: {"model": ErrorResponse},
        404: {"model": ErrorResponse},
        409: {"model": ErrorConflictResponse},
    },
)
async def update_my_articles(
    data: ArticleFavoriteRequest,
    current_user: User = Depends(get_current_user),
):
    """Add an article to my favorites. (`MEMBER`)"""
    try:
        updated_user = await UserService.add_articles_favs(current_user, data.article_id, data.cafe_id)
        # Fetch aggregated user with populated cafes
        return await UserService.get_by_id(updated_user.id, aggregate=True)
    except DuplicateKeyError as e:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=[
                {
                    "msg": "User with these fields already exists.",
                    "fields": list(e.details.get("keyPattern", {}).keys()),
                }
            ],
        )
    
@user_router.delete(
    "/users/@me/articles",
    response_model=UserAggregateOut,
    responses={
        401: {"model": ErrorResponse},
        403: {"model": ErrorResponse},
        404: {"model": ErrorResponse},
        409: {"model": ErrorConflictResponse},
    },
)
async def delete_my_articles(
    data: ArticleFavoriteRequest,
    current_user: User = Depends(get_current_user),
):
    """Remove an article from my favorites. (`MEMBER`)"""
    try:
        updated_user = await UserService.remove_articles_favs(current_user, data.article_id, data.cafe_id)
        # Fetch aggregated user with populated cafes
        return await UserService.get_by_id(updated_user.id, aggregate=True)
    except DuplicateKeyError as e:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=[
                {
                    "msg": "User with these fields already exists.",
                    "fields": list(e.details.get("keyPattern", {}).keys()),
                }
            ],
        )



@user_router.put(
    "/users/{id}",
    response_model=UserOut,
    responses={
        401: {"model": ErrorResponse},
        403: {"model": ErrorResponse},
        404: {"model": ErrorResponse},
        409: {"model": ErrorConflictResponse},
    },
)
async def update_user(
    data: UserUpdate,
    id: PydanticObjectId = Path(..., description="ID of the user"),
    current_user: User = Depends(get_current_user),
):
    """Update a user. (`MEMBER`)"""
    user = await UserService.get_by_id(id)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=[{"msg": "User with this ID does not exist."}],
        )

    if id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=[{"msg": "You can only update your own profile"}],
        )

    try:
        return await UserService.update(user, data)
    except DuplicateKeyError as e:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=[
                {
                    "msg": "User with these fields already exists.",
                    "fields": list(e.details.get("keyPattern", {}).keys()),
                }
            ],
        )


@user_router.delete(
    "/users/{id}",
    responses={
        401: {"model": ErrorResponse},
        403: {"model": ErrorResponse},
        404: {"model": ErrorResponse},
    },
)
async def delete_user(
    id: PydanticObjectId = Path(..., description="ID of the user"),
    current_user: User = Depends(get_current_user),
):
    """Delete a user. (`MEMBER`)"""
    user = await UserService.get_by_id(id)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=[{"msg": "User with this ID does not exist."}],
        )

    if id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=[{"msg": "You can only delete your own profile"}],
        )

    await UserService.delete(user)
