"""
API clients for Metabase.

Note that:

- the ``api_key`` should be your username for your Metabase account
- the ``api_secret`` should be your password for your Metabase account
"""

import json

import requests


class MetabaseConnector:
    """
    Bridge class for the Metabase REST API.
    """

    def __init__(self, base_url: str, api_key: str, api_secret: str) -> None:
        """
        Create the connector.
        """

        self.base_url = base_url
        self.__api_key = api_key
        self.__api_secret = api_secret
        self.__auth_token = None

        sign_in_response = self.sign_in()
        self.__auth_token = sign_in_response.json()["id"]

    @property
    def auth_token(self) -> str:
        return self.__auth_token

    @property
    def request_headers(self) -> dict:
        """
        Default request headers.
        """

        headers = {
            "Content-Type": "application/json",
            "Accept": "application/json",
        }
        if self.auth_token:
            headers["X-Metabase-Session"] = self.auth_token

        return headers

    ###
    # Authentication Methods
    ###
    def sign_in(self) -> requests.Response:
        """
        https://www.metabase.com/docs/latest/api-documentation.html#post-apisession
        """

        endpoint = "session"
        body = {
            "username": self.__api_key,
            "password": self.__api_secret,
        }
        return requests.request(
            method="POST",
            url=self.base_url + endpoint,
            headers=self.request_headers,
            data=json.dumps(body),
        )

    def sign_out(self) -> requests.Response:
        """
        https://www.metabase.com/docs/latest/api-documentation.html#delete-apisession
        """

        endpoint = "session"
        return requests.request(
            method="DELETE",
            url=self.base_url + endpoint,
            headers=self.request_headers,
        )

    ###
    # Database Methods
    ###
    def get_databases(self) -> requests.Response:
        """
        https://www.metabase.com/docs/v0.41/api-documentation.html#get-apidatabase
        """

        endpoint = "database"
        return requests.request(
            method="GET",
            url=self.base_url + endpoint,
            headers=self.request_headers,
        )

    def get_database_by_id(self, database_id: int | str) -> requests.Response:
        """
        https://www.metabase.com/docs/v0.41/api-documentation.html#get-apidatabaseid
        """

        endpoint = f"database/{database_id}"
        return requests.request(
            method="GET",
            url=self.base_url + endpoint,
            headers=self.request_headers,
        )

    ###
    # User Methods
    ###
    def get_user_current(self) -> requests.Response:
        """
        https://www.metabase.com/docs/latest/api-documentation.html#get-apiusercurrent
        """

        endpoint = "user/current"
        return requests.request(
            method="GET",
            url=self.base_url + endpoint,
            headers=self.request_headers,
        )
