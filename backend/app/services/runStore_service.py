"""
Run Store

Persists a snapshot of each workflow run so the human-review flow can:

- fetch the current draft + suggestions for a run
- apply direct section edits
- apply approved suggestions and re-tailor
- keep a version history of tailored resumes for that run

This is intentionally a simple JSON-file store (one file per run_id) rather
than a database, matching the rest of this project's persistence style
(see InventoryStorageService). It's swappable for a real DB or LangGraph
checkpointer later without changing the API surface much.
"""

import json
from datetime import datetime
from pathlib import Path
from typing import Any, Optional

RUN_STORE_DIR = Path("app/data/runs")


def _run_path(run_id: str) -> Path:
    RUN_STORE_DIR.mkdir(parents=True, exist_ok=True)
    return RUN_STORE_DIR / f"{run_id}.json"


def save_run(run_id: str, data: dict[str, Any]) -> None:
    """
    Overwrites the full run record. `data` should already be
    JSON-serializable (e.g. via pydantic .model_dump(mode="json")).
    """

    path = _run_path(run_id)

    data = dict(data)
    data["run_id"] = run_id
    data["saved_at"] = datetime.utcnow().isoformat()

    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False, default=str)


def load_run(run_id: str) -> Optional[dict[str, Any]]:

    path = _run_path(run_id)

    if not path.exists():
        return None

    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)

def list_runs() -> list[dict]:
    runs = []

    for file in RUN_STORE_DIR.glob("*.json"):
        with open(file, "r", encoding="utf-8") as f:
            data = json.load(f)

        comparison = data.get("comparison_data") or {}
        jd = data.get("parsed_jd") or {}
        details = jd.get("job_details") or {}

        runs.append(
            {
                "run_id": file.stem,
                "created_at": data.get("created_at"),
                "finalized": data.get("finalized", False),
                "job_title": details.get("title"),
                "company": details.get("company"),
                "ats_before": comparison.get("ats_before"),
                "ats_after": comparison.get("ats_after"),
            }
        )

    runs.sort(
        key=lambda x: x.get("created_at") or "",
        reverse=True,
    )

    return runs

def update_run(run_id: str, patch: dict[str, Any]) -> dict[str, Any]:
    """
    Shallow-merges `patch` into the stored run and saves it back.
    Raises if the run doesn't exist yet.
    """

    existing = load_run(run_id)

    if existing is None:
        raise ValueError(f"No stored run found for run_id={run_id}")

    existing.update(patch)

    save_run(run_id, existing)

    return existing


def apply_dot_path(data: dict[str, Any], path: str, value: Any) -> dict[str, Any]:
    """
    Applies a single dot-path edit to a nested dict/list structure, e.g.:

        apply_dot_path(resume_dict, "professional_summary.content", "New text")
        apply_dot_path(resume_dict, "professional_experience.0.responsibilities", [...])
        apply_dot_path(resume_dict, "professional_experience.0.projects.1.bullet_points.2", "Edited bullet")

    Numeric path segments index into lists. Returns the mutated `data`
    (mutated in place and also returned for convenience).
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