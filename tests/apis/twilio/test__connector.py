from __future__ import annotations

import dataclasses

import pytest

from src.apis.twilio import connector

WORKSPACE = "WS123"
BASE_URL = f"https://taskrouter.twilio.com/v1/Workspaces/{WORKSPACE}/"


@dataclasses.dataclass
class Credentials:
    workspace: str
    api_key: str
    api_secret: str

    @classmethod
    def default(cls) -> Credentials:
        return cls(
            workspace=WORKSPACE,
            api_key="some-key",
            api_secret="some-secret",
        )


@pytest.fixture
def connection(monkeypatch: pytest.MonkeyPatch) -> connector.TwilioConnector:
    creds = Credentials.default()
    return connector.TwilioConnector(
        workspace=creds.workspace,
        api_key=creds.api_key,
        api_secret=creds.api_secret,
    )


def test__connector_properties_are_correct(
    connection: connector.TwilioConnector,
):
    assert connection.base_url == BASE_URL
    assert connection.auth == ("some-key", "some-secret")
    assert connection.request_headers == {
        "Content-Type": "application/json",
        "Accept": "application/json",
    }
