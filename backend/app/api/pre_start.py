""" This script populates the db previous to the FastAPI start """
from pymongo import MongoClient

from api.core.config import settings
from api.auth.deps import get_password_hash


def main() -> None:
    # Get a connection to the database
    client = MongoClient(
        f"mongodb://{settings.MONGO_USERNAME}:{settings.MONGO_PASSWORD}@{settings.MONGO_BASE_HOST_PORT}/")
    db = client["api_demo_v2"]
    users = db["users"]

    # Set up the demo user. As we have a mongo volume, we do a replace instead
    # of creating the user in case that this isn't the first startup
    users.replace_one(
        {"username": {"$eq": settings.DEMO_USERNAME}},
        {"username": settings.DEMO_USERNAME,
            "hashed_password": get_password_hash(settings.DEMO_USER_PASSWORD)},
        upsert=True)


if __name__ == "__main__":
    main()
