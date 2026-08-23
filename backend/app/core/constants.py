"""
Application Constants
"""

from pathlib import Path

# ==========================================================
# Directories
# ==========================================================

UPLOAD_DIR = Path("uploads")

UPLOAD_DIR.mkdir(
    exist_ok=True,
)

# ==========================================================
# File Types
# ==========================================================

SUPPORTED_EXTENSIONS = [
    ".pdf",
]

SUPPORTED_MIME_TYPES = [
    "application/pdf",
]

# ==========================================================
# Upload Limits
# ==========================================================

MAX_UPLOAD_SIZE = 10 * 1024 * 1024
MAX_CHAT_REVISIONS = 5
# 10 MB

# ==========================================================
# LLM
# ==========================================================

DEFAULT_TEMPERATURE = 0.1

DEFAULT_MAX_TOKENS = 4096

SECTION_SKILL = "skill"

SECTION_SUMMARY = "professional_summary"

SECTION_EXPERIENCE = "experience"

SECTION_PROJECT = "project"

SECTION_CERTIFICATION = "certification"

SECTION_EDUCATION = "education"

SECTION_ACHIEVEMENT = "achievement"