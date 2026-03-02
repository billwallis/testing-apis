from __future__ import annotations

import dataclasses
from types import SimpleNamespace

import pytest

from src.apis.tableau import connector

BASE_URL = "https://tableau.test/api/3.8/"
MOCK_SIGN_IN_RESPONSE = {
    "credentials": {
        "token": "a1b2-c3d4",
        "site": {
            "id": "site-id",
        },
        "user": {
            "id": "user-id",
        },
    },
}


@dataclasses.dataclass
class Credentials:
    domain: str
    api_key: str
    api_secret: str
    auth_type: str

    @classmethod
    def default(cls) -> Credentials:
        return cls(
            domain="tableau.test",
            api_key="some-key",
            api_secret="some-secret",
            auth_type="uap",
        )


@pytest.fixture
def connection(monkeypatch: pytest.MonkeyPatch) -> connector.TableauConnector:
    monkeypatch.setattr(
        connector.TableauConnector,
        "sign_in",
        lambda _: SimpleNamespace(json=lambda: MOCK_SIGN_IN_RESPONSE),
    )
    creds = Credentials.default()
    return connector.TableauConnector(
        domain=creds.domain,
        api_key=creds.api_key,
        api_secret=creds.api_secret,
        auth_type=creds.auth_type,
    )


def test__invalid_auth_type_raise_an_error():
    with pytest.raises(ValueError):
        connector.TableauConnector(
            domain="",
            api_key="",
            api_secret="",
            auth_type="bad-auth-type",
        )


def test__connector_properties_are_correct(
    connection: connector.TableauConnector,
):
    assert connection.base_url == BASE_URL
    assert (
        connection.auth_type == connector.TableauAuthType.USERNAME_AND_PASSWORD
    )
    assert connection.credentials == {
        "name": "some-key",
        "password": "some-secret",
        "site": {
            "contentUrl": "",
        },
    }
    assert connection.request_headers == {
        "Content-Type": "application/json",
        "Accept": "application/json",
        "X-Tableau-Auth": "a1b2-c3d4",
    }
