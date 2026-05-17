from __future__ import annotations

import dataclasses

import pytest
from braze import connector

BASE_URL = "https://rest.region.braze.eu/"


@dataclasses.dataclass
class Credentials:
    base_url: str
    brand: str
    api_key: str

    @classmethod
    def default(cls) -> Credentials:
        return cls(
            base_url=BASE_URL,
            brand="test",
            api_key="a1b2-c3d4",
        )


@pytest.fixture
def connection() -> connector.BrazeConnector:
    creds = Credentials.default()
    return connector.BrazeConnector(
        base_url=creds.base_url,
        brand=creds.brand,
        api_key=creds.api_key,
    )


def test__invalid_brands_raise_an_error():
    with pytest.raises(ValueError):
        connector.BrazeConnector(
            base_url="",
            api_key="",
            brand="bad-brand",
        )


def test__connector_properties_are_correct(
    connection: connector.BrazeConnector,
):
    assert connection.base_url == BASE_URL
    assert connection.request_headers == {
        "Content-Type": "application/json",
        "Accept": "application/json",
        "Authorization": "Bearer a1b2-c3d4",
    }
