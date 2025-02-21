"""
Module for handling search-related models.
"""

from typing import List, Optional

from pydantic import BaseModel

from app.cafe.models import CafeViewOut


class SearchCreate(BaseModel):
    """Model for creating search queries."""

    query: str


class SearchOut(BaseModel):
    """Model for search output."""

    cafes: Optional[List[CafeViewOut]] = None
