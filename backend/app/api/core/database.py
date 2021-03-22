""" MongoDB singleton with utilities"""

from typing import Optional

from pymongo import MongoClient

from api.core.config import settings
from api.auth.deps import get_password_hash
from api.schemas.user import UserInDB

db = MongoClient(
    f"mongodb://{settings.MONGO_USERNAME}:{settings.MONGO_PASSWORD}@{settings.MONGO_BASE_HOST_PORT}/api_demo")


def get_user(username) -> Optional[UserInDB, None]:
    user = db.users.find_one({"username": {"$eq": username}})

    if user:
        return UserInDB(**user)
    return None