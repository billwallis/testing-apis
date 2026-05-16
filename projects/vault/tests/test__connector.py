from __future__ import annotations

import dataclasses
from types import SimpleNamespace

import pytest
from vault import connector

BASE_URL = "https://vault.test/v1/"
MOCK_SIGN_IN_RESPONSE = {"auth": {"client_token": "a1b2-c3d4"}}


@dataclasses.dataclass
class Credentials:
    domain: str
    api_key: str
    api_secret: str

    @classmethod
    def default(cls) -> Credentials:
        return cls(
            domain="vault.test",
            api_key="some-key",
            api_secret="some-secret",
        )


@pytest.fixture
def connection(monkeypatch: pytest.MonkeyPatch) -> connector.VaultConnector:
    monkeypatch.setattr(
        connector.VaultConnector,
        "sign_in",
        lambda _: SimpleNamespace(json=lambda: MOCK_SIGN_IN_RESPONSE),
    )
    creds = Credentials.default()
    return connector.VaultConnector(
        domain=creds.domain,
        api_key=creds.api_key,
        api_secret=creds.api_secret,
    )


def test__invalid_auth_type_raise_an_error():
    with pytest.raises(ValueError):
        connector.VaultConnector(
            domain="",
            api_key="",
            api_secret="",
        )


def test__connector_properties_are_correct(
    connection: connector.VaultConnector,
):
    assert connection.base_url == BASE_URL
    assert connection.request_headers == {
        "Content-Type": "application/json",
        "Accept": "application/json",
        "X-Vault-Token": "a1b2-c3d4",
    }
