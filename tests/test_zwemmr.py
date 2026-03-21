"""Smoke test for zwemmr package."""

import zwemmr


def test_import() -> None:
    assert zwemmr.__doc__ is not None
