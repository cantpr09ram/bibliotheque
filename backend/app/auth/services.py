from fastapi import HTTPException, Depends
from fastapi.security import OAuth2PasswordBearer
from app.database import get_users_collection
import os

from .utils import pwd_context

def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)


def authenticate_user(username: str, password: str):
    users_collection = get_users_collection()
    user = users_collection.find_one({"username": username})
    if not user or not verify_password(password, user["password"]):
        return False
    return user