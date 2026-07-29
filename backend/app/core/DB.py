"""
MongoDB connection.

Single shared client for the app's lifetime. pymongo's client is
thread-safe and pools connections internally, so this is safe to reuse
across FastAPI's threadpool-executed sync route handlers.
"""

from pymongo import MongoClient
from pymongo.collection import Collection

from app.core.config import settings

_client = MongoClient(settings.MONGO_URI)
_db = _client[settings.MONGO_DB_NAME]


def get_db():
    return _db


def get_runs_collection() -> Collection:
    return _db["runs"]


def ensure_indexes() -> None:
    runs = get_runs_collection()
    runs.create_index("run_id", unique=True)
    runs.create_index("created_at")