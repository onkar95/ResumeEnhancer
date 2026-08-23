"""
Tracks resume generations per user to enforce a rolling 24h quota.
Any generation counts, regardless of JD content, per the product decision
to keep this simple and protect LLM token spend.
"""

from datetime import datetime, timedelta

from app.core.DB import get_db

FREE_LIMIT = 2
WINDOW_HOURS = 24


def get_usage_collection():
    return get_db()["generation_events"]


def ensure_usage_indexes() -> None:
    get_usage_collection().create_index("user_id")
    get_usage_collection().create_index("created_at")


def _window_start() -> str:
    return (datetime.utcnow() - timedelta(hours=WINDOW_HOURS)).isoformat()


def count_recent_generations(user_id: str) -> int:
    return get_usage_collection().count_documents(
        {"user_id": user_id, "created_at": {"$gte": _window_start()}}
    )


def remaining_quota(user_id: str) -> int:
    return max(0, FREE_LIMIT - count_recent_generations(user_id))


def has_quota(user_id: str) -> bool:
    return count_recent_generations(user_id) < FREE_LIMIT


def record_generation(user_id: str, run_id: str) -> None:
    get_usage_collection().insert_one(
        {
            "user_id": user_id,
            "run_id": run_id,
            "created_at": datetime.utcnow().isoformat(),
        }
    )