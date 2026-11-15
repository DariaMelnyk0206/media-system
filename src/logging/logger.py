"""
src/logging/logger.py
~~~~~~~~~~~~~~~~~~~~~
Logging configuration for the Personal Media Library System.

Requirements: REQ-NF-005 (operational logging), REQ-NF-006 (non-intrusive).

Two handlers are attached to the root application logger ("pmls"):
  - FileHandler  → logs/system.log  (append, UTF-8)
  - StreamHandler → stderr

Log format:
  2026-11-15 18:00:00,123  INFO      pmls.routes   GET /api/media-items → 200 (12ms)

Usage:
  from src.logging.logger import get_logger
  log = get_logger(__name__)
  log.info("component started")
"""

from __future__ import annotations

import logging
import sys
from pathlib import Path

# ---------------------------------------------------------------------------
# Constants
# ---------------------------------------------------------------------------

_LOG_DIR = Path(__file__).resolve().parents[2] / "logs"
_LOG_FILE = _LOG_DIR / "system.log"

_FORMAT = "%(asctime)s  %(levelname)-8s  %(name)s  %(message)s"
_DATE_FORMAT = "%Y-%m-%d %H:%M:%S"

_ROOT_LOGGER_NAME = "pmls"

# ---------------------------------------------------------------------------
# Internal state — ensure setup() runs exactly once
# ---------------------------------------------------------------------------

_configured = False


def _setup() -> None:
    """Configure handlers on the root application logger.

    Called automatically on first ``get_logger`` invocation.
    Safe to call multiple times — only the first call has any effect.
    """
    global _configured  # noqa: PLW0603
    if _configured:
        return

    # Ensure logs/ directory exists (created at app start, not tracked by git).
    _LOG_DIR.mkdir(parents=True, exist_ok=True)

    logger = logging.getLogger(_ROOT_LOGGER_NAME)
    logger.setLevel(logging.DEBUG)

    formatter = logging.Formatter(fmt=_FORMAT, datefmt=_DATE_FORMAT)

    # --- File handler (append, UTF-8) ---
    file_handler = logging.FileHandler(_LOG_FILE, mode="a", encoding="utf-8")
    file_handler.setLevel(logging.DEBUG)
    file_handler.setFormatter(formatter)

    # --- Console handler (stderr) ---
    console_handler = logging.StreamHandler(sys.stderr)
    console_handler.setLevel(logging.INFO)
    console_handler.setFormatter(formatter)

    logger.addHandler(file_handler)
    logger.addHandler(console_handler)

    # Prevent log records from propagating to the root logging hierarchy,
    # which would cause duplicate output if the host process configures its
    # own root handlers (e.g. uvicorn).
    logger.propagate = False

    _configured = True


def get_logger(name: str) -> logging.Logger:
    """Return a child logger under the ``pmls`` namespace.

    Args:
        name: Typically ``__name__`` of the calling module.
              The prefix ``src.`` is stripped so logger names stay concise,
              e.g. ``pmls.routes`` instead of ``pmls.src.routes``.

    Returns:
        A configured :class:`logging.Logger` instance.

    Example::

        log = get_logger(__name__)
        log.info("MediaItem created  id=%s", item_id)
    """
    _setup()

    # Strip leading "src." so callers inside the package get clean names.
    short_name = name.removeprefix("src.")
    return logging.getLogger(f"{_ROOT_LOGGER_NAME}.{short_name}")
