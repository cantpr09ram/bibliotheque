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
    """
    Retrieve all categories with basic information (ID and name).

    - **Returns**: 
        - A list of categories where each category includes:
            - `id`: The unique identifier of the category.
            - `name`: The name of the category.
    - **Return Type**: `List[CategorySummary]` (List of category summaries)
    """
    categories = get_categories_collection().find({}, {"_id": 1, "name": 1})
    if categories is None:
        categories = []
    return [{"id": str(category["_id"]), "name": category["name"]} for category in categories]

@router.post("/categories/{category_id}/subcategories", response_model=Category)
async def add_subcategory_to_category(category_id: str, subcategory: SubCategory, current_user: dict = Depends(get_current_user)):
    """
    Add a new subcategory to an existing category.

    - **Parameters**:
        - `category_id` (str): The unique identifier of the category to which the subcategory will be added.
        - `subcategory` (SubCategoryCreate): The subcategory information to add (validated via `SubCategoryCreate` schema).
        - `current_user` (dict): The current authenticated user information (injected dependency).

    - **Process**:
        - Fetch the category by its ID from the database.
        - Check if the category exists; if not, raise a 404 error.
        - Convert the subcategory data to a dictionary and add it to the category's `subcategories` list.
        - Update the category in the database with the new subcategory.
        - Return the updated category.

    - **Returns**:
        - The updated category, including the newly added subcategory.
    - **Raises**:
        - `404`: If the category with the specified ID is not found.
    """
    # Find the category by its ID in the database
    category = get_categories_collection().find_one({"_id": category_id})
    
    # If the category doesn't exist, raise a 404 error
    if category is None:
        raise HTTPException(status_code=404, detail="Category not found")

    # Convert the subcategory data into a dictionary
    subcategory_data = subcategory.dict()

    # Check if the category already has a 'subcategories' field; if not, create an empty list
    if "subcategories" not in category:
        category["subcategories"] = []

    # Append the new subcategory to the category's subcategories list
    category["subcategories"].append(subcategory_data)

    # Update the category in the database, setting the new subcategories list
    get_categories_collection().update_one({"_id": category_id}, {"$set": {"subcategories": category["subcategories"]}})

    # Retrieve the updated category from the database
    updated_category = get_categories_collection().find_one({"_id": category_id})

    # Return the updated category, including the new subcategory
    return updated_category


@router.get("/categories/{category_id}", response_model=Category)
async def get_category(category_id: str):
    """
    Retrieve detailed information of a single category by its ID.

    - **Parameters**:
        - `category_id` (str): The unique identifier of the category to retrieve.
    - **Returns**: 
        - The full category information, including fields like name, description, owner, etc.
    - **Raises**:
        - `404`: If the category with the specified ID is not found.
    """
    category = get_categories_collection().find_one({"_id": category_id})
    if category is None:
        raise HTTPException(status_code=404, detail="Category not found")
    return category

@router.post("/categories", response_model=Category,)
async def create_category(category: Category, current_user: dict = Depends(get_current_user)):
    """
    Create a new category and store it in the database.

    - **Parameters**:
        - `category` (Category): The category information to be created.
        - `current_user` (dict): The current authenticated user information (injected dependency).
    - **Process**:
        - Associate the new category with the current user as the owner.
        - Insert the category into the database.
    - **Returns**:
        - The newly created category, including its ID.
    """
    category_dict = category.dict()
    category_dict["owner"] = current_user["username"]
    result = get_categories_collection().insert_one(category_dict)
    category_dict["_id"] = str(result.inserted_id)
    return category_dict

@router.put("/categories/{category_id}", response_model=Category)
async def update_category(category_id: str, category: Category, current_user: dict = Depends(get_current_user)):
    """
    Update an existing category by its ID.

    - **Parameters**:
        - `category_id` (str): The unique identifier of the category to update.
        - `category` (Category): The updated category information.
        - `current_user` (dict): The current authenticated user information (injected dependency).
    - **Process**:
        - Update the category in the database.
        - The updated category will be associated with the current user as the owner.
    - **Returns**:
        - The updated category information.
    """
    category_dict = category.dict()
    category_dict["owner"] = current_user["username"]
    result = get_categories_collection().replace_one({"_id": category_id}, category)