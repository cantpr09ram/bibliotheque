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

def get_categories_collection():
    return db.categories

def get_books_collection():
    return db.books

def get_events_collection():
    return db.events