import pydantic
from typing import List, Optional

class CategoryBase(pydantic.BaseModel):
    name: str
    id: str
    description: Optional[str] = None
    subcategories: Optional[List[subcategories]] = []

class subCategoryBase(pydantic.BaseModel):
    name: str
    id: str
    description: Optional[str] = None