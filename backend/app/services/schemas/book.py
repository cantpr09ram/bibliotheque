<<<<<<< Updated upstream
import pydantic
import datetime
from category import Category, subCategory

class BookBase(pydantic.BaseModel):
    title: str
    publication_date: datetime.date
    description: Optional[str] = None
    id: str
    isbn: str
    author: str
    category: category.Category.name
    subcategory: category.subCategory.name
    img: str
=======
from pydantic import BaseModel
from typing import Optional

class Book(BaseModel):
    title: str
    author: str
    published_year: int
    isbn: str
    cover: Optional[str] = None
    language: str
    publisher: str
    description: str
    Category: str
    subCategory: str
>>>>>>> Stashed changes
