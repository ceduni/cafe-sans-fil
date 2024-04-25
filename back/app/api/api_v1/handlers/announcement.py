from fastapi import APIRouter, HTTPException, Depends, Path, Request, Query
from typing import List, Optional, Dict
from uuid import UUID

from app.schemas.announcement_schema import AnnouncementCreate, AnnouncementOut
from app.services.announcement_service import AnnouncementService
from app.models.user_model import User
from app.api.deps.user_deps import get_current_user

announcement_router = APIRouter()

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
        elif key.endswith("_id"):
            value = UUID(value)

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

@announcement_router.get("/announcements/", response_model=List[AnnouncementOut])
async def list_announcements(
    request: Request,
    cafe_id: Optional[UUID] = Query(None, description="Filter announcements by cafe ID."),
    sort_by: Optional[str] = Query("-created_at", description="Sort announcements by a specific field. Prefix with '-' for descending order (e.g., '-created_at')."),
    page: Optional[int] = Query(1, description="Specify the page number for pagination."),
    limit: Optional[int] = Query(9, description="Set the number of cafes to return per page.")
):
    query_params = dict(request.query_params)
    parsed_params = parse_query_params(query_params)
    return await AnnouncementService.get_announcements(**parsed_params)

@announcement_router.post("/announcements/", response_model=AnnouncementOut)
async def create_announcement(announcement: AnnouncementCreate):
    return await AnnouncementService.create_announcement(announcement)

@announcement_router.delete("/announcements/{announcement_id}")
async def delete_announcement(announcement_id: UUID):
    return await AnnouncementService.remove_announcement(announcement_id)

@announcement_router.post("/announcements/{announcement_id}/like", response_model=AnnouncementOut)
async def toggle_like(
    announcement_id: UUID = Path(..., description="The ID of the announcement"),
    current_user: User = Depends(get_current_user),
    unlike: bool = False
):
    if not unlike:
        return await AnnouncementService.add_like_to_announcement(announcement_id, current_user.user_id)
    else:
        return await AnnouncementService.remove_like_from_announcement(announcement_id, current_user.user_id)
