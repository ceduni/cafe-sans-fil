from fastapi import APIRouter, HTTPException, Path, Query, status, Request, Depends
from app.models.cafe_model import Role
from app.schemas.cafe_schema import CafeOut, CafeCreate, CafeUpdate, MenuItemOut, MenuItemCreate, MenuItemUpdate, StaffCreate, StaffUpdate, StaffOut
from app.services.cafe_service import CafeService
from app.services.order_service import OrderService
from app.services.user_service import UserService
from typing import List, Optional
from app.models.user_model import User
from app.api.deps.user_deps import get_current_user

"""
This module defines the API routes related to cafes, their menus, and a unified search function for cafes and menu items.
"""

cafe_router = APIRouter()

# --------------------------------------
#               Cafe
# --------------------------------------

@cafe_router.get("/cafes", response_model=List[CafeOut], summary="List Cafes", description="Retrieve a list of all cafes.")
async def list_cafes(request: Request):
    query_params = dict(request.query_params)
    return await CafeService.list_cafes(**query_params)

@cafe_router.get("/cafes/{cafe_slug}", response_model=CafeOut, summary="Get Cafe", description="Retrieve detailed information about a specific cafe.")
async def get_cafe(cafe_slug: str = Path(..., description="The slug of the cafe")):
    cafe = await CafeService.retrieve_cafe(cafe_slug)
    if not cafe:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail="Café not found"
        )
    
    return cafe

@cafe_router.post("/cafes", response_model=CafeOut, summary="Create Cafe", description="Create a new cafe with the provided information.")
async def create_cafe(cafe: CafeCreate, current_user: User = Depends(get_current_user)):
    # Authorization check
    if "cafesansfil" != current_user.username:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Access forbidden"
        )
    return await CafeService.create_cafe(cafe)

@cafe_router.put("/cafes/{cafe_slug}", response_model=CafeOut, summary="Update Cafe", description="Update the details of an existing cafe.")
async def update_cafe(cafe: CafeUpdate, cafe_slug: str = Path(..., description="The slug of the cafe to update"),  current_user: User = Depends(get_current_user)):
    cafe_exists = await CafeService.retrieve_cafe(cafe_slug)
    if not cafe_exists:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Café not found"
        )

    try:
        await CafeService.is_authorized_for_cafe_action_by_slug(cafe_slug, current_user, [Role.ADMIN])
    except ValueError as e:
        if str(e) == "Cafe not found":
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=str(e)
            )
        elif str(e) == "Access forbidden":
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=str(e)
            )

    return await CafeService.update_cafe(cafe_slug, cafe)

# --------------------------------------
#               Menu
# --------------------------------------

@cafe_router.get("/cafes/{cafe_slug}/menu", response_model=List[MenuItemOut], summary="List Menu Items", description="Retrieve the menu items of a specific café.")
async def list_menu_items(request: Request, cafe_slug: str = Path(..., description="The slug of the cafe")):
    query_params = dict(request.query_params)
    query_params['slug'] = cafe_slug
    menu = await CafeService.list_menu_items(**query_params)
    if not menu:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Menu not found for the given café."
        )
    return menu

@cafe_router.get("/cafes/{cafe_slug}/menu/{item_slug}", response_model=MenuItemOut, summary="Get Menu Item", description="Retrieve detailed information about a specific menu item.")
async def get_menu_item(cafe_slug: str = Path(..., description="The slug of the cafe"), item_slug: str = Path(..., description="The slug of the menu item")):
    item = await CafeService.retrieve_menu_item(cafe_slug, item_slug)
    if not item:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Menu item not found."
        )
    return item

@cafe_router.post("/cafes/{cafe_slug}/menu", response_model=MenuItemOut, summary="Create Menu Item", description="Create a new menu item for the specified café.")
async def create_menu_item(item: MenuItemCreate, cafe_slug: str = Path(..., description="The slug of the cafe"), current_user: User = Depends(get_current_user)):
    try:
        await CafeService.is_authorized_for_cafe_action_by_slug(cafe_slug, current_user, [Role.ADMIN])
    except ValueError as e:
        if str(e) == "Cafe not found":
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=str(e)
            )
        elif str(e) == "Access forbidden":
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=str(e)
            )

    return await CafeService.create_menu_item(cafe_slug, item)

@cafe_router.put("/cafes/{cafe_slug}/menu/{item_slug}", response_model=MenuItemOut, summary="Update Menu Item", description="Update the details of an existing menu item.")
async def update_menu_item(item: MenuItemUpdate, cafe_slug: str = Path(..., description="The slug of the cafe"), item_slug: str = Path(..., description="The slug of the menu item"), current_user: User = Depends(get_current_user)):
    try:
        await CafeService.is_authorized_for_cafe_action_by_slug(cafe_slug, current_user, [Role.ADMIN, Role.VOLUNTEER])
        return await CafeService.update_menu_item(cafe_slug, item_slug, item)
    except ValueError as e:
        error_message = str(e)
        if error_message == "Menu item not found":
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=error_message
            )
        elif error_message == "Cafe not found":
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=error_message
            )
        elif error_message == "Access forbidden":
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=error_message
            )

