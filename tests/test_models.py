"""Tests for zwemmr domain models."""

import datetime

import pytest

from zwemmr.models import ActivityType, City, Pool, TimeSlot


class TestTimeSlot:
    def test_duration_minutes(self) -> None:
        slot = TimeSlot(
            day=1,
            start=datetime.time(7, 0),
            end=datetime.time(8, 30),
            activity=ActivityType.EARLY_BIRD,
        )
        assert slot.duration_minutes == 90

    def test_frozen(self) -> None:
        slot = TimeSlot(
            day=1,
            start=datetime.time(7, 0),
            end=datetime.time(8, 0),
            activity=ActivityType.LANE_SWIMMING,
        )
        with pytest.raises(AttributeError):
            slot.day = 2  # type: ignore[misc]


class TestPool:
    @pytest.fixture()
    def pool(self) -> Pool:
        return Pool(
            name="Het Zuiderbad",
            city=City.AMSTERDAM,
            address="Hobbemastraat 26",
            slots=(
                TimeSlot(
                    1,
                    datetime.time(7, 0),
                    datetime.time(8, 30),
                    ActivityType.EARLY_BIRD,
                ),
                TimeSlot(
                    1,
                    datetime.time(12, 0),
                    datetime.time(13, 30),
                    ActivityType.LANE_SWIMMING,
                ),
                TimeSlot(
                    3,
                    datetime.time(19, 0),
                    datetime.time(21, 0),
                    ActivityType.RECREATIONAL,
                ),
            ),
        )

    def test_open_on_filters_by_day(self, pool: Pool) -> None:
        monday_slots = pool.open_on(1)
        assert len(monday_slots) == 2

    def test_open_on_empty(self, pool: Pool) -> None:
        assert pool.open_on(7) == ()

    def test_by_activity(self, pool: Pool) -> None:
        early = pool.by_activity(ActivityType.EARLY_BIRD)
        assert len(early) == 1
        assert early[0].start == datetime.time(7, 0)
