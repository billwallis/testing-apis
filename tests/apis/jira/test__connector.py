from __future__ import annotations

import dataclasses

import pytest

from src.apis.jira import connector

DOMAIN = "test-domain"
BASE_URL = f"https://{DOMAIN}.atlassian.net/rest/api/3/"


@dataclasses.dataclass
class Credentials:
    domain: str
    api_key: str
    api_secret: str

    @classmethod
    def default(cls) -> Credentials:
        return cls(
            domain=DOMAIN,
            api_key="some-key",
            api_secret="some-secret",
        )


@pytest.fixture
def connection() -> connector.JiraConnector:
    creds = Credentials.default()
    return connector.JiraConnector(
        domain=creds.domain,
        api_key=creds.api_key,
        api_secret=creds.api_secret,
    )


def test__connector_properties_are_correct(connection: connector.JiraConnector):
    assert connection.base_url == BASE_URL
    assert connection.request_headers == {
        "Content-Type": "application/json",
        "Accept": "application/json",
        "Authorization": "Basic c29tZS1rZXk6c29tZS1zZWNyZXQ=",
    }
