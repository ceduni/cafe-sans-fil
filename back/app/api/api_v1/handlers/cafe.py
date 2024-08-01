from fastapi import (
    APIRouter,
    HTTPException,
    Path,
    Query,
    status,
    Request,
    Depends,
    UploadFile,
)
from app.models.cafe_model import Role
from app.schemas.cafe_schema import (
    CafeOut,
    CafeShortOut,
    CafeCreate,
    CafeUpdate,
    MenuItemOut,
    MenuItemCreate,
    MenuItemUpdate,
    StaffCreate,
    StaffUpdate,
    StaffOut,
)
from app.services.cafe_service import CafeService
from app.services.order_service import OrderService
from app.services.user_service import UserService
from app.models.user_model import User
from app.api.deps.user_deps import get_current_user
from typing import List, Dict, Optional
import json

"""
This module defines the API routes related to cafes, their menus, and a unified search function for cafes and menu items.
"""

cafe_router = APIRouter()


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


# --------------------------------------
#               Cafe
# --------------------------------------


@cafe_router.get(
    "/cafes",
    response_model=List[CafeShortOut],
    summary="List Cafes",
    description="Retrieve a list of all cafes with short information.",
)
async def list_cafes(
    request: Request,
    is_open: Optional[bool] = Query(
        None, description="Filter cafes by open status (true/false)."
    ),
    sort_by: Optional[str] = Query(
        "name",
        description="Sort cafes by a specific field. Prefix with '-' for descending order (e.g., '-name').",
    ),
    page: Optional[int] = Query(
        1, description="Specify the page number for pagination."
    ),
    limit: Optional[int] = Query(
        40, description="Set the number of cafes to return per page."
    ),
):
    """
    Retrieve a list of all cafes with short information.

    Args:
        - request: Request
        - is_open: Optional[bool] (default: None) - Filter cafes by open status (true/false).
        - sort_by: Optional[str] (default: "name") - Sort cafes by a specific field. Prefix with '-' for descending order (e.g., '-name').
        - page: Optional[int] (default: 1) - Specify the page number for pagination.
        - limit: Optional[int] (default: 40) - Set the number of cafes to return per page.

    Returns:
        - List[CafeShortOut]: A list of cafes with short information.
    """
    query_params = dict(request.query_params)
    parsed_params = parse_query_params(query_params)
    return await CafeService.list_cafes(**parsed_params)


@cafe_router.get(
    "/cafes/{cafe_id_or_slug}",
    response_model=CafeOut,
    summary="Get Cafe",
    description="Retrieve detailed information about a specific cafe.",
)
async def get_cafe(
    cafe_id_or_slug: str = Path(
        ..., description="The UUID or slug of the cafe to retrieve"
    )
):
    """
    Retrieve detailed information about a specific cafe.

    Args:
        cafe_id_or_slug (str): The UUID or slug of the cafe to retrieve.

    Raises:
        HTTPException: If the cafe is not found.

    Returns:
        CafeOut: The detailed information about the cafe.
    """
    cafe = await CafeService.retrieve_cafe(cafe_id_or_slug)
    if not cafe:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Café not found"
        )

    return cafe


@cafe_router.post(
    "/cafes",
    response_model=CafeOut,
    summary="⚫ Create Cafe",
    description="Create a new cafe with the provided information. \n\nAuthorization: Only cafesansfil can create cafe.",
    include_in_schema=False,
)
async def create_cafe(cafe: CafeCreate, current_user: User = Depends(get_current_user)):
    """
    Create a new cafe with the provided information.

    This endpoint allows the creation of a new cafe with the provided information. Only users with the username '7802085' are authorized to create a cafe.

    Args:
        - cafe (CafeCreate): The information of the cafe to be created.
        - current_user (User, optional): The currently authenticated user. Defaults to the user returned by the `get_current_user` dependency.

    Raises:
        - HTTPException: If the user is not authorized to create a cafe. The status code is 403 FORBIDDEN and the detail is 'Access forbidden'.
        - HTTPException: If the cafe already exists. The status code is 409 CONFLICT and the detail is 'Cafe already exists'.
        - HTTPException: If there is a duplicate value in the cafe information. The status code is 409 CONFLICT and the detail is the specific duplicate value.

    Returns:
        - CafeOut: The created cafe with detailed information.
    """
    # Authorization check
    if "7802085" != current_user.username:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail="Access forbidden"
        )
    try:
        return await CafeService.create_cafe(cafe)
    except ValueError as e:
        if "duplicate" in str(e).lower() and len(str(e)) < 100:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=str(e))

        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT, detail="Cafe already exists"
        )


