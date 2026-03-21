"""Tests for data loading utilities."""

import pytest

from zwemmr.data import get_data_path


class TestGetDataPath:
    def test_missing_file_raises(self) -> None:
        with pytest.raises(FileNotFoundError, match="Data file not found"):
            get_data_path("nonexistent.xlsx")

    def test_existing_file(self) -> None:
        path = get_data_path("zwembaden_amsterdam.xlsx")
        assert path.exists()
        assert path.name == "zwembaden_amsterdam.xlsx"
