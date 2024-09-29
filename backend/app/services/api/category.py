from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel
from typing import List, Optional

from app.services.schemas.category import Category, SubCategory
from app.auth.dependencies import get_current_user
from app.database import get_categories_collection

router = APIRouter()

class CategorySummary(BaseModel):
    id: str
    name: str

@router.get("/categories", response_model=List[CategorySummary])
async def get_categories():
    categories = get_categories_collection().find({}, {"_id": 1, "name": 1})
    if categories is None:
        categories = []
    return [{"id": str(category["_id"]), "name": category["name"]} for category in categories]

@router.get("/categories/{category_id}", response_model=Category)
async def get_category(category_id: str):
    category = get_categories_collection().find_one({"_id": category_id})
    if category is None:
        raise HTTPException(status_code=404, detail="Category not found")
    return category

@router.post("/categories", response_model=Category,)
async def create_category(category: Category, current_user: dict = Depends(get_current_user)):
    category_dict = category.dict()
    category_dict["owner"] = current_user["username"]
    result = get_categories_collection().insert_one(category_dict)
    category_dict["_id"] = str(result.inserted_id)
    return category_dict

@router.put("/categories/{category_id}", response_model=Category)
async def update_category(category_id: str, category: Category, current_user: dict = Depends(get_current_user)):
    category_dict = category.dict()
    category_dict["owner"] = current_user["username"]
    result = get_categories_collection().replace_one({"_id": category_id}, category)