"""Domain models for swimming pool data."""

from __future__ import annotations

import datetime
from dataclasses import dataclass
from enum import StrEnum


class City(StrEnum):
    """Supported cities."""

    AMSTERDAM = "Amsterdam"


class ActivityType(StrEnum):
    """Types of swimming activities."""

    LANE_SWIMMING = "baanzwemmen"
    RECREATIONAL = "recreatief zwemmen"
    EARLY_BIRD = "vroegzwemmen"
    LESSONS = "leszwemmen"


@dataclass(frozen=True, slots=True)
class TimeSlot:
    """A time slot during which a pool is open for a specific activity."""

    day: int  # ISO weekday (1=Monday, 7=Sunday)
    start: datetime.time
    end: datetime.time
    activity: ActivityType

    @property
    def duration_minutes(self) -> int:
        """Duration of the time slot in minutes."""
        start_dt = datetime.datetime.combine(datetime.date.min, self.start)
        end_dt = datetime.datetime.combine(datetime.date.min, self.end)
        return int((end_dt - start_dt).total_seconds() // 60)


@dataclass(frozen=True, slots=True)
class Pool:
    """A swimming pool with its schedule."""

    name: str
    city: City
    address: str
    slots: tuple[TimeSlot, ...]

    def open_on(self, day: int) -> tuple[TimeSlot, ...]:
        """Return all time slots for a given ISO weekday."""
        return tuple(s for s in self.slots if s.day == day)

    def by_activity(self, activity: ActivityType) -> tuple[TimeSlot, ...]:
        """Return all time slots for a given activity type."""
        return tuple(s for s in self.slots if s.activity == activity)
