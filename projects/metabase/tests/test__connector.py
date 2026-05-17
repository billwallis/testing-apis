from __future__ import annotations

import dataclasses
from types import SimpleNamespace

import pytest
from metabase import connector

BASE_URL = "https://domain:0000/api/"


@dataclasses.dataclass
class Credentials:
    base_url: str
    api_key: str
    api_secret: str

    @classmethod
    def default(cls) -> Credentials:
        return cls(
            base_url=BASE_URL,
            api_key="some-key",
            api_secret="some-secret",
        )


@pytest.fixture
def connection(monkeypatch: pytest.MonkeyPatch) -> connector.MetabaseConnector:
    monkeypatch.setattr(
        connector.MetabaseConnector,
        "sign_in",
        lambda _: SimpleNamespace(json=lambda: {"id": "a1b2-c3d4"}),
    )
    creds = Credentials.default()
    return connector.MetabaseConnector(
        base_url=creds.base_url,
        api_key=creds.api_key,
        api_secret=creds.api_secret,
    )


def test__connector_properties_are_correct(
    connection: connector.MetabaseConnector,
):
    assert connection.base_url == BASE_URL
    assert connection.request_headers == {
        "Content-Type": "application/json",
        "Accept": "application/json",
        "X-Metabase-Session": "a1b2-c3d4",
    }
