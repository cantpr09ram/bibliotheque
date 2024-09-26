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
