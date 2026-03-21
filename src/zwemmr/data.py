"""Data loading utilities for swimming pool information."""

from __future__ import annotations

from pathlib import Path

DATA_DIR = Path(__file__).resolve().parent.parent.parent / "data"


def get_data_path(filename: str) -> Path:
    """Resolve a data file path, raising FileNotFoundError if missing."""
    path = DATA_DIR / filename
    if not path.exists():
        msg = f"Data file not found: {path}"
        raise FileNotFoundError(msg)
    return path
