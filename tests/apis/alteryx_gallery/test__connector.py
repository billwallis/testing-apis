from __future__ import annotations

import dataclasses

import pytest

from src.apis.alteryx_gallery import connector

BASE_URL = "http://some.ip.address/api/"


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
def connection() -> connector.GalleryConnector:
    creds = Credentials.default()
    return connector.GalleryConnector(
        base_url=creds.base_url,
        api_key=creds.api_key,
        api_secret=creds.api_secret,
    )


def test__connector_properties_are_correct(
    connection: connector.GalleryConnector,
):
    assert connection.base_url == BASE_URL
    assert connection.request_headers == {
        "Content-Type": "application/json",
        "Accept": "application/json",
    }