@cafe_router.delete("/cafes/{cafe_slug}/menu/{item_slug}", summary="Delete Menu Item", description="Delete a specific menu item from the café's menu.")
async def delete_menu_item(cafe_slug: str = Path(..., description="The slug of the cafe"), item_slug: str = Path(..., description="The slug of the menu item"), current_user: User = Depends(get_current_user)):
    try:
        await CafeService.is_authorized_for_cafe_action_by_slug(cafe_slug, current_user, [Role.ADMIN])
        await CafeService.delete_menu_item(cafe_slug, item_slug)
        return {"message": f"Item {item_slug} has been successfully deleted."}
    except ValueError as e:
        error_message = str(e)
        if error_message == "Menu item not found":
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=error_message
            )
        elif error_message == "Cafe not found":
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=error_message
            )
        elif error_message == "Access forbidden":
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=error_message
            )
        
# --------------------------------------
#               Staff
# --------------------------------------

@cafe_router.get("/cafes/{cafe_slug}/staff", response_model=List[StaffOut], summary="List Staff", description="Retrieve a list of all staff members for a specific cafe.")
async def list_staff(cafe_slug: str = Path(..., description="The slug of the cafe")):
    return await CafeService.list_staff_members(cafe_slug)

@cafe_router.post("/cafes/{cafe_slug}/staff", response_model=StaffOut, summary="Create Staff Member", description="Add a new staff member to a specific cafe.")
async def create_staff_member(cafe_slug: str, staff: StaffCreate, current_user: User = Depends(get_current_user)):
    user = await CafeService.retrieve_staff_member(cafe_slug, staff.username)
    if user:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Staff member already exists"
        )
    
    user = await UserService.retrieve_user(staff.username)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )

    try:
        await CafeService.is_authorized_for_cafe_action_by_slug(cafe_slug, current_user, [Role.ADMIN])
    except ValueError as e:
        if str(e) == "Cafe not found":
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=str(e)
            )
        elif str(e) == "Access forbidden":
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=str(e)
            )
        
    return await CafeService.create_staff_member(cafe_slug, staff)

@cafe_router.put("/cafes/{cafe_slug}/staff/{username}", response_model=StaffOut, summary="Update Staff Member", description="Update details of an existing staff member.")
async def update_staff_member(cafe_slug: str, username: str, staff: StaffUpdate, current_user: User = Depends(get_current_user)):
    try:
        await CafeService.is_authorized_for_cafe_action_by_slug(cafe_slug, current_user, [Role.ADMIN])
        return await CafeService.update_staff_member(cafe_slug, username, staff)
    except ValueError as e:
        if str(e) == "Cafe not found":
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=str(e)
            )
        elif str(e) == "Access forbidden":
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=str(e)
            )
        elif str(e) == "Staff member not found":
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=str(e)
            )
    

@cafe_router.delete("/cafes/{cafe_slug}/staff/{username}", summary="Delete Staff Member", description="Remove a staff member from a cafe.")
async def delete_staff_member(cafe_slug: str, username: str, current_user: User = Depends(get_current_user)):    
    try:
        await CafeService.is_authorized_for_cafe_action_by_slug(cafe_slug, current_user, [Role.ADMIN])
        await CafeService.delete_staff_member(cafe_slug, username)
    except ValueError as e:
        if str(e) == "Cafe not found":
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=str(e)
            )
        elif str(e) == "Access forbidden":
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=str(e)
            )
        elif str(e) == "Staff member not found":
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=str(e)
            )
    
    return {"message": f"Staff member {username} has been successfully deleted."}

# --------------------------------------
#               Sales Report
# --------------------------------------

@cafe_router.get("/cafes/{cafe_slug}/sales-report", summary="Get Sales Report", description="Retrieve a sales report for a specific cafe. If no date range is provided, the entire available data range is considered.")
async def get_sales_report(
    cafe_slug: str = Path(..., description="The slug of the cafe for which to generate the report."),
    start_date: Optional[str] = Query(None, description="The start date of the reporting period in YYYY-MM-DD format."),
    end_date: Optional[str] = Query(None, description="The end date of the reporting period in YYYY-MM-DD format."),
    report_type: str = Query("daily", description="The type of report to generate. Can be 'daily', 'weekly', or 'monthly'."),
    current_user: User = Depends(get_current_user)
):
    try:
        await CafeService.is_authorized_for_cafe_action_by_slug(cafe_slug, current_user, [Role.ADMIN])
    except ValueError as e:
        if str(e) == "Cafe not found":
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=str(e)
            )
        elif str(e) == "Access forbidden":
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=str(e)
            )
        
    report_data = await OrderService.generate_sales_report_data(cafe_slug, start_date, end_date, report_type)
    
    return report_data

# --------------------------------------
#               Search
# --------------------------------------

@cafe_router.get("/search", summary="Search for Cafes and Menu Items", description="Search across cafes and their menu items with a given query.")
async def search(request: Request, query: str = Query(..., description="Search query for cafes or menu items")):
    filters = dict(request.query_params)
    filters.pop('query', None)
    return await CafeService.search_cafes_and_items(query, **filters)
