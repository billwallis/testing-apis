from __future__ import annotations

import dataclasses
import uuid

import pytest
from alteryx_gallery import connector_alt

BASE_URL = "http://some.ip.address/api/"


class MockTime:
    @staticmethod
    def time() -> int:
        return 1637748738


class MockUUID:
    @staticmethod
    def uuid1() -> uuid.UUID:
        return uuid.UUID("0baecdf0-f808-11ef-98ca-00e04c244920")

    @staticmethod
    def uuid4() -> uuid.UUID:
        return uuid.UUID("dd4f2306-bf41-416b-8084-936da02e8dd4")


class MockClient:
    def __init__(self, client_key: str, client_secret: str) -> None:
        self.client_key = client_key
        self.client_secret = client_secret

    def sign(self, url: str):
        return [
            f"{self},{url}",
            {
                "Authorization": 'oauth_signature="4N06lp4cYi07HOB4k0kjd3xJLjo%3D"'
            },
        ]


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
def connection() -> connector_alt.GalleryConnector:
    creds = Credentials.default()
    return connector_alt.GalleryConnector(
        base_url=creds.base_url,
        api_key=creds.api_key,
        api_secret=creds.api_secret,
    )


def test__connector_properties_are_correct(
    monkeypatch: pytest.MonkeyPatch,
    connection: connector_alt.GalleryConnector,
):
    monkeypatch.setattr(connector_alt, "time", MockTime)
    monkeypatch.setattr(connector_alt, "uuid", MockUUID)
    monkeypatch.setattr(connector_alt, "Client", MockClient)

    assert connection.base_url == BASE_URL
    assert connection.request_headers == {
        "Content-Type": "application/json",
        "Accept": "application/json",
        "Authorization": "OAuth "
        + ",".join(
            [
                'oauth_timestamp="1637748738"',
                'oauth_signature_method="HMAC-SHA1"',
                'oauth_consumer_key="some-key"',
                'oauth_version="1.0"',
                'oauth_nonce="dd4f2306bf41416b8084936da02e8dd40baecdf0f80811ef98ca00e04c244920"',
                'oauth_signature="4N06lp4cYi07HOB4k0kjd3xJLjo%3D"',
            ]
        ),
    }
