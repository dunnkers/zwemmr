"""Tests for domain model and extraction conversion."""

from __future__ import annotations

import json
from datetime import datetime
from zoneinfo import ZoneInfo

from zwemmr.extraction import (
    RoosterSchema,
    TijdslotSchema,
    _parse_activiteit,
    rooster_from_schema,
)
from zwemmr.model import (
    Activiteit,
    Rooster,
    Tijdslot,
    rooster_from_dict,
    rooster_to_dict,
)

AMS = ZoneInfo("Europe/Amsterdam")


class TestActiviteit:
    def test_enum_values(self) -> None:
        assert Activiteit.BANENZWEMMEN == "banenzwemmen"
        assert Activiteit.VRIJ_ZWEMMEN == "vrij_zwemmen"
        assert Activiteit.LESZWEMMEN == "leszwemmen"
        assert Activiteit.AQUAROBICS == "aquarobics"
        assert Activiteit.RECREATIEF_ZWEMMEN == "recreatief_zwemmen"
        assert Activiteit.OVERIG == "overig"

    def test_enum_has_six_members(self) -> None:
        assert len(Activiteit) == 6


class TestParseActiviteit:
    def test_exact_match(self) -> None:
        assert _parse_activiteit("banenzwemmen") == Activiteit.BANENZWEMMEN

    def test_synonym_match(self) -> None:
        assert _parse_activiteit("baanzwemmen") == Activiteit.BANENZWEMMEN
        assert _parse_activiteit("zwemles") == Activiteit.LESZWEMMEN

    def test_case_insensitive(self) -> None:
        assert _parse_activiteit("Banenzwemmen") == Activiteit.BANENZWEMMEN

    def test_with_whitespace(self) -> None:
        assert _parse_activiteit("  vrij zwemmen  ") == Activiteit.VRIJ_ZWEMMEN

    def test_partial_match(self) -> None:
        assert _parse_activiteit("aquarobics voor senioren") == Activiteit.AQUAROBICS

    def test_unknown_maps_to_overig(self) -> None:
        assert _parse_activiteit("discozwemmen") == Activiteit.OVERIG
        assert _parse_activiteit("waterpolo") == Activiteit.OVERIG


class TestTijdslot:
    def test_frozen(self) -> None:
        slot = Tijdslot(
            start=datetime(2026, 3, 23, 7, 0, tzinfo=AMS),
            eind=datetime(2026, 3, 23, 9, 0, tzinfo=AMS),
            activiteit=Activiteit.BANENZWEMMEN,
        )
        assert slot.activiteit == Activiteit.BANENZWEMMEN
        assert slot.opmerking is None

    def test_with_opmerking(self) -> None:
        slot = Tijdslot(
            start=datetime(2026, 3, 23, 7, 0, tzinfo=AMS),
            eind=datetime(2026, 3, 23, 9, 0, tzinfo=AMS),
            activiteit=Activiteit.BANENZWEMMEN,
            opmerking="alleen crawlbaan",
        )
        assert slot.opmerking == "alleen crawlbaan"


class TestRoosterFromSchema:
    def test_basic_conversion(self) -> None:
        schema = RoosterSchema(
            tijdsloten=[
                TijdslotSchema(
                    start="2026-03-23T07:00:00+01:00",
                    eind="2026-03-23T09:00:00+01:00",
                    activiteit="banenzwemmen",
                    opmerking=None,
                ),
                TijdslotSchema(
                    start="2026-03-23T10:00:00+01:00",
                    eind="2026-03-23T12:00:00+01:00",
                    activiteit="vrij zwemmen",
                    opmerking="25m bad",
                ),
            ]
        )
        rooster = rooster_from_schema(
            "zuiderbad", "Het Zuiderbad", "https://example.com", schema
        )
        assert rooster.zwembad_id == "zuiderbad"
        assert rooster.naam == "Het Zuiderbad"
        assert len(rooster.tijdsloten) == 2
        assert rooster.tijdsloten[0].activiteit == Activiteit.BANENZWEMMEN
        assert rooster.tijdsloten[1].activiteit == Activiteit.VRIJ_ZWEMMEN
        assert rooster.tijdsloten[1].opmerking == "25m bad"

    def test_naive_datetimes_get_tz(self) -> None:
        schema = RoosterSchema(
            tijdsloten=[
                TijdslotSchema(
                    start="2026-03-23T07:00:00",
                    eind="2026-03-23T09:00:00",
                    activiteit="leszwemmen",
                ),
            ]
        )
        rooster = rooster_from_schema("test", "Test", "https://example.com", schema)
        assert rooster.tijdsloten[0].start.tzinfo is not None

    def test_unknown_activiteit_maps_to_overig(self) -> None:
        schema = RoosterSchema(
            tijdsloten=[
                TijdslotSchema(
                    start="2026-03-23T07:00:00+01:00",
                    eind="2026-03-23T09:00:00+01:00",
                    activiteit="waterpolo",
                ),
            ]
        )
        rooster = rooster_from_schema("test", "Test", "https://example.com", schema)
        assert rooster.tijdsloten[0].activiteit == Activiteit.OVERIG

    def test_empty_tijdsloten(self) -> None:
        schema = RoosterSchema(tijdsloten=[])
        rooster = rooster_from_schema("test", "Test", "https://example.com", schema)
        assert rooster.tijdsloten == ()


class TestJsonRoundtrip:
    def test_rooster_roundtrip(self) -> None:
        original = Rooster(
            zwembad_id="zuiderbad",
            naam="Het Zuiderbad",
            bron_url="https://example.com",
            scrape_datum=datetime(2026, 3, 21, 10, 30, tzinfo=AMS),
            tijdsloten=(
                Tijdslot(
                    start=datetime(2026, 3, 23, 7, 0, tzinfo=AMS),
                    eind=datetime(2026, 3, 23, 9, 0, tzinfo=AMS),
                    activiteit=Activiteit.BANENZWEMMEN,
                    opmerking="test",
                ),
            ),
        )
        d = rooster_to_dict(original)
        json_str = json.dumps(d)
        restored = rooster_from_dict(json.loads(json_str))

        assert restored.zwembad_id == original.zwembad_id
        assert restored.naam == original.naam
        assert restored.bron_url == original.bron_url
        assert len(restored.tijdsloten) == 1
        assert restored.tijdsloten[0].activiteit == Activiteit.BANENZWEMMEN
        assert restored.tijdsloten[0].opmerking == "test"
