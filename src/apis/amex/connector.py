"""
API client for Amex.
"""

import datetime

import requests

BASE_URL = "https://global.americanexpress.com/api/servicing/v1/"


class AmexConnector:
    """
    Bridge class for the Amex REST API.

    Note that this is using the Amex website backend API, not the public API
    that you need to register for:

    - https://developer.americanexpress.com/
    """

    def __init__(self, account_key: str, cookie: str | None = None):
        self.base_url = BASE_URL
        self.account_key = account_key
        self.cookie = cookie

    @property
    def request_headers(self) -> dict:
        """
        Default request headers.

        These are the headers used by the Amex website; copying them makes it
        less likely that the request will be blocked by the server.
        """

        headers = {
            "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
            "accept-encoding": "gzip, deflate, br, zstd",
            "accept-language": "en-GB,en;q=0.9,es-ES;q=0.8,es;q=0.7,en-US;q=0.6",
            "cookie": self.cookie,
            "dnt": "1",
            "priority": "u=0, i",
            "referer": "https://global.americanexpress.com/activity/statements",
            "sec-ch-ua": '"Google Chrome";v="137", "Chromium";v="137", "Not/A)Brand";v="24"',
            "sec-ch-ua-mobile": "?0",
            "sec-ch-ua-platform": '"Windows"',
            "sec-fetch-dest": "document",
            "sec-fetch-mode": "navigate",
            "sec-fetch-site": "same-origin",
            "sec-fetch-user": "?1",
            "upgrade-insecure-requests": "1",
            "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/137.0.0.0 Safari/537.36",
        }

        return {k: v for k, v in headers.items() if v is not None}

    def get_cookie(self) -> None:
        # Log in to the Amex website and retrieve the cookie
        pass

    def get_statement(
        self,
        statement_end_date: datetime.date,
    ) -> requests.Response:
        """
        https://global.americanexpress.com/activity/statements
        """

        endpoint = "financials/documents"
        body = {
            "file_format": "csv",
            "limit": "all",
            "status": "posted",
            "statement_end_date": statement_end_date.isoformat(),
            "additional_fields": "true",
            "account_key": self.account_key,
            "client_id": "AmexAPI",
        }

        return requests.request(
            method="GET",
            url=self.base_url + endpoint,
            headers=self.request_headers,
            params=body,
        )
