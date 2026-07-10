# import json
# import re


# def parse_llm_json(response: str):
#     print("=" * 100)
#     print(repr(response[:200]))
#     print("=" * 100)

#     response = response.strip()

#     response = re.sub(r"^```json\s*", "", response)
#     response = re.sub(r"^```\s*", "", response)
#     response = re.sub(r"\s*```$", "", response)

#     response = response.strip()

#     # return json.loads(response)

#     return json.loads(response.strip())

"""
JSON Utility Functions

Provides helper functions for safely parsing JSON returned by LLMs.

Handles:

- ```json ... ``` fenced responses
- plain JSON
- malformed markdown wrappers

Author: Resume Tailor AI
"""

import json
import re
from typing import Any


class JSONParsingError(Exception):
    """Raised when LLM output cannot be parsed as JSON."""



def clean_json_response(response: str) -> str:
    """
    Remove markdown code fences from LLM output.

    Example

    ```json
    {}
    ```

    becomes

    {}
    """

    if not response:
        raise JSONParsingError("Empty LLM response.")

    cleaned = response.strip()

    cleaned = re.sub(
        r"^```json\s*",
        "",
        cleaned,
        flags=re.IGNORECASE,
    )

    cleaned = re.sub(
        r"^```",
        "",
        cleaned,
    )

    cleaned = re.sub(
        r"```$",
        "",
        cleaned,
    )

    return cleaned.strip()


def parse_llm_json(response: str) -> dict[str, Any]:
    """
    Parse JSON returned by an LLM.

    Raises JSONParsingError if parsing fails.
    """

    cleaned = clean_json_response(response)

    try:
        return json.loads(cleaned)

    except json.JSONDecodeError as exc:
        raise JSONParsingError(
            f"Failed to parse JSON.\n\nResponse:\n{cleaned}"
        ) from exc

def extract_json(response: str) -> dict:
    """
    Extract JSON from LLM response.
    Handles markdown wrapped responses.
    """

    response = response.strip()

    response = re.sub(
        r"^```json",
        "",
        response,
        flags=re.IGNORECASE,
    )

    response = re.sub(
        r"```$",
        "",
        response,
    )

    response = response.strip()

    return json.loads(response)