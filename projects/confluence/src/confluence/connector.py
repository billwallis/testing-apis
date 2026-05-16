"""
API clients for Confluence.

Note that:

- the ``api_key`` should be your email address for your Atlassian account
- the ``api_secret`` should be a token that you generate for your Atlassian account

See the following documentation:

- https://id.atlassian.com/manage-profile/security/api-tokens
"""

import base64

import requests


class ConfluenceConnector:
    """
    Bridge class for the Confluence REST API.
    """

    def __init__(self, domain: str, api_key: str, api_secret: str) -> None:
        self.base_url = f"https://{domain}.atlassian.net/wiki/rest/api/"
        self._api_key = api_key
        self._api_secret = api_secret

    @property
    def auth_basic(self) -> str:
        """
        Encode the key and secret following the Atlassian documentation:

        - https://developer.atlassian.com/cloud/jira/platform/basic-auth-for-rest-apis/#supply-basic-auth-headers
        """

        # TODO: Consider using requests.auth.HTTPBasicAuth() instead
        return (
            "Basic "
            + base64.b64encode(
                f"{self._api_key}:{self._api_secret}".encode()
            ).decode()
        )

    @property
    def request_headers(self) -> dict:
        """
        Default request headers.
        """

        return {
            "Content-Type": "application/json",
            "Accept": "application/json",
            "Authorization": self.auth_basic,
        }

    def get_spaces(self) -> requests.Response:
        """
        https://developer.atlassian.com/cloud/confluence/rest/api-group-space/#api-wiki-rest-api-space-get
        """

        endpoint = "space"
        return requests.request(
            method="GET",
            url=self.base_url + endpoint,
            headers=self.request_headers,
        )

    def search_content_by_cql(self, cql: str) -> requests.Response:
        """
        https://developer.atlassian.com/cloud/confluence/rest/api-group-content/#api-wiki-rest-api-content-search-get
        """

        endpoint = f"content/search?cql={cql}"
        return requests.request(
            method="GET",
            url=self.base_url + endpoint,
            headers=self.request_headers,
        )