@cafe_router.put(
    "/cafes/{cafe_id_or_slug}",
    response_model=CafeOut,
    summary="🔴 Update Cafe",
    description="Update the details of an existing cafe.",
)
async def update_cafe(
    cafe: CafeUpdate,
    cafe_id_or_slug: str = Path(
        ..., description="The UUID or slug of the cafe to update"
    ),
    current_user: User = Depends(get_current_user),
):
    """
    Update the details of an existing cafe.

    Args:
        - cafe (CafeUpdate): The updated cafe information.
        - cafe_id_or_slug (str): The UUID or slug of the cafe to update.
        - current_user (User): The current user making the request.

    Raises:
        - HTTPException: If the cafe is not found. The status code is 404 NOT FOUND and the detail is 'Café not found'.
        - HTTPException: If the user is not authorized to update the cafe. The status code is 403 FORBIDDEN and the detail is 'Access forbidden'.
        - HTTPException: If there is a duplicate value in the cafe information. The status code is 409 CONFLICT and the detail is the specific duplicate value.
        - HTTPException: If the cafe already exists. The status code is 409 CONFLICT and the detail is 'Cafe already exists'.

    Returns:
        - CafeOut: The updated cafe with detailed information.
    """
    cafe_exists = await CafeService.retrieve_cafe(cafe_id_or_slug)
    if not cafe_exists:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Café not found"
        )

    try:
        await CafeService.is_authorized_for_cafe_action_by_slug(
            cafe_id_or_slug, current_user, [Role.ADMIN]
        )
        return await CafeService.update_cafe(cafe_id_or_slug, cafe)
    except ValueError as e:
        if str(e) == "Cafe not found":
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
        elif str(e) == "Access forbidden":
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=str(e))
        elif "duplicate" in str(e).lower() and len(str(e)) < 100:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=str(e))
        else:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT, detail="Cafe already exists"
            )


# --------------------------------------
#               Menu
# --------------------------------------


@cafe_router.get(
    "/cafes/{cafe_id_or_slug}/menu",
    response_model=List[MenuItemOut],
    summary="List Menu Items",
    description="Retrieve the menu items of a specific café.",
)
async def list_menu_items(
    request: Request,
    cafe_id_or_slug: str = Path(..., description="The UUID or slug of the cafe"),
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
    Retrieve the menu items of a specific café.

    Args:
        - request: Request - The HTTP request object.
        - cafe_id_or_slug: str - The UUID or slug of the cafe.
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
    query_params["cafe_id_or_slug"] = cafe_id_or_slug
    parsed_params = parse_query_params(query_params)
    menu = await CafeService.list_menu_items(**parsed_params)
    if not menu:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Menu not found for the given café.",
        )
    return menu


@cafe_router.get(
    "/cafes/{cafe_slug}/menu/{item_slug}",
    response_model=MenuItemOut,
    summary="Get Menu Item",
    description="Retrieve detailed information about a specific menu item.",
)
async def get_menu_item(
    cafe_slug: str = Path(..., description="The slug of the cafe"),
    item_slug: str = Path(..., description="The slug of the menu item"),
):
    """
    Get detailed information about a specific menu item.

    Args:
        - cafe_slug (str): The slug of the cafe.
        - item_slug (str): The slug of the menu item.

    Raises:
        - HTTPException: If the menu item is not found.

    Returns:
        - MenuItemOut: The detailed information about the menu item.
    """
    item = await CafeService.retrieve_menu_item(cafe_slug, item_slug)
    if not item:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Menu item not found."
        )
    return item


@cafe_router.post(
    "/cafes/{cafe_slug}/menu",
    response_model=MenuItemOut,
    summary="🔴 Create Menu Item",
    description="Create a new menu item for the specified café.",
)
async def create_menu_item(
    item: MenuItemCreate,
    cafe_slug: str = Path(..., description="The slug of the cafe"),
    current_user: User = Depends(get_current_user),
):
    """
    Create a new menu item for the specified café.

    Args:
        item (MenuItemCreate): The menu item to create.
        cafe_slug (str, optional): The slug of the cafe. Defaults to Path(..., description="The slug of the cafe").
        current_user (User, optional): The current user. Defaults to Depends(get_current_user).

    Raises:
        HTTPException: If the cafe is not found, access is forbidden, or a conflict occurs.

    Returns:
        MenuItemOut: The created menu item.
    """
    try:
        await CafeService.is_authorized_for_cafe_action_by_slug(
            cafe_slug, current_user, [Role.ADMIN]
        )
        return await CafeService.create_menu_item(cafe_slug, item)
    except ValueError as e:
        if str(e) == "Cafe not found":
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
        elif str(e) == "Access forbidden":
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=str(e))
        else:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=str(e))


