# """
# Run Store

# Persists a snapshot of each workflow run so the human-review flow can:

# - fetch the current draft + suggestions for a run
# - apply direct section edits
# - apply approved suggestions and re-tailor
# - keep a version history of tailored resumes for that run

# This is intentionally a simple JSON-file store (one file per run_id) rather
# than a database, matching the rest of this project's persistence style
# (see InventoryStorageService). It's swappable for a real DB or LangGraph
# checkpointer later without changing the API surface much.
# """

# import json
# from datetime import datetime
# from pathlib import Path
# from typing import Any, Optional

# RUN_STORE_DIR = Path("app/data/runs")


# def _run_path(run_id: str) -> Path:
#     RUN_STORE_DIR.mkdir(parents=True, exist_ok=True)
#     return RUN_STORE_DIR / f"{run_id}.json"


# def save_run(run_id: str, data: dict[str, Any]) -> None:
#     """
#     Overwrites the full run record. `data` should already be
#     JSON-serializable (e.g. via pydantic .model_dump(mode="json")).
#     """

#     path = _run_path(run_id)

#     data = dict(data)
#     data["run_id"] = run_id
#     data["saved_at"] = datetime.utcnow().isoformat()

#     with open(path, "w", encoding="utf-8") as f:
#         json.dump(data, f, indent=2, ensure_ascii=False, default=str)


# def load_run(run_id: str) -> Optional[dict[str, Any]]:

#     path = _run_path(run_id)

#     if not path.exists():
#         return None

#     with open(path, "r", encoding="utf-8") as f:
#         return json.load(f)

# def list_runs() -> list[dict]:
#     runs = []

#     for file in RUN_STORE_DIR.glob("*.json"):
#         with open(file, "r", encoding="utf-8") as f:
#             data = json.load(f)

#         comparison = data.get("comparison_data") or {}
#         jd = data.get("parsed_jd") or {}
#         details = jd.get("job_details") or {}

#         runs.append(
#             {
#                 "run_id": file.stem,
#                 "created_at": data.get("created_at"),
#                 "finalized": data.get("finalized", False),
#                 "job_title": details.get("title"),
#                 "company": details.get("company"),
#                 "ats_before": comparison.get("ats_before"),
#                 "ats_after": comparison.get("ats_after"),
#             }
#         )

#     runs.sort(
#         key=lambda x: x.get("created_at") or "",
#         reverse=True,
#     )

#     return runs

# def update_run(run_id: str, patch: dict[str, Any]) -> dict[str, Any]:
#     """
#     Shallow-merges `patch` into the stored run and saves it back.
#     Raises if the run doesn't exist yet.
#     """

#     existing = load_run(run_id)

#     if existing is None:
#         raise ValueError(f"No stored run found for run_id={run_id}")

#     existing.update(patch)

#     save_run(run_id, existing)

#     return existing


# def apply_dot_path(data: dict[str, Any], path: str, value: Any) -> dict[str, Any]:
#     """
#     Applies a single dot-path edit to a nested dict/list structure, e.g.:

#         apply_dot_path(resume_dict, "professional_summary.content", "New text")
#         apply_dot_path(resume_dict, "professional_experience.0.responsibilities", [...])
#         apply_dot_path(resume_dict, "professional_experience.0.projects.1.bullet_points.2", "Edited bullet")

#     Numeric path segments index into lists. Returns the mutated `data`
#     (mutated in place and also returned for convenience).
#     """

#     segments = path.split(".")
#     node = data

#     for seg in segments[:-1]:

#         key: Any = int(seg) if seg.isdigit() else seg
#         node = node[key]

#     last = segments[-1]
#     last_key: Any = int(last) if last.isdigit() else last
#     node[last_key] = value

#     return data


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


def list_runs() -> list[dict]:

    cursor = (
        get_runs_collection()
        .find(
            {},
            {
                "run_id": 1,
                "created_at": 1,
                "finalized": 1,
                "resume_name": 1,
                "parsed_jd.job_details.title": 1,
                "parsed_jd.job_details.company": 1,
                "comparison_data.ats_before": 1,
                "comparison_data.ats_after": 1,
                "_id": 0,
            },
        )
        .sort("created_at", -1)
    )

    runs = []

    for doc in cursor:

        jd_details = (doc.get("parsed_jd") or {}).get("job_details") or {}
        comparison = doc.get("comparison_data") or {}

        runs.append(
            {
                "run_id": doc.get("run_id"),
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