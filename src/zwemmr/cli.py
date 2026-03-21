"""CLI entry point for scraping swimming pool schedules."""

from __future__ import annotations

import argparse
import logging
from pathlib import Path

from zwemmr.pools import load_pools
from zwemmr.scraper import run_scrape


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Scrape swimming pool schedules",
    )
    parser.add_argument(
        "--pool",
        help="Scrape only this pool ID (default: all pools)",
    )
    parser.add_argument(
        "--output-dir",
        default="data/roosters",
        help="Output directory for JSON files (default: data/roosters)",
    )
    parser.add_argument(
        "--csv",
        default=None,
        help="Path to the pools CSV file (default: data/zwembaden_amsterdam.csv)",
    )
    parser.add_argument(
        "-v",
        "--verbose",
        action="store_true",
        help="Enable verbose logging",
    )
    args = parser.parse_args()

    logging.basicConfig(
        level=logging.DEBUG if args.verbose else logging.INFO,
        format="%(asctime)s %(levelname)s %(name)s: %(message)s",
    )

    csv_path = Path(args.csv) if args.csv else None
    pools = load_pools(csv_path)

    if args.pool:
        pools = tuple(p for p in pools if p.id == args.pool)
        if not pools:
            parser.error(f"Pool '{args.pool}' not found in CSV")

    output_dir = Path(args.output_dir)
    roosters = run_scrape(pools, output_dir)
    logging.getLogger(__name__).info("Scraped %d pools successfully", len(roosters))
