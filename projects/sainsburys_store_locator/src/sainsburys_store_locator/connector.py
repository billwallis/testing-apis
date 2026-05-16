import requests
import utils

BASE_URL = "https://api.stores.sainsburys.co.uk/v1/"


class StoreLocatorConnector:
    """
    Bridge class for the Sainsbury's Store Locator API.
    """

    def __init__(self) -> None:
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

    def get_stores(self, params: dict | None = None) -> requests.Response:
        """
        https://app.swaggerhub.com/apis-docs/JSainsburys/Storelocater_API_PROD/1.0.0#/stores/getStores
        """

        endpoint = "stores"
        if params:
            endpoint += utils.to_param_string(params)
        return requests.request(
            method="GET",
            url=self.base_url + endpoint,
            headers=self.request_headers,
        )

    def get_store_by_id(self, store_id: int) -> requests.Response:
        """
        https://app.swaggerhub.com/apis-docs/JSainsburys/Storelocater_API_PROD/1.0.0#/stores/getStore
        """

        endpoint = f"stores/{store_id}"
        return requests.request(
            method="GET",
            url=self.base_url + endpoint,
            headers=self.request_headers,
        )
