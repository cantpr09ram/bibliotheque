<<<<<<< Updated upstream
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
=======
import pydantic
from typing import List

class subCategoryBase(pydantic.BaseModel):
    name: str
    id: int
    description: str = ""

class CategoryBase(pydantic.BaseModel):
    name: str
    id: int
    description: str = ""
    subCategory: List[subCategoryBase] = []

    def add_subcategory(self, subcategory: subCategoryBase):
        self.subCategory.append(subcategory)

    def get_subcategories(self) -> List[subCategoryBase]:
        return self.subCategory
>>>>>>> Stashed changes
