import requests
import utils


class TwilioConnector:
    """
    Bridge class for the Twilio REST API.
    """

    def __init__(self, workspace: str, api_key: str, api_secret: str) -> None:
        self.base_url = (
            f"https://taskrouter.twilio.com/v1/Workspaces/{workspace}/"
        )
        self.auth = (api_key, api_secret)

    @property
    def request_headers(self) -> dict:
        """
        Default request headers.
        """

        return {
            "Content-Type": "application/json",
            "Accept": "application/json",
        }

    def list_all_events(
        self,
        start_datetime: str,
        end_datetime: str,
    ) -> requests.Response:
        """
        https://www.twilio.com/docs/taskrouter/api/event#list-all-events

        Dates must be a string in the ISO-8601 format, e.g. 2020-01-01T00:00:00Z
        """

        params = {
            "StartDate": start_datetime,
            "EndDate": end_datetime,
            "PageSize": 100,
        }
        endpoint = "Events?" + utils.to_param_string(params)
        return requests.request(
            method="GET",
            auth=self.auth,
            url=self.base_url + endpoint,
            headers=self.request_headers,
        )
