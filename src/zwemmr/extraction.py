"""Pydantic schemas for LLM extraction and conversion to domain model."""

from __future__ import annotations

from datetime import datetime
from zoneinfo import ZoneInfo

from pydantic import BaseModel, Field

from zwemmr.model import Activiteit, Rooster, Tijdslot

AMS_TZ = ZoneInfo("Europe/Amsterdam")

_ACTIVITEIT_MAP: dict[str, Activiteit] = {
    "banenzwemmen": Activiteit.BANENZWEMMEN,
    "baanzwemmen": Activiteit.BANENZWEMMEN,
    "lane swimming": Activiteit.BANENZWEMMEN,
    "vrij zwemmen": Activiteit.VRIJ_ZWEMMEN,
    "vrij_zwemmen": Activiteit.VRIJ_ZWEMMEN,
    "free swimming": Activiteit.VRIJ_ZWEMMEN,
    "leszwemmen": Activiteit.LESZWEMMEN,
    "zwemles": Activiteit.LESZWEMMEN,
    "aquarobics": Activiteit.AQUAROBICS,
    "aqua-aerobics": Activiteit.AQUAROBICS,
    "aquagym": Activiteit.AQUAROBICS,
    "recreatief zwemmen": Activiteit.RECREATIEF_ZWEMMEN,
    "recreatief_zwemmen": Activiteit.RECREATIEF_ZWEMMEN,
    "recreatiezwemmen": Activiteit.RECREATIEF_ZWEMMEN,
}


class TijdslotSchema(BaseModel):
    """LLM extraction schema for a single time slot."""

    start: str = Field(..., description="Start datetime in ISO 8601 format")
    eind: str = Field(..., description="End datetime in ISO 8601 format")
    activiteit: str = Field(
        ...,
        description=(
            "Activity type in Dutch, e.g. banenzwemmen, vrij zwemmen, "
            "leszwemmen, aquarobics, recreatief zwemmen"
        ),
    )
    opmerking: str | None = Field(
        None, description="Any special notes, e.g. 'alleen crawlbaan', 'dames-only'"
    )


class RoosterSchema(BaseModel):
    """LLM extraction schema for a pool schedule."""

    tijdsloten: list[TijdslotSchema] = Field(
        ..., description="All scheduled time slots found on the page"
    )


def _parse_activiteit(raw: str) -> Activiteit:
    """Map a raw activiteit string to the Activiteit enum."""
    normalized = raw.strip().lower()
    if normalized in _ACTIVITEIT_MAP:
        return _ACTIVITEIT_MAP[normalized]
    for key, value in _ACTIVITEIT_MAP.items():
        if key in normalized or normalized in key:
            return value
    return Activiteit.OVERIG


def _ensure_tz_aware(dt: datetime) -> datetime:
    """Ensure a datetime is tz-aware in Europe/Amsterdam."""
    if dt.tzinfo is None:
        return dt.replace(tzinfo=AMS_TZ)
    return dt.astimezone(AMS_TZ)


def rooster_from_schema(
    zwembad_id: str,
    naam: str,
    bron_url: str,
    schema: RoosterSchema,
) -> Rooster:
    """Convert LLM extraction schema to domain model."""
    now = _ensure_tz_aware(datetime.now(tz=AMS_TZ))
    tijdsloten = tuple(
        Tijdslot(
            start=_ensure_tz_aware(datetime.fromisoformat(s.start)),
            eind=_ensure_tz_aware(datetime.fromisoformat(s.eind)),
            activiteit=_parse_activiteit(s.activiteit),
            opmerking=s.opmerking,
        )
        for s in schema.tijdsloten
    )
    return Rooster(
        zwembad_id=zwembad_id,
        naam=naam,
        bron_url=bron_url,
        scrape_datum=now,
        tijdsloten=tijdsloten,
    )
