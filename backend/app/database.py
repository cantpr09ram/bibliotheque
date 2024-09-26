import os
from pymongo import MongoClient

client = None
db = None

def init_db():
    global client, db
    client = MongoClient(os.getenv("MONGODB_URI"))
    db = client.db

def get_users_collection():
    return db.users

def get_library_collection():
    return db.library