"""Live LLM test: validate structured extraction with google-genai."""

from __future__ import annotations

import os
import unittest

import pytest

pytestmark = pytest.mark.live

_SAMPLE_HTML = """\
<html><body>
<h1>Zwembad De Test - Rooster</h1>
<table>
  <tr><th>Dag</th><th>Tijd</th><th>Activiteit</th></tr>
  <tr><td>Maandag 24 maart 2026</td><td>07:00 - 09:00</td><td>Banenzwemmen</td></tr>
  <tr><td>Maandag 24 maart 2026</td><td>10:00 - 12:00</td><td>Vrij zwemmen</td></tr>
  <tr><td>Dinsdag 25 maart 2026</td><td>07:00 - 08:30</td><td>Banenzwemmen</td></tr>
</table>
</body></html>
"""


@unittest.skipUnless(
    os.environ.get("GEMINI_API_KEY"),
    "GEMINI_API_KEY not set",
)
class TestLiveLLMExtraction:
    """Send a hardcoded HTML snippet to Gemini and validate structured parsing."""

    def test_extract_schedule_from_html(self) -> None:
        from google import genai
        from google.genai import types

        from zwemmr.extraction import RoosterSchema, rooster_from_schema
        from zwemmr.model import Activiteit

        client = genai.Client(api_key=os.environ["GEMINI_API_KEY"])

        prompt = (
            "Extract all swimming pool time slots from this HTML schedule.\n\n"
            f"{_SAMPLE_HTML}\n\n"
            "For each slot provide start and eind as ISO 8601 datetimes "
            "with timezone Europe/Amsterdam (+01:00 for CET). "
            "Use the dates shown in the HTML. "
            "For activiteit use the Dutch activity name as shown."
        )

        response = client.models.generate_content(
            model="gemini-3.1-flash-lite-preview",
            contents=prompt,
            config=types.GenerateContentConfig(
                response_mime_type="application/json",
                response_json_schema=RoosterSchema,
            ),
        )

        assert response.text is not None
        schema = RoosterSchema.model_validate_json(response.text)
        assert len(schema.tijdsloten) == 3

        rooster = rooster_from_schema(
            "test_pool", "Zwembad De Test", "https://example.com", schema
        )
        assert rooster.zwembad_id == "test_pool"
        assert len(rooster.tijdsloten) == 3
        assert rooster.tijdsloten[0].activiteit == Activiteit.BANENZWEMMEN
