from fastapi import APIRouter, HTTPException, Depends, Path, Request, Query
from typing import List, Optional, Dict
from beanie import PydanticObjectId

from app.schemas.event_schema import EventCreate, EventUpdate, EventOut
from app.services.event_service import EventService
from app.models.user_model import User
from app.api.deps.user_deps import get_current_user

event_router = APIRouter()

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
            value = PydanticObjectId(value)

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

@event_router.get("/events/", response_model=List[EventOut])
async def list_events(
    request: Request,
    cafe_id: Optional[PydanticObjectId] = Query(None, description="Filter events by cafe ID."),
    sort_by: Optional[str] = Query("-start_date", description="Sort events by a specific field. Prefix with '-' for descending order (e.g., '-start_date')."),
    page: Optional[int] = Query(1, description="Specify the page number for pagination."),
    limit: Optional[int] = Query(9, description="Set the number of cafes to return per page.")
):
    query_params = dict(request.query_params)
    parsed_params = parse_query_params(query_params)
    return await EventService.get_events(**parsed_params)

@event_router.post("/events/", response_model=EventOut)
async def create_event(event: EventCreate):
    return await EventService.create_event(event)

@event_router.put("/events/{event_id}", response_model=EventOut)
async def update_event(event_id: PydanticObjectId, event: EventUpdate):
    return await EventService.update_event(event_id, event)

@event_router.delete("/events/{event_id}")
async def delete_event(event_id: PydanticObjectId):
    return await EventService.remove_event(event_id)

@event_router.post("/events/{event_id}/attend", response_model=EventOut)
async def toggle_attendance(
    event_id: PydanticObjectId = Path(..., description="The ID of the event"),
    current_user: User = Depends(get_current_user),
    remove: bool = False
):
    if not remove:
        return await EventService.add_attendee_to_event(event_id, current_user.id)
    else:
        return await EventService.remove_attendee_from_event(event_id, current_user.id)

@event_router.post("/events/{event_id}/support", response_model=EventOut)
async def toggle_support(
    event_id: PydanticObjectId = Path(..., description="The ID of the event"),
    current_user: User = Depends(get_current_user),
    remove: bool = False
):
    if not remove:
        return await EventService.add_supporter_to_event(event_id, current_user.id)
    else:
        return await EventService.remove_supporter_from_event(event_id, current_user.id)