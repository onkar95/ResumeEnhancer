from datetime import datetime
from uuid import uuid4

from app.core.DB import get_db


def get_users_collection():
    return get_db()["users"]


def ensure_user_indexes() -> None:
    get_users_collection().create_index("google_id", unique=True)
    get_users_collection().create_index("user_id", unique=True)


def upsert_google_user(google_id: str, email: str, name: str | None, picture: str | None) -> dict:
    users = get_users_collection()

    existing = users.find_one({"google_id": google_id})

    if existing:
        users.update_one(
            {"google_id": google_id},
            {"$set": {"last_login": datetime.utcnow().isoformat(), "name": name, "picture": picture}},
        )
        existing.pop("_id", None)
        existing["last_login"] = datetime.utcnow().isoformat()
        return existing

    doc = {
        "user_id": str(uuid4()),
        "google_id": google_id,
        "email": email,
        "name": name,
        "picture": picture,
        "created_at": datetime.utcnow().isoformat(),
        "last_login": datetime.utcnow().isoformat(),
    }

    users.insert_one(doc)
    doc.pop("_id", None)
    return doc


def get_user_by_id(user_id: str) -> dict | None:
    doc = get_users_collection().find_one({"user_id": user_id})
    if doc:
        doc.pop("_id", None)
    return doc