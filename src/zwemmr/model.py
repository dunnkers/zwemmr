"""Domain model for swimming pool schedules."""

from __future__ import annotations

import json
from dataclasses import dataclass
from datetime import datetime
from enum import StrEnum
from pathlib import Path


class Activiteit(StrEnum):
    """Type of swimming activity."""

    BANENZWEMMEN = "banenzwemmen"
    VRIJ_ZWEMMEN = "vrij_zwemmen"
    LESZWEMMEN = "leszwemmen"
    AQUAROBICS = "aquarobics"
    RECREATIEF_ZWEMMEN = "recreatief_zwemmen"
    OVERIG = "overig"


@dataclass(frozen=True)
class Tijdslot:
    """A concrete scheduled time slot at a pool."""

    start: datetime
    eind: datetime
    activiteit: Activiteit
    opmerking: str | None = None


@dataclass(frozen=True)
class Rooster:
    """Complete scraped schedule for one pool."""

    zwembad_id: str
    naam: str
    bron_url: str
    scrape_datum: datetime
    tijdsloten: tuple[Tijdslot, ...]


def tijdslot_to_dict(slot: Tijdslot) -> dict[str, str | None]:
    return {
        "start": slot.start.isoformat(),
        "eind": slot.eind.isoformat(),
        "activiteit": slot.activiteit.value,
        "opmerking": slot.opmerking,
    }


def tijdslot_from_dict(d: dict[str, str | None]) -> Tijdslot:
    return Tijdslot(
        start=datetime.fromisoformat(d["start"]),  # type: ignore[arg-type]
        eind=datetime.fromisoformat(d["eind"]),  # type: ignore[arg-type]
        activiteit=Activiteit(d["activiteit"]),
        opmerking=d.get("opmerking"),
    )


def rooster_to_dict(rooster: Rooster) -> dict[str, object]:
    return {
        "zwembad_id": rooster.zwembad_id,
        "naam": rooster.naam,
        "bron_url": rooster.bron_url,
        "scrape_datum": rooster.scrape_datum.isoformat(),
        "tijdsloten": [tijdslot_to_dict(s) for s in rooster.tijdsloten],
    }


def rooster_from_dict(d: dict[str, object]) -> Rooster:
    return Rooster(
        zwembad_id=str(d["zwembad_id"]),
        naam=str(d["naam"]),
        bron_url=str(d["bron_url"]),
        scrape_datum=datetime.fromisoformat(str(d["scrape_datum"])),
        tijdsloten=tuple(
            tijdslot_from_dict(s)
            for s in d["tijdsloten"]  # type: ignore[union-attr]
        ),
    )


def save_rooster(rooster: Rooster, output_dir: Path) -> Path:
    """Save a rooster as JSON to {output_dir}/{zwembad_id}/{YYYY-MM-DD}.json."""
    pool_dir = output_dir / rooster.zwembad_id
    pool_dir.mkdir(parents=True, exist_ok=True)
    date_str = rooster.scrape_datum.strftime("%Y-%m-%d")
    path = pool_dir / f"{date_str}.json"
    path.write_text(
        json.dumps(rooster_to_dict(rooster), indent=2, ensure_ascii=False) + "\n",
        encoding="utf-8",
    )
    return path
