""" MongoDB singleton with utilities"""

from typing import Optional

from pymongo import MongoClient

from api.core.config import settings
from api.schemas.user import UserInDB

client = MongoClient(
    f"mongodb://{settings.MONGO_USERNAME}:{settings.MONGO_PASSWORD}@{settings.MONGO_BASE_HOST_PORT}/")
db = client["api_demo_v2"]

def get_user(username) -> Optional[UserInDB]:
    user = db.users.find_one({"username": {"$eq": username}})

    if user:
        return UserInDB(**user)
    return None