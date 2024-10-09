from __future__ import annotations  # Enables forward references
from pydantic import BaseModel, Field
from typing import List, Optional

class SubCategory(BaseModel):
    name: str
    id: str
    description: Optional[str] = None

class Category(BaseModel):
    name: str
    id: str
    description: Optional[str] = None
    subcategories: List[SubCategory] = Field(default_factory=list)
