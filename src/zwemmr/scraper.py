"""Crawl swimming pool schedule pages and extract structured data."""

from __future__ import annotations

import asyncio
import json
import logging
import os
from pathlib import Path

from crawl4ai import AsyncWebCrawler, CrawlerRunConfig, LLMConfig
from crawl4ai.extraction_strategy import LLMExtractionStrategy

from zwemmr.extraction import RoosterSchema, rooster_from_schema
from zwemmr.model import Rooster, save_rooster
from zwemmr.pools import ZwembadInfo

logger = logging.getLogger(__name__)

_EXTRACTION_INSTRUCTION = """\
Extract ALL swimming pool time slots from this schedule page.

For each time slot, provide:
- start: full ISO 8601 datetime with timezone Europe/Amsterdam \
(e.g. "2026-03-23T07:00:00+01:00")
- eind: full ISO 8601 datetime with timezone Europe/Amsterdam \
(e.g. "2026-03-23T09:00:00+01:00")
- activiteit: the activity type in Dutch. Use one of: banenzwemmen, \
vrij zwemmen, leszwemmen, aquarobics, recreatief zwemmen. \
If the activity doesn't match any of these, use the original Dutch name.
- opmerking: any special notes (e.g. "alleen crawlbaan", "dames", \
"25m bad"). Set to null if there are no special notes.

Extract the schedule for the upcoming week. Use the actual dates you see \
on the page. If the page shows times without dates, use the dates of \
the current week starting from today.

Return ALL time slots you can find.\
"""


def _make_llm_config() -> LLMConfig:
    api_key = os.environ.get("GEMINI_API_KEY", "")
    return LLMConfig(
        provider="gemini/gemini-3.1-flash-lite-preview",
        api_token=api_key,
    )


def _make_extraction_strategy() -> LLMExtractionStrategy:
    return LLMExtractionStrategy(
        llm_config=_make_llm_config(),
        schema=RoosterSchema.model_json_schema(),
        extraction_type="schema",
        instruction=_EXTRACTION_INSTRUCTION,
    )


async def scrape_pool(pool: ZwembadInfo) -> Rooster:
    """Scrape a single pool's schedule page and return structured data."""
    logger.info("Scraping %s from %s", pool.id, pool.scrape_url)
    strategy = _make_extraction_strategy()
    run_config = CrawlerRunConfig(extraction_strategy=strategy)

    async with AsyncWebCrawler() as crawler:
        result = await crawler.arun(url=pool.scrape_url, config=run_config)

    raw = json.loads(result.extracted_content)
    if isinstance(raw, list):
        raw = raw[0] if raw else {"tijdsloten": []}
    schema = RoosterSchema.model_validate(raw)
    return rooster_from_schema(pool.id, pool.naam, pool.scrape_url, schema)


async def scrape_all(
    pools: tuple[ZwembadInfo, ...],
    output_dir: Path,
) -> list[Rooster]:
    """Scrape all pools sequentially and save results as JSON."""
    roosters: list[Rooster] = []
    for pool in pools:
        try:
            rooster = await scrape_pool(pool)
            path = save_rooster(rooster, output_dir)
            logger.info(
                "Saved %d time slots for %s to %s",
                len(rooster.tijdsloten),
                pool.id,
                path,
            )
            roosters.append(rooster)
        except Exception:
            logger.exception("Failed to scrape %s", pool.id)
    return roosters


def run_scrape(
    pools: tuple[ZwembadInfo, ...],
    output_dir: Path,
) -> list[Rooster]:
    """Synchronous entry point for scraping."""
    return asyncio.run(scrape_all(pools, output_dir))
