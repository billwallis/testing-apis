"""
API clients for TfL.
"""

import requests

from src.apis.tfl import model

BASE_URL = "https://api.tfl.gov.uk/"


class TFLConnector:
    """
    Bridge class for the TfL REST API.
    """

    def __init__(self):
        self.base_url = BASE_URL

    @property
    def request_headers(self) -> dict:
        """
        Default request headers.
        """
        return {
            "Content-Type": "application/json",
            "Accept": "application/json",
        }

    def get_accident_stats(self, year: int) -> requests.Response:
        """
        https://api-portal.tfl.gov.uk/api-details#api=AccidentStats
        """
        endpoint = f"AccidentStats/{year}"
        return requests.request(
            method="GET",
            url=self.base_url + endpoint,
            headers=self.request_headers,
        )

    def get_air_quality(self) -> requests.Response:
        """
        https://api-portal.tfl.gov.uk/api-details#api=AirQuality
        """
        endpoint = "AirQuality"
        return requests.request(
            method="GET",
            url=self.base_url + endpoint,
            headers=self.request_headers,
        )

    def get_bike_points(
        self,
        bike_point_id: str | None = None,
        query: str | None = None,
    ) -> requests.Response:
        """
        https://api-portal.tfl.gov.uk/api-details#api=BikePoint
        """
        if bike_point_id and query:
            raise ValueError(
                "Only one of 'bike_point_id' or 'query' can be provided."
            )

        endpoint = "BikePoint"
        if bike_point_id:
            endpoint += f"/{bike_point_id}"
        if query:
            endpoint += f"/Search?query={query}"

        return requests.request(
            method="GET",
            url=self.base_url + endpoint,
            headers=self.request_headers,
        )

    def get_crowding(
        self,
        naptan: str,
        day_of_week: str | None = None,
    ) -> requests.Response:
        """
        https://api-portal.tfl.gov.uk/api-details#api=crowding

        For info about the NaPTAN codes, see:

        - https://github.com/ZackaryH8/tube-naptan
        """
        endpoint = f"crowding/{naptan}"
        if day_of_week:
            endpoint += f"/{day_of_week}"

        return requests.request(
            method="GET",
            url=self.base_url + endpoint,
            headers=self.request_headers,
        )

    def get_journey(
        self,
        meta: bool = False,
    ) -> requests.Response:
        """
        https://api-portal.tfl.gov.uk/api-details#api=Journey
        """
        endpoint = "Journey"
        if meta:
            endpoint += "/Meta/Modes"

        return requests.request(
            method="GET",
            url=self.base_url + endpoint,
            headers=self.request_headers,
        )

    def get_journey_plan(
        self,
        from_: str,
        to: str,
        search_params: model.JourneyPlannerSearchParams | None = None,
    ) -> requests.Response:
        """
        https://api-portal.tfl.gov.uk/api-details#api=Journey
        """
        endpoint = f"Journey/JourneyResults/{from_}/to/{to}"
        if search_params:
            endpoint += f"?{search_params.to_params()}"
        return requests.request(
            method="GET",
            url=self.base_url + endpoint,
            headers=self.request_headers,
        )

    def get_network_status(self) -> requests.Response:
        """
        https://api-portal.tfl.gov.uk/api-details#api=NetworkStatus
        """
        endpoint = "NetworkStatus"
        return requests.request(
            method="GET",
            url=self.base_url + endpoint,
            headers=self.request_headers,
        )
