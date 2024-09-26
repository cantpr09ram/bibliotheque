import pydantic
from category import Category

class EventBase(pydantic.BaseModel):
    title: str
    date: str
    description: str
    id: str
    img: str
    category: category.Category.name