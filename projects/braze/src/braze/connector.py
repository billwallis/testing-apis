"""
API clients for Braze.
"""

import enum
import json

import requests


class Brand(enum.StrEnum):
    TEST = enum.auto()
    JAJA = enum.auto()
    BOI = enum.auto()
    AA = enum.auto()


def _parse_brand(brand: str) -> Brand:
    try:
        return Brand(brand.lower().strip())
    except ValueError as e:
        brands = [f"'{k.value}'" for k in Brand]
        raise ValueError(f"Brand must be one of {', '.join(brands)}") from e


class BrazeConnector:
    """
    Bridge class for the Braze REST API.
    """

    def __init__(self, base_url: str, brand: str, api_key: str) -> None:
        self.base_url = base_url
        self.brand = _parse_brand(brand)
        self.api_key = api_key

    @property
    def request_headers(self) -> dict:
        """
        Default request headers.
        """

        return {
            "Content-Type": "application/json",
            "Accept": "application/json",
            "Authorization": f"Bearer {self.api_key}",
        }

    def get_campaigns_list(self, page: int = 0) -> requests.Response:
        """
        https://www.braze.com/docs/api/endpoints/export/campaigns/get_campaigns/
        """

        endpoint = f"campaigns/list?page={page}"
        return requests.request(
            method="GET",
            url=self.base_url + endpoint,
            headers=self.request_headers,
        )

    def user_profile_export_by_identifier(
        self,
        body: dict,
    ) -> requests.Response:
        """
        https://www.braze.com/docs/api/endpoints/export/user_data/post_users_identifier/
        """

        endpoint = "users/export/ids"
        return requests.request(
            method="POST",
            url=self.base_url + endpoint,
            headers=self.request_headers,
            data=json.dumps(body),
        )

    def user_profile_export_by_segment(
        self,
        segment_id: str,
    ) -> requests.Response:
        """
        https://www.braze.com/docs/api/endpoints/export/user_data/post_users_segment/
        """

        endpoint = "users/export/segment"
        body = {
            "segment_id": segment_id,
            "fields_to_export": [
                "external_id",
                "braze_id",
                "campaigns_received",
                "custom_attributes",
                "custom_events",
            ],
        }
        return requests.request(
            method="POST",
            url=self.base_url + endpoint,
            headers=self.request_headers,
            data=json.dumps(body),
        )
