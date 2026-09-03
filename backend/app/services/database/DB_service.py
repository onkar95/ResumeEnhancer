"""
Run Store (MongoDB-backed)

Same public API as the old JSON-file version, so review.py, approval.py,
and resume_workflow.py need zero changes:

    save_run(run_id, data)
    load_run(run_id) -> dict | None
    list_runs() -> list[dict]
    update_run(run_id, patch) -> dict
    delete_run(run_id) -> bool
    clear_all_runs() -> int
    apply_dot_path(data, path, value) -> dict
"""

from datetime import datetime
from typing import Any, Optional

from app.core.DB import get_runs_collection


def save_run(run_id: str, data: dict[str, Any]) -> None:
    """
    Overwrites (upserts) the full run record.
    """

    doc = dict(data)
    doc["run_id"] = run_id
    doc["saved_at"] = datetime.utcnow().isoformat()
    doc.setdefault("created_at", doc["saved_at"])

    get_runs_collection().update_one(
        {"run_id": run_id},
        {"$set": doc},
        upsert=True,
    )


def load_run(run_id: str) -> Optional[dict[str, Any]]:

    doc = get_runs_collection().find_one({"run_id": run_id})

    if doc is None:
        return None

    doc.pop("_id", None)
    return doc


def list_runs(user_id=None, limit=20, offset=0) -> list[dict]:
    query = {"user_id": user_id} if user_id else {}

    cursor = (
        get_runs_collection()
        .find(
            query,
            {
                "run_id": 1,
                "created_at": 1,
                "user_id": 1,
                "finalized": 1,
                "resume_name": 1,
                "parsed_jd.job_details.title": 1,
                "parsed_jd.job_details.company": 1,
                "comparison_data.ats_before": 1, 
                "comparison_data.ats_after": 1,
                "_id": 0
            },
        )
        .sort("created_at", -1)
        .skip(offset)
        .limit(limit)
    )

    runs = []

    for doc in cursor:

        jd_details = (doc.get("parsed_jd") or {}).get("job_details") or {}
        comparison = doc.get("comparison_data") or {}

        runs.append(
            {
                "run_id": doc.get("run_id"),
                "user_id": doc.get("user_id"),
                "created_at": doc.get("created_at"),
                "finalized": doc.get("finalized", False),
                "resume_name": doc.get("resume_name"),
                "job_title": jd_details.get("title"),
                "company": jd_details.get("company"),
                "ats_before": comparison.get("ats_before"),
                "ats_after": comparison.get("ats_after"),
            }
        )

    return runs

def update_run(run_id: str, patch: dict[str, Any]) -> dict[str, Any]:

    existing = load_run(run_id)

    if existing is None:
        raise ValueError(f"No stored run found for run_id={run_id}")

    existing.update(patch)

    save_run(run_id, existing)

    return existing


def delete_run(run_id: str) -> bool:

    result = get_runs_collection().delete_one({"run_id": run_id})

    return result.deleted_count > 0


def clear_all_runs() -> int:

    result = get_runs_collection().delete_many({})

    return result.deleted_count


def apply_dot_path(data: dict[str, Any], path: str, value: Any) -> dict[str, Any]:
    """
    Unchanged from the file-store version -- pure in-memory dict mutation.
    """

    segments = path.split(".")
    node = data

    for seg in segments[:-1]:
        key: Any = int(seg) if seg.isdigit() else seg
        node = node[key]

    last = segments[-1]
    last_key: Any = int(last) if last.isdigit() else last
    node[last_key] = value

    return data