@cafe_router.put(
    "/cafes/{cafe_slug}/menu/{item_slug}",
    response_model=MenuItemOut,
    summary="🟢 Update Menu Item",
    description="Update the details of an existing menu item.",
)
async def update_menu_item(
    item: MenuItemUpdate,
    cafe_slug: str = Path(..., description="The slug of the cafe"),
    item_slug: str = Path(..., description="The slug of the menu item"),
    current_user: User = Depends(get_current_user),
):
    """
    Update the details of an existing menu item.

    Args:
        item (MenuItemUpdate): The updated menu item.
        cafe_slug (str, optional): The slug of the cafe. Defaults to Path(..., description="The slug of the cafe").
        item_slug (str, optional): The slug of the menu item. Defaults to Path(..., description="The slug of the menu item").
        current_user (User, optional): The current user. Defaults to Depends(get_current_user).

    Raises:
        HTTPException: If the menu item or cafe is not found, access is forbidden, or a conflict occurs.

    Returns:
        MenuItemOut: The updated menu item.
    """
    try:
        # await CafeService.is_authorized_for_cafe_action_by_slug(
        #     cafe_slug, current_user, [Role.ADMIN, Role.VOLUNTEER]
        # )
        return await CafeService.update_menu_item(cafe_slug, item_slug, item)
    except ValueError as e:
        error_message = str(e)
        if error_message == "Menu item not found":
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail=error_message
            )
        elif error_message == "Cafe not found":
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail=error_message
            )
        elif error_message == "Access forbidden":
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN, detail=error_message
            )
        else:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT, detail=error_message
            )


@cafe_router.delete(
    "/cafes/{cafe_slug}/menu/{item_slug}",
    summary="🔴 Delete Menu Item",
    description="Delete a specific menu item from the café's menu.",
)
async def delete_menu_item(
    cafe_slug: str = Path(..., description="The slug of the cafe"),
    item_slug: str = Path(..., description="The slug of the menu item"),
    current_user: User = Depends(get_current_user),
):
    """
    Delete a specific menu item from the cafe's menu.

    Args:
        cafe_slug (str): The slug of the cafe (Path Parameter)
        item_slug (str): The slug of the menu item (Path Parameter)
        current_user (User): The current user (Dependency Injection)

    Raises:
        HTTPException: If the menu item is not found, the cafe is not found, or access is forbidden.

    Returns:
        dict: A dictionary containing a message indicating the success of the deletion.
    """
    try:
        await CafeService.is_authorized_for_cafe_action_by_slug(
            cafe_slug, current_user, [Role.ADMIN]
        )
        await CafeService.delete_menu_item(cafe_slug, item_slug)
        return {"message": f"Item {item_slug} has been successfully deleted."}
    except ValueError as e:
        error_message = str(e)
        if error_message == "Menu item not found":
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail=error_message
            )
        elif error_message == "Cafe not found":
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail=error_message
            )
        elif error_message == "Access forbidden":
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN, detail=error_message
            )


# --------------------------------------
#               Staff
# --------------------------------------


@cafe_router.get(
    "/cafes/{cafe_slug}/staff",
    response_model=List[StaffOut],
    summary="List Staff",
    description="Retrieve a list of all staff members for a specific cafe.",
)
async def list_staff(cafe_slug: str = Path(..., description="The slug of the cafe")):
    """
    Retrieves a list of all staff members for a specific cafe.

    Args:
        cafe_slug (str): The slug of the cafe.

    Returns:
        List[StaffOut]: A list of StaffOut objects representing the staff members of the cafe.
    """
    return await CafeService.list_staff_members(cafe_slug)


@cafe_router.post(
    "/cafes/{cafe_slug}/staff",
    response_model=StaffOut,
    summary="🔴 Create Staff Member",
    description="Add a new staff member to a specific cafe.",
)
async def create_staff_member(
    cafe_slug: str, staff: StaffCreate, current_user: User = Depends(get_current_user)
):
    """
    Add a new staff member to a specific cafe.

    Args:
        cafe_slug (str): The slug of the cafe.
        staff (StaffCreate): The details of the staff member to be added.
        current_user (User, optional): The current user making the request.
        
    Raises:
        HTTPException: If the staff member already exists, user is not found, cafe is not found, or access is forbidden.

    Returns:
        The newly created staff member.
    """
    user = await CafeService.retrieve_staff_member(cafe_slug, staff.username)
    if user:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT, detail="Staff member already exists"
        )

    user = await UserService.retrieve_user(staff.username)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="User not found"
        )

    try:
        await CafeService.is_authorized_for_cafe_action_by_slug(
            cafe_slug, current_user, [Role.ADMIN]
        )
    except ValueError as e:
        if str(e) == "Cafe not found":
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
        elif str(e) == "Access forbidden":
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=str(e))

    return await CafeService.create_staff_member(cafe_slug, staff)


@cafe_router.put(
    "/cafes/{cafe_slug}/staff/{username}",
    response_model=StaffOut,
    summary="🔴 Update Staff Member",
    description="Update details of an existing staff member.",
)
async def update_staff_member(
    cafe_slug: str,
    username: str,
    staff: StaffUpdate,
    current_user: User = Depends(get_current_user),
):
    """
    Update details of an existing staff member.

    Args:
        cafe_slug (str): The slug of the cafe.
        username (str): The username of the staff member to update.
        staff (StaffUpdate): The details to update for the staff member.
        current_user (User, optional): The current user making the request.

    Raises:
        HTTPException: If the cafe is not found, access is forbidden, or the staff member is not found.

    Returns:
        The updated staff member information.
    """
    try:
        await CafeService.is_authorized_for_cafe_action_by_slug(
            cafe_slug, current_user, [Role.ADMIN]
        )
        return await CafeService.update_staff_member(cafe_slug, username, staff)
    except ValueError as e:
        if str(e) == "Cafe not found":
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
        elif str(e) == "Access forbidden":
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=str(e))
        elif str(e) == "Staff member not found":
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))


@cafe_router.delete(
    "/cafes/{cafe_slug}/staff/{username}",
    summary="🔴 Delete Staff Member",
    description="Remove a staff member from a cafe.",
)
async def delete_staff_member(
    cafe_slug: str, username: str, current_user: User = Depends(get_current_user)
):
    """
    Remove a staff member from a cafe.

    Args:
        cafe_slug (str): The slug of the cafe.
        username (str): The username of the staff member to delete.
        current_user (User, optional): The current user making the request. Defaults to the user obtained from the dependency `get_current_user`.

    Raises:
        HTTPException: If the cafe is not found, access is forbidden, or the staff member is not found.

    Returns:
        dict: A dictionary containing a message indicating the success of the deletion.
    """
    try:
        await CafeService.is_authorized_for_cafe_action_by_slug(
            cafe_slug, current_user, [Role.ADMIN]
        )
        await CafeService.delete_staff_member(cafe_slug, username)
    except ValueError as e:
        if str(e) == "Cafe not found":
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
        elif str(e) == "Access forbidden":
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=str(e))
        elif str(e) == "Staff member not found":
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))

    return {"message": f"Staff member {username} has been successfully deleted."}


# --------------------------------------
#               Sales Report
# --------------------------------------


@cafe_router.get(
    "/cafes/{cafe_slug}/sales-report",
    summary="🔴 Get Sales Report",
    description="Retrieve a sales report for a specific cafe. If no date range is provided, the entire available data range is considered.",
)
async def get_sales_report(
    cafe_slug: str = Path(
        ..., description="The slug of the cafe for which to generate the report."
    ),
    start_date: Optional[str] = Query(
        None, description="The start date of the reporting period in YYYY-MM-DD format."
    ),
    end_date: Optional[str] = Query(
        None, description="The end date of the reporting period in YYYY-MM-DD format."
    ),
    report_type: str = Query(
        "daily",
        description="The type of report to generate. Can be 'daily', 'weekly', or 'monthly'.",
    ),
    current_user: User = Depends(get_current_user),
):
    """
    Retrieve a sales report for a specific cafe. If no date range is provided, the entire available data range is considered.
    
    Args:
        cafe_slug (str): The slug of the cafe for which to generate the report.
        start_date (Optional[str]): The start date of the reporting period in YYYY-MM-DD format. Defaults to None.
        end_date (Optional[str]): The end date of the reporting period in YYYY-MM-DD format. Defaults to None.
        report_type (str): The type of report to generate. Can be 'daily', 'weekly', or 'monthly'. Defaults to 'daily'.
        current_user (User): The current user. Defaults to the user obtained from the get_current_user dependency.
    
    Raises:
        HTTPException: If the cafe is not found or access is forbidden.
    
    Returns:
        The sales report data generated by OrderService.generate_sales_report_data.
    """
    try:
        await CafeService.is_authorized_for_cafe_action_by_slug(
            cafe_slug, current_user, [Role.ADMIN]
        )
    except ValueError as e:
        if str(e) == "Cafe not found":
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
        elif str(e) == "Access forbidden":
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=str(e))

    report_data = await OrderService.generate_sales_report_data(
        cafe_slug, start_date, end_date, report_type
    )

    return report_data


# --------------------------------------
#               Search
# --------------------------------------

# @cafe_router.get("/search", summary="Search for Cafes and Menu Items", description="Search across cafes and their menu items with a given query.")
# async def search(
#     request: Request,
#     query: str = Query(..., description="Search query for cafes or menu items"),
# ):
#     filters = dict(request.query_params)
#     filters.pop('query', None)
#     return await CafeService.search_cafes_and_items(query, **filters)
