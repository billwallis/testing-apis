"""
API clients for New Relic.
"""

import pathlib
from typing import Any

import requests

HERE = pathlib.Path(__file__).parent
BASE_URL = "https://api.newrelic.com/graphql/"
REQUEST_TIMEOUT_SECONDS = 10
NRQL_WRAPPER = (HERE / "nrql-wrapper.graphql").read_text(encoding="utf-8")


class NewRelicConnector:
    """
    Bridge class for the New Relic NerdGraph (GraphQL) API.
    """

    def __init__(self, account_id: str, api_key: str) -> None:
        self.base_url = BASE_URL
        self.account_id = account_id
        self.api_key = api_key

    @property
    def request_headers(self) -> dict:
        """
        Default request headers.
        """
        return {
            "Content-Type": "application/json",
            "Accept": "application/json",
            "API-Key": self.api_key,
        }

    def query(self, query: str) -> list[dict]:
        """
        Execute a NRQL query and return the result.
        """

        # fmt: off
        query_ = (
            NRQL_WRAPPER
                .replace("{{account_id}}", self.account_id)
                .replace("{{query}}", query.replace("\n", " ").strip())
        )
        # fmt: on

        return _get_and_unpack(
            url=self.base_url,
            headers=self.request_headers,
            params={"query": query_},
        )


def _get_and_unpack(
    url: str,
    headers: dict | None = None,
    params: dict | None = None,
) -> list[dict]:
    if response := get(url, headers, params):
        return response["data"]["actor"]["account"]["nrql"]["results"]
    return []


def get(
    url: str,
    headers: dict | None = None,
    params: dict | None = None,
) -> Any:
    """
    Perform a GET request and return the JSON response.
    """

    response = requests.get(
        url=url,
        headers=headers,
        params=params,
        timeout=REQUEST_TIMEOUT_SECONDS,
    )
    response.raise_for_status()

    return response.json()
