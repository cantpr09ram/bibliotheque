from fastapi import APIRouter

from app.services.api import category
from app.services.api import book
api_router = APIRouter()
api_router.include_router(category.router, tags=["categories"])
api_router.include_router(book.router, tags=["books"])