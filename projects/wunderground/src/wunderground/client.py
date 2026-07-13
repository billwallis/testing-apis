"""
API client for Wunderground.

- https://www.wunderground.com/
"""

import datetime
from typing import Literal

import requests

BASE_URL = "https://api.weather.com/v2/pws/"
DEFAULT_TIMEOUT_SECONDS = 10

type UnitType = Literal[
    "e",  # Imperial
    "m",  # Metric
]
type ObservationDayRange = Literal["1day", "3day"]
type SummaryDayRange = Literal["1day", "3day", "7day"]


class WundergroundConnector:
    """
    Bridge class for the Wunderground REST API (not publicly documented).
    """

    base_url: str
    api_key: str

    def __init__(self, api_key: str) -> None:
        self.base_url = BASE_URL
        self.api_key = api_key

    @property
    def request_headers(self) -> dict:
        """
        Default request headers.

        These mimic a browser request, making the request less likely to be
        blocked.
        """

        return {
            "Accept": "application/json, text/plain, */*",
            "Accept-Encoding": "gzip, deflate, br, zstd",
            "Accept-Language": "en-GB,en;q=0.9,es-ES;q=0.8,es;q=0.7,en-US;q=0.6",
            "Dnt": "1",
            "Origin": "https://www.wunderground.com",
            "Priority": "u=1, i",
            "Referer": "https://www.wunderground.com/",
            "Sec-Sh-Ua": '"Chromium";v="134", "Not:A-Brand";v="24", "Google Chrome";v="134"',
            "Sec-Sh-Ua-Mobile": "?0",
            "Sec-Sh-Ua-Platform": '"Windows"',
            "Sec-Fetch-Dest": "empty",
            "Sec-Fetch-Mode": "cors",
            "Sec-Fetch-Site": "cross-site",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/134.0.0.0 Safari/537.36",
        }

    def _get_current_observation(
        self,
        station_id: str,
        units: UnitType,
    ) -> requests.Response:
        """
        Return the latest weather data observation for a specific station.
        """

        endpoint = "observations/current"
        params = {
            "apiKey": self.api_key,
            "stationId": station_id,
            "numericPrecision": "decimal",
            "format": "json",
            "units": units,
        }

        return requests.request(
            method="GET",
            url=self.base_url + endpoint,
            headers=self.request_headers,
            params=params,
            timeout=DEFAULT_TIMEOUT_SECONDS,
        )

    def _get_observation_history(
        self,
        station_id: str,
        date: datetime.date,
        units: UnitType,
    ) -> requests.Response:
        """
        Return historical weather data observations for a specific station and
        date.
        """

        endpoint = "history/all"
        params = {
            "apiKey": self.api_key,
            "stationId": station_id,
            "date": date.strftime("%Y%m%d"),
            "numericPrecision": "decimal",
            "format": "json",
            "units": units,
        }

        return requests.request(
            method="GET",
            url=self.base_url + endpoint,
            headers=self.request_headers,
            params=params,
            timeout=DEFAULT_TIMEOUT_SECONDS,
        )

    def _get_recent_observations(
        self,
        station_id: str,
        days: ObservationDayRange,
        units: UnitType,
    ) -> requests.Response:
        """
        Return recent weather data observations for a specific station.
        """

        endpoint = f"observations/all/{days}"
        params = {
            "apiKey": self.api_key,
            "stationId": station_id,
            "numericPrecision": "decimal",
            "format": "json",
            "units": units,
        }

        return requests.request(
            method="GET",
            url=self.base_url + endpoint,
            headers=self.request_headers,
            params=params,
            timeout=DEFAULT_TIMEOUT_SECONDS,
        )

    def get_observations(
        self,
        station_id: str,
        date: datetime.date,
        units: UnitType = "m",
    ) -> list[dict]:
        """
        Return weather data observations for a specific station and date.

        The response contains a list of observations for the specified station
        and date. There are several observations per day.
        """

        if date < datetime.date.today() - datetime.timedelta(days=31):
            raise ValueError("Date must be within the last 31 days")

        # if the date is within the last 3 days, use the observations endpoint;
        # otherwise, use the history endpoint
        if date < datetime.date.today() - datetime.timedelta(days=3):
            observations = self._get_observation_history(
                station_id=station_id,
                date=date,
                units=units,
            )
            return observations.json().get("observations", [])

        observations = self._get_recent_observations(
            station_id=station_id,
            days="3day",
            units=units,
        )
        return [
            obs
            for obs in observations.json().get("observations", [])
            if obs["obsTimeLocal"].startswith(date.isoformat())
        ]

    def _get_recent_summaries(
        self,
        station_id: str,
        days: SummaryDayRange,
        units: UnitType,
    ) -> requests.Response:
        """
        Return recent weather data summaries for a specific station.
        """

        endpoint = f"dailysummary/{days}"
        params = {
            "apiKey": self.api_key,
            "stationId": station_id,
            "numericPrecision": "decimal",
            "format": "json",
            "units": units,
        }

        return requests.request(
            method="GET",
            url=self.base_url + endpoint,
            headers=self.request_headers,
            params=params,
            timeout=DEFAULT_TIMEOUT_SECONDS,
        )

    def _get_summary_history(
        self,
        station_id: str,
        start_date: datetime.date,
        end_date: datetime.date,
        units: UnitType,
    ) -> requests.Response:
        """
        Return historical weather data summaries for a specific station and date
        range.
        """

        endpoint = "history/daily"
        params = {
            "apiKey": self.api_key,
            "stationId": station_id,
            "startDate": start_date.strftime("%Y%m%d"),
            "endDate": end_date.strftime("%Y%m%d"),
            "numericPrecision": "decimal",
            "format": "json",
            "units": units,
        }

        return requests.request(
            method="GET",
            url=self.base_url + endpoint,
            headers=self.request_headers,
            params=params,
            timeout=DEFAULT_TIMEOUT_SECONDS,
        )

    def get_summaries(
        self,
        station_id: str,
        start_date: datetime.date,
        end_date: datetime.date,
        units: UnitType = "m",
    ) -> list[dict]:
        """
        Return weather data summaries for a specific station and date range.

        The response contains a daily summary of the weather data for the
        specified station and days. There is one summary per day.
        """

        if start_date > end_date:
            raise ValueError("Start date must be before end date")
        if start_date < datetime.date.today() - datetime.timedelta(days=31):
            raise ValueError("Start date must be within the last 31 days")

        # as far as I've seen, we can always use the history endpoint for
        # summaries
        observations = self._get_summary_history(
            station_id=station_id,
            start_date=start_date,
            end_date=end_date,
            units=units,
        )
        return observations.json().get("observations", [])
