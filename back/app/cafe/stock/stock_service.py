from typing import List, Union

from beanie import PydanticObjectId
from beanie.odm.queries.find import FindMany

from app.cafe.stock.stock_model import Stock, StockCreate, StockUpdate
from app.cafe.models import Cafe
from app.service import set_attributes

class StockService:
    """Service class for CRUD and search operations on Menu."""

    @staticmethod
    async def get_all(
        to_list: bool = True,
        **filters: dict,
    ) -> Union[FindMany[Stock], List[Stock]]:
        """Get stocks."""
        sort_by = filters.pop("sort_by", "name")
        query = Stock.find(filters).sort(sort_by)
        return await query.to_list() if to_list else query

    @staticmethod
    async def get_by_ids_and_cafe_id(
        ids: List[PydanticObjectId], cafe_id: PydanticObjectId
    ) -> list[Stock]:
        return await Stock.find({"cafe_id": cafe_id, "_id": {"$in": ids}}).to_list()

    @staticmethod
    async def get_by_id_and_cafe_id(id: PydanticObjectId, cafe_id: PydanticObjectId):
        """Get a stock item by ID and cafe ID."""
        return await Stock.find_one({"_id": id, "cafe_id": cafe_id})

    @staticmethod
    async def get(id: PydanticObjectId) -> Stock:
        """Get a stock item by ID."""
        return await Stock.get(id)

    @staticmethod
    async def create(cafe: Cafe, data: StockCreate) -> Stock:
        """Create a new stock item."""
        item = Stock(**data.model_dump(), cafe_id=cafe.id)
        await item.insert()
        return item

    @staticmethod
    async def update(item: Stock, data: StockUpdate) -> Stock:
        """Update a stock item."""
        set_attributes(item, data)
        await item.save()
        return item

    @staticmethod
    async def delete(item: Stock) -> None:
        """Delete a stock item."""
        await item.delete()

    @staticmethod
    async def create_many(cafe: Cafe, data: List[StockCreate]) -> List[Stock]:
        """Create multiple stock items."""
        items = [
            Stock(**item_data.model_dump(), cafe_id=cafe.id) for item_data in data
        ]
        await Stock.insert_many(items)
        return items

    @staticmethod
    async def update_many(
        ids: List[PydanticObjectId], data: StockUpdate
    ) -> List[Stock]:
        """Update multiple stock items."""
        result = await Stock.find_many({"_id": {"$in": ids}}).update_many(
            {"$set": data.model_dump(exclude_unset=True)}
        )
        if result.matched_count == 0:
            return None

        return await Stock.find_many({"_id": {"$in": ids}}).to_list()

    @staticmethod
    async def delete_many(ids: List[PydanticObjectId]) -> None:
        """Delete multiple stock items."""
        await Stock.find_many({"_id": {"$in": ids}}).delete_many()
