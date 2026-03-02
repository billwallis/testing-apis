"""
API clients for Notion.
"""

import requests

DEFAULT_NOTION_VERSION = "2022-06-28"


class NotionConnector:
    """
    Bridge class for the Notion REST API.
    """

    def __init__(
        self, api_token: str, version: str = DEFAULT_NOTION_VERSION
    ) -> None:
        """
        Create the connector.
        """
        self.base_url = "https://api.notion.com/v1/"
        self.notion_version = version
        self.api_token = api_token

    @property
    def auth_basic(self) -> str:
        """
        Encode the key and secret following the Notion documentation:

        - https://developers.notion.com/reference/authentication
        """
        return f"Bearer {self.api_token}"

    @property
    def request_headers(self) -> dict:
        """
        Default request headers.
        """
        return {
            "Content-Type": "application/json",
            "Accept": "application/json",
            "Notion-Version": self.notion_version,
            "Authorization": self.auth_basic,
        }

    def get_users(self) -> requests.Response:
        """
        https://developers.notion.com/reference/get-users
        """
        endpoint = "users"
        return requests.request(
            method="GET",
            url=self.base_url + endpoint,
            headers=self.request_headers,
        )
