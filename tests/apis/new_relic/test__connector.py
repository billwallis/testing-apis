import http
import textwrap

import pytest
import requests
from requests.exceptions import RequestException

from src.apis.new_relic import connector


class MockResponse:
    def __init__(self, data: dict, code: int) -> None:
        self.data = data
        self.code = code

    def json(self):
        return self.data

    def raise_for_status(self):
        if not (200 <= self.code < 300):
            raise RequestException("I'm a doctor, Jim, not a server!")


@pytest.fixture
def connection() -> connector.NewRelicConnector:
    return connector.NewRelicConnector(
        account_id="123456789",
        api_key="NRAK-A1B2C3D4",
    )


def test__connector_properties_are_correct(
    connection: connector.NewRelicConnector,
):
    assert connection.base_url == "https://api.newrelic.com/graphql/"
    assert connection.request_headers == {
        "Content-Type": "application/json",
        "Accept": "application/json",
        "API-Key": "NRAK-A1B2C3D4",
    }


def test__queries_are_constructed_correctly(
    monkeypatch: pytest.MonkeyPatch,
    connection: connector.NewRelicConnector,
):
    def mock_get(
        url: str, headers: dict, params: dict, timeout: int
    ) -> MockResponse:
        assert url == "https://api.newrelic.com/graphql/"
        assert timeout == 10
        assert headers == {
            "Content-Type": "application/json",
            "Accept": "application/json",
            "API-Key": "NRAK-A1B2C3D4",
        }
        assert params == {
            "query": textwrap.dedent(
                """\
                {
                  actor {
                    account(id: 123456789) {
                      nrql(query: "some query with a new line   and some spaces") {
                        results
                      }
                    }
                  }
                }
                """
            )
        }

        return MockResponse({}, http.HTTPStatus.OK)

    monkeypatch.setattr(requests, "get", mock_get)
    connection.query("some query\nwith a new line\n  and some spaces")


def test__query_results_are_returned_correctly(
    monkeypatch: pytest.MonkeyPatch,
    connection: connector.NewRelicConnector,
):
    query = """from SomeTable select count(*)"""
    results = [{"count", 123}]
    response = {"data": {"actor": {"account": {"nrql": {"results": results}}}}}

    monkeypatch.setattr(
        requests,
        "get",
        lambda *args, **kwargs: MockResponse(response, http.HTTPStatus.OK),
    )

    assert connection.query(query) == results


def test__bad_queries_raise_an_exception(
    monkeypatch: pytest.MonkeyPatch,
    connection: connector.NewRelicConnector,
):
    monkeypatch.setattr(
        requests,
        "get",
        lambda *args, **kwargs: MockResponse({}, http.HTTPStatus.BAD_REQUEST),
    )

    with pytest.raises(RequestException):
        connection.query("something bad")
