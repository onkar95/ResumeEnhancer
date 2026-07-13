from pathlib import Path
import hashlib
import json

CACHE_DIR = Path("cache")


def build_cache_key(
    prompt: str,
    prefix: str = ""
) -> str:

    raw = f"{prefix}\n{prompt}"

    return hashlib.md5(
        raw.encode("utf-8")
    ).hexdigest()


def load_cache(
    cache_key: str
):

    path = CACHE_DIR / f"{cache_key}.json"

    if not path.exists():
        return None

    try:

        with open(
            path,
            "r",
            encoding="utf-8"
        ) as f:

            return json.load(f)

    except Exception:
        return None


def save_cache(
    cache_key: str,
    data
):

    CACHE_DIR.mkdir(
        parents=True,
        exist_ok=True
    )

    path = CACHE_DIR / f"{cache_key}.json"

    with open(
        path,
        "w",
        encoding="utf-8"
    ) as f:

        json.dump(
            data,
            f,
            indent=2,
            ensure_ascii=False
        )