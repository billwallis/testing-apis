from types import SimpleNamespace

import pytest
from companies_house import connector


@pytest.fixture
def connection(
    monkeypatch: pytest.MonkeyPatch,
) -> connector.CompaniesHouseConnector:
    return connector.CompaniesHouseConnector(api_key="a1b2-c3d4")


def test__connector_properties_are_correct(
    connection: connector.CompaniesHouseConnector,
):
    assert connection.base_url == connector.BASE_URL
    assert connection.request_headers == {
        "Content-Type": "application/json",
        "Accept": "application/json",
        "Authorization": "Basic YTFiMi1jM2Q0Og==",
    }


def test__search_parameters_are_built_correctly(
    monkeypatch: pytest.MonkeyPatch,
    connection: connector.CompaniesHouseConnector,
):
    request_data = {}

    def mock_request(method: str, url: str, headers: dict) -> None:
        request_data["method"] = method
        request_data["url"] = url
        request_data["headers"] = headers

    monkeypatch.setattr(
        connector, "requests", SimpleNamespace(request=mock_request)
    )
    connection.search(q="Company Name", items_per_page=10)

    assert request_data["method"] == "GET"
    assert (
        request_data["url"]
        == connector.BASE_URL + "search?q=Company Name&items_per_page=10&"
    )
