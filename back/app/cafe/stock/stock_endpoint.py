from typing import Optional, TypeVar

from beanie import PydanticObjectId
from fastapi import APIRouter, Depends, HTTPException, Path, Query, Request, status
from app.cafe.service import CafeService
from app.cafe.stock.stock_model import Stock
from app.cafe.stock.stock_service import StockService
from app.models import ErrorResponse
from app.service import parse_query_params

stock_router = APIRouter()

@stock_router.get(
    "/cafes/{slug}/stock",
    response_model=Stock,
    responses={
        404: {"model": ErrorResponse},
    },
)
async def list_stock_items(
    request: Request,
    slug: str = Path(..., description="Slug of the cafe"),
):
    """Get a list of stock items for a cafe."""
    cafe = await CafeService.get(slug)
    if not cafe:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=[{"msg": "A cafe with this slug does not exist."}],
        )

    filters = parse_query_params(dict(request.query_params))
    filters["cafe_id"] = cafe.id

    items = await StockService.get_all(to_list=True, **filters)
    return items



@stock_router.get(
    "/cafes/{slug}/stock/{id}",
    response_model=Stock,
    responses={
        404: {"model": ErrorResponse},
    },
)
async def get_item(
    slug: str = Path(..., description="Slug of the cafe"),
    id: PydanticObjectId = Path(..., description="ID of the stock item"),
):
    """Get a stock item."""
    cafe = await CafeService.get(slug)
    if not cafe:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=[{"msg": "A cafe with this slug does not exist."}],
        )

    item = await StockService.get_by_id_and_cafe_id(id, cafe.id)
    if not item:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=[{"msg": "An item with this ID does not exist."}],
        )
        
    return item
