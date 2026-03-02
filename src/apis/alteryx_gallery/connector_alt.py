"""
Alternative API clients for Alteryx Gallery.
"""

import math
import re
import time
import uuid

import requests
from oauthlib.oauth1 import Client


class GalleryConnector:
    """
    Bridge class for the Alteryx Gallery REST API.
    """

    def __init__(self, base_url: str, api_key: str, api_secret: str) -> None:
        self.base_url = base_url
        self._api_key = api_key
        self._api_secret = api_secret

    @property
    def oauth_timestamp(self) -> str:
        """Example: 1637748738"""
        return str(math.floor(time.time()))

    @property
    def oauth_signature_method(self) -> str:
        return "HMAC-SHA1"

    @property
    def oauth_consumer_key(self) -> str:
        return self._api_key

    @property
    def oauth_version(self) -> str:
        """Optional"""
        return "1.0"

    @property
    def oauth_nonce(self) -> str:
        """
        Example: GeZ1v

        Just a random string that will be used only once. For more info, see:

        - https://stackoverflow.com/a/40328464/8213085
        """
        return uuid.uuid4().hex + uuid.uuid1().hex

    @property
    def oauth_signature(self) -> str:
        """
        Example: 6PT9ZnqXRfLCwp37NrFbVzRUZHg%3D

        Use oauthlib.oauth1 to get the oauth_signature in the response header,
        then parse out the oauth_signature value. This uses ``HMAC-SHA1`` by
        default.
        """
        client = Client(
            client_key=self._api_key,
            client_secret=self._api_secret,
        )
        return re.search(
            'oauth_signature="(.*)"',
            client.sign(self.base_url)[1]["Authorization"],
        )[1]

    @property
    def oauth_params(self) -> dict:
        return {
            "oauth_timestamp": self.oauth_timestamp,
            "oauth_signature_method": self.oauth_signature_method,
            "oauth_consumer_key": self.oauth_consumer_key,
            "oauth_version": self.oauth_version,
            "oauth_nonce": self.oauth_nonce,
            "oauth_signature": self.oauth_signature,
        }

    @property
    def request_headers(self) -> dict:
        """
        Default request headers.
        """
        return {
            "Content-Type": "application/json",
            "Accept": "application/json",
            "Authorization": (
                "OAuth "
                + ",".join([f'{k}="{v}"' for k, v in self.oauth_params.items()])
            ),
        }

    def get_credentials(self) -> requests.Response:
        endpoint = "user/v2/credentials"
        return requests.request(
            method="GET",
            url=self.base_url + endpoint,
            headers=self.request_headers,
        )
