"""Tests for diagnostics."""

from __future__ import annotations

import json

from homeassistant.components.diagnostics import REDACTED

from custom_components.warmup.diagnostics import async_get_config_entry_diagnostics

from .conftest import room_of


async def test_diagnostics_redacts_personal_data(hass, setup, aioclient_mock, state):
    result = await async_get_config_entry_diagnostics(hass, setup)
    text = json.dumps(result)
    room = room_of(state)
    for value in ("user@example.com", "tok", room["roomName"], room["serial"], "Home"):
        assert f'"{value}"' not in text
    diag_room = result["rooms"][0]
    for key in ("id", "location_id", "name", "location_name", "serial", "schedule"):
        assert diag_room[key] == REDACTED
    assert result["entry"]["email"] == REDACTED
    assert diag_room["floor_temperature"] == 20.5
