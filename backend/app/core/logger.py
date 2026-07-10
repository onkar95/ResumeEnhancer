"""
Application Logger

Provides a centralized logger for the entire application.

Features
--------
- Console logging
- File logging
- Rotating log files
- Singleton logger
"""

from pathlib import Path
import logging
from logging.handlers import RotatingFileHandler


# ==========================================================
# Log Directory
# ==========================================================

LOG_DIR = Path("logs")
LOG_DIR.mkdir(exist_ok=True)

LOG_FILE = LOG_DIR / "app.log"


# ==========================================================
# Logger Configuration
# ==========================================================

LOGGER_NAME = "resume_tailor"

logger = logging.getLogger(LOGGER_NAME)

logger.setLevel(logging.INFO)


# Prevent duplicate handlers during reload
if not logger.handlers:

    # ------------------------------------------------------
    # Console Handler
    # ------------------------------------------------------

    console_handler = logging.StreamHandler()

    console_handler.setLevel(logging.INFO)

    console_formatter = logging.Formatter(
        "%(asctime)s | %(levelname)-8s | %(message)s",
        datefmt="%H:%M:%S",
    )

    console_handler.setFormatter(
        console_formatter
    )

    # ------------------------------------------------------
    # File Handler
    # ------------------------------------------------------

    file_handler = RotatingFileHandler(
        filename=LOG_FILE,
        maxBytes=5 * 1024 * 1024,  # 5 MB
        backupCount=5,
        encoding="utf-8",
    )

    file_handler.setLevel(logging.INFO)

    file_formatter = logging.Formatter(
        "%(asctime)s | %(levelname)-8s | %(name)s | %(filename)s:%(lineno)d | %(message)s"
    )

    file_handler.setFormatter(
        file_formatter
    )

    # ------------------------------------------------------
    # Attach Handlers
    # ------------------------------------------------------

    logger.addHandler(console_handler)

    logger.addHandler(file_handler)

    logger.propagate = False