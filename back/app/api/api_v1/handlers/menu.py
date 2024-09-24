from uuid import UUID
from fastapi import (
    APIRouter,
    HTTPException,
    Path,
    Query,
    status,
    Request,
    Depends
)
from app.models.cafe_model import Role
from app.schemas.menu_schema import MenuItemOut, MenuItemCreate, MenuItemUpdate
from app.services.cafe_service import CafeService
from app.services.menu_service import MenuItemService
from app.models.user_model import User
from app.api.deps.user_deps import get_current_user
from typing import List, Dict, Optional

"""
This module defines the API routes related to menu items for cafes.
"""

menu_router = APIRouter()


def parse_query_params(query_params: Dict) -> Dict:
    """
    Parses and converts the query parameters to the appropriate data types based on the values.

    Args:
        query_params (Dict): A dictionary containing the query parameters to be parsed.

    Returns:
        Dict: A dictionary with the parsed query parameters where values are converted to their appropriate types.
    """
    parsed_params = {}
    for key, value in query_params.items():
        if value.lower() == "true":
            value = True
        elif value.lower() == "false":
            value = False
        elif "," in value:
            value = value.split(",")
        elif "," in value:
            value = [
                float(v) if v.replace(".", "", 1).isdigit() else v
                for v in value.split(",")
            ]
        elif value.replace(".", "", 1).isdigit():
            value = float(value)

        if "__" in key:
            parts = key.split("__")
            if parts[-1] in ["eq", "gt", "gte", "in", "lt", "lte", "ne", "nin"]:
                field = "__".join(parts[:-1])
                op = "$" + parts[-1]
                parsed_params[field] = {op: value}
            else:
                parsed_params[key] = value
        else:
            parsed_params[key] = value
    return parsed_params



@menu_router.get(
    "/cafes/{cafe_slug}/menu",
    response_model=List[MenuItemOut],
    summary="List Menu Items",
    description="Retrieve the menu items of a specific café using its slug or UUID.",
)
async def list_menu_items(
    request: Request,
    cafe_slug: str = Path(..., description="The slug or UUID of the cafe"),
    in_stock: Optional[bool] = Query(
        None, description="Filter menu items by stock availability (true/false)."
    ),
    sort_by: Optional[str] = Query(
        None,
        description="Sort menus by a specific field. Prefix with '-' for descending order (e.g., '-name').",
    ),
    page: Optional[int] = Query(
        1, description="Specify the page number for pagination."
    ),
    limit: Optional[int] = Query(
        40, description="Set the number of cafes to return per page."
    ),
):
    """
    Retrieve the menu items of a specific café using its slug or UUID.

    Args:
        - request: Request - The HTTP request object.
        - cafe_slug: str - The slug or UUID of the cafe.
        - in_stock: Optional[bool] - Filter menu items by stock availability (true/false).
        - sort_by: Optional[str] - Sort menus by a specific field. Prefix with '-' for descending order (e.g., '-name').
        - page: Optional[int] - Specify the page number for pagination.
        - limit: Optional[int] - Set the number of cafes to return per page.

    Raises:
        - HTTPException: If the menu is not found for the given café.

    Returns:
        - List[MenuItemOut]: A list of menu items for the specified café.
    """
    query_params = dict(request.query_params)
    parsed_params = parse_query_params(query_params)

    # Retrieve the cafe by slug or UUID
    cafe = await CafeService.retrieve_cafe(cafe_slug)
    if not cafe:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Cafe not found")
    parsed_params["cafe_id"] = cafe.cafe_id

    return await MenuItemService.list_menu_items(**parsed_params)


@menu_router.get(
    "/menu/{item_id}",
    response_model=MenuItemOut,
    summary="Get Menu Item",
    description="Retrieve detailed information about a specific menu item.",
)
async def get_menu_item(
    item_id: UUID = Path(..., description="The UUID of the menu item"),
):
    """
    Get detailed information about a specific menu item.

    Args:
        - item_id (UUID): The UUID of the menu item.

    Raises:
        - HTTPException: If the menu item is not found.

    Returns:
        - MenuItemOut: The detailed information about the menu item.
    """
    item = await MenuItemService.retrieve_menu_item(item_id)
    if not item:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Menu item not found."
        )
    return item


@menu_router.post(
    "/cafes/{cafe_slug}/menu",
    response_model=MenuItemOut,
    summary="🔴 Create Menu Item",
    description="Create a new menu item for the specified café.",
)
async def create_menu_item(
    item: MenuItemCreate,
    cafe_slug: str = Path(..., description="The slug or UUID of the cafe"),
    current_user: User = Depends(get_current_user),
):
    """
    Create a new menu item for the specified café.

    Args:
        item (MenuItemCreate): The menu item to create.
        cafe_slug (str): The slug or UUID of the cafe.
        current_user (User): The current user making the request.

    Raises:
        HTTPException: If the cafe is not found or access is forbidden.

    Returns:
        MenuItemOut: The created menu item.
    """
    try:
        await CafeService.is_authorized_for_cafe_action(
            cafe_slug, current_user, [Role.ADMIN]
        )
        cafe = await CafeService.retrieve_cafe(cafe_slug)
        return await MenuItemService.create_menu_item(cafe.cafe_id, item)
    except ValueError as e:
        if str(e) == "Cafe not found":
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
        elif str(e) == "Access forbidden":
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=str(e))
        else:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=str(e))


@menu_router.put(
    "/menu/{item_id}",
    response_model=MenuItemOut,
    summary="🟢 Update Menu Item",
    description="Update the details of an existing menu item.",
)
async def update_menu_item(
    item: MenuItemUpdate,
    item_id: UUID = Path(..., description="The UUID of the menu item"),
    current_user: User = Depends(get_current_user),
):
    """
    Update the details of an existing menu item.

    Args:
        item (MenuItemUpdate): The updated menu item.
        item_id (UUID): The UUID of the menu item.
        current_user (User): The current user making the request.

    Raises:
        HTTPException: If the menu item or cafe is not found or access is forbidden.

    Returns:
        MenuItemOut: The updated menu item.
    """
    # Retrieve the menu item
    item = await MenuItemService.retrieve_menu_item(item_id)
    if not item:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Menu item not found."
        )

    # Retrieve cafe id from the item and check authorization
    cafe_id = item.cafe_id
    try:
        await CafeService.is_authorized_for_cafe_action(cafe_id, current_user, [Role.ADMIN, Role.VOLUNTEER])
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=str(e))

    # Proceed with the update
    try:
        updated_item = await MenuItemService.update_menu_item(item_id, item)
        return updated_item
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=str(e))


@menu_router.delete(
    "/menu/{item_id}",
    summary="🔴 Delete Menu Item",
    description="Delete a specific menu item.",
)
async def delete_menu_item(
    item_id: UUID = Path(..., description="The UUID of the menu item"),
    current_user: User = Depends(get_current_user),
):
    """
    Delete a specific menu item.

    Args:
        item_id (UUID): The UUID of the menu item.
        current_user (User): The current user making the request.

    Raises:
        HTTPException: If the menu item or cafe is not found or access is forbidden.

    Returns:
        dict: A dictionary containing a message indicating the success of the deletion.
    """
    # Retrieve the menu item
    item = await MenuItemService.retrieve_menu_item(item_id)
    if not item:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Menu item not found."
        )

    # Retrieve cafe id from the item and check authorization
    cafe_id = item.cafe_slug
    try:
        await CafeService.is_authorized_for_cafe_action(cafe_id, current_user, [Role.ADMIN])
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=str(e))

    await MenuItemService.delete_menu_item(item_id)
    return {"message": f"Item {item_id} has been successfully deleted."}
