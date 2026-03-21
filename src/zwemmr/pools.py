"""Load swimming pool metadata from CSV."""

from __future__ import annotations

import csv
from dataclasses import dataclass
from pathlib import Path

_DEFAULT_CSV = (
    Path(__file__).resolve().parent.parent.parent / "data" / "zwembaden_amsterdam.csv"
)


@dataclass(frozen=True)
class ZwembadInfo:
    """Metadata for a single swimming pool."""

    id: str
    naam: str
    scrape_url: str
    scrape_methode: str


def load_pools(csv_path: Path | None = None) -> tuple[ZwembadInfo, ...]:
    """Load pool metadata from CSV, filtering to pools with a scrape_url."""
    path = csv_path or _DEFAULT_CSV
    with path.open(encoding="utf-8") as f:
        reader = csv.DictReader(f)
        pools = []
        for row in reader:
            scrape_url = row.get("scrape_url", "").strip()
            if not scrape_url:
                continue
            pools.append(
                ZwembadInfo(
                    id=row["id"].strip(),
                    naam=row["naam"].strip(),
                    scrape_url=scrape_url,
                    scrape_methode=row.get("scrape_methode", "html").strip(),
                )
            )
    return tuple(pools)
