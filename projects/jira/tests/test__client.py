from __future__ import annotations

import dataclasses

import pytest
from jira import client

DOMAIN = "test-domain"
BASE_URL = f"https://{DOMAIN}.atlassian.net/"


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
def jira_client() -> client.JiraClient:
    creds = Credentials.default()
    return client.JiraClient(
        domain=creds.domain,
        api_key=creds.api_key,
        api_secret=creds.api_secret,
    )


def test__connector_properties_are_correct(jira_client: client.JiraClient):
    assert jira_client.base_url == BASE_URL
    assert jira_client.request_headers == {
        "Content-Type": "application/json",
        "Accept": "application/json",
        "Authorization": "Basic c29tZS1rZXk6c29tZS1zZWNyZXQ=",
    }
