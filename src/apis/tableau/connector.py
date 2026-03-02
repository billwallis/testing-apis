"""
Class to facilitate working with the Tableau Server REST API:

- https://help.tableau.com/current/api/rest_api/en-us/REST/rest_api_ref.htm
"""

import enum
import json

import requests

API_VERSION = "3.8"


class TableauAuthType(enum.StrEnum):
    PERSONAL_ACCESS_TOKEN = "pat"
    USERNAME_AND_PASSWORD = "uap"


def _parse_auth(auth_type: str) -> TableauAuthType:
    try:
        return TableauAuthType(auth_type.lower().strip())
    except ValueError as e:
        auth_types = [f"'{k.value}'" for k in TableauAuthType]
        raise ValueError(
            f"Auth type must be one of {', '.join(auth_types)}"
        ) from e


class TableauConnector:
    def __init__(
        self,
        domain: str,
        api_key: str,
        api_secret: str,
        auth_type: str = "uap",
    ) -> None:
        self.base_url = f"https://{domain}/api/{API_VERSION}/"
        self.api_key = api_key
        self.api_secret = api_secret
        self.auth_type = _parse_auth(auth_type)
        # self.auth_token = None

        creds = self.sign_in().json()["credentials"]
        self.auth_token = creds["token"]
        self.site_id = creds["site"]["id"]
        self.user_id = creds["user"]["id"]

    @property
    def credentials(self) -> dict:
        if self.auth_type == TableauAuthType.PERSONAL_ACCESS_TOKEN:
            key_name = "personalAccessTokenName"
            secret_name = "personalAccessTokenSecret"
        elif self.auth_type == TableauAuthType.USERNAME_AND_PASSWORD:
            key_name = "name"
            secret_name = "password"
        else:
            raise ValueError("Invalid auth type")

        return {
            key_name: self.api_key,
            secret_name: self.api_secret,
            "site": {
                "contentUrl": "",
            },
        }

    @property
    def request_headers(self) -> dict:
        """
        Default request headers.
        """
        headers = {
            "Content-Type": "application/json",
            "Accept": "application/json",
        }
        if t := getattr(self, "auth_token", None):
            headers["X-Tableau-Auth"] = t

        return headers

    ###
    # Authentication Methods
    ###
    def sign_in(self) -> requests.Response:
        """
        https://help.tableau.com/current/api/rest_api/en-us/REST/rest_api_ref_authentication.htm#sign_in
        """
        endpoint = "auth/signin"
        return requests.request(
            method="POST",
            url=self.base_url + endpoint,
            headers=self.request_headers,
            data=json.dumps({"credentials": self.credentials}),
        )

    def sign_out(self) -> requests.Response:
        """
        https://help.tableau.com/current/api/rest_api/en-us/REST/rest_api_ref_authentication.htm#sign_out
        """
        endpoint = "auth/signout"
        return requests.request(
            method="POST",
            url=self.base_url + endpoint,
            headers=self.request_headers,
        )

    ###
    # Users and Groups Methods
    ###
    def get_users_on_site(self) -> requests.Response:
        """
        https://help.tableau.com/current/api/rest_api/en-us/REST/rest_api_ref_users_and_groups.htm#get_users_on_site
        """
        endpoint = f"sites/{self.site_id}/users?fields=_all_&pageSize=1000"
        return requests.request(
            method="GET",
            url=self.base_url + endpoint,
            headers=self.request_headers,
        )

    def query_user_on_site(self, user_id: str) -> requests.Response:
        """
        https://help.tableau.com/current/api/rest_api/en-us/REST/rest_api_ref_users_and_groups.htm#query_user_on_site
        """
        endpoint = f"sites/{self.site_id}/users/{user_id}"
        return requests.request(
            method="GET",
            url=self.base_url + endpoint,
            headers=self.request_headers,
        )

    ###
    # Data Sources Methods
    ###
    def query_data_source_connections(
        self,
        datasource_id: str,
    ) -> requests.Response:
        """
        https://help.tableau.com/current/api/rest_api/en-us/REST/rest_api_ref_data_sources.htm#query_data_source_connections
        """
        endpoint = (
            f"sites/{self.site_id}/datasources/{datasource_id}/connections"
        )
        return requests.request(
            method="GET",
            url=self.base_url + endpoint,
            headers=self.request_headers,
        )

    def query_data_sources(self) -> requests.Response:
        """
        https://help.tableau.com/current/api/rest_api/en-us/REST/rest_api_ref_data_sources.htm#query_data_sources
        """
        endpoint = f"sites/{self.site_id}/datasources?pageSize=1000"
        return requests.request(
            method="GET",
            url=self.base_url + endpoint,
            headers=self.request_headers,
        )

    def update_data_source_connection(
        self,
        datasource_id: str,
        connection_id: str,
        new_password: str,
    ) -> requests.Response:
        """
        https://help.tableau.com/current/api/rest_api/en-us/REST/rest_api_ref_data_sources.htm#update_data_source_connection

        Only set up to change the password.
        """
        endpoint = f"sites/{self.site_id}/datasources/{datasource_id}/connections/{connection_id}"
        body = {
            "connection": {
                "password": new_password,
                "embedPassword": "True",
            }
        }
        return requests.request(
            method="PUT",
            url=self.base_url + endpoint,
            headers=self.request_headers,
            data=json.dumps(body),
        )

    def update_data_source_now(self, datasource_id: str) -> requests.Response:
        """
        https://help.tableau.com/current/api/rest_api/en-us/REST/rest_api_ref_data_sources.htm#update_data_source_now
        """
        endpoint = f"sites/{self.site_id}/datasources/{datasource_id}/refresh"
        return requests.request(
            method="POST",
            url=self.base_url + endpoint,
            headers=self.request_headers,
            data="{}",
        )

    def update_data_source(
        self,
        datasource_id: str,
        new_owner_id: str,
    ) -> requests.Response:
        """
        https://help.tableau.com/current/api/rest_api/en-us/REST/rest_api_ref_data_sources.htm#update_data_source

        Currently only set up to change the owner
        """
        endpoint = f"sites/{self.site_id}/datasources/{datasource_id}"
        body = {
            "datasource": {
                "owner": {
                    "id": new_owner_id,
                }
            }
        }
        return requests.request(
            method="PUT",
            url=self.base_url + endpoint,
            headers=self.request_headers,
            data=json.dumps(body),
        )

    ###
    # Workbooks and Views Methods
    ###
    def query_workbook_connections(self, workbook_id: str) -> requests.Response:
        """
        https://help.tableau.com/current/api/rest_api/en-us/REST/rest_api_ref_workbooks_and_views.htm#query_workbook_connections
        """
        endpoint = f"sites/{self.site_id}/workbooks/{workbook_id}/connections"
        return requests.request(
            method="GET",
            url=self.base_url + endpoint,
            headers=self.request_headers,
        )

    def query_workbooks_for_site(self) -> requests.Response:
        """
        https://help.tableau.com/current/api/rest_api/en-us/REST/rest_api_ref_workbooks_and_views.htm#query_workbooks_for_site
        """
        endpoint = f"sites/{self.site_id}/workbooks?pageSize=1000"
        return requests.request(
            method="GET",
            url=self.base_url + endpoint,
            headers=self.request_headers,
        )

    def query_workbooks_for_user(self, user_id: str) -> requests.Response:
        """
        https://help.tableau.com/current/api/rest_api/en-us/REST/rest_api_ref_workbooks_and_views.htm#query_workbooks_for_user
        """
        endpoint = f"sites/{self.site_id}/users/{user_id}/workbooks?ownedBy=true&pageSize=1000"
        return requests.request(
            method="GET",
            url=self.base_url + endpoint,
            headers=self.request_headers,
        )

    def update_workbook_connection(
        self,
        workbook_id: str,
        connection_id: str,
        new_password: str,
    ) -> requests.Response:
        """
        https://help.tableau.com/current/api/rest_api/en-us/REST/rest_api_ref_workbooks_and_views.htm#update_workbook_connection

        Only set up to change the password.
        """
        endpoint = f"sites/{self.site_id}/workbooks/{workbook_id}/connections/{connection_id}"
        body = {
            "connection": {
                "password": new_password,
                "embedPassword": "True",
            }
        }
        return requests.request(
            method="PUT",
            url=self.base_url + endpoint,
            headers=self.request_headers,
            data=json.dumps(body),
        )

    def update_workbook_now(self, workbook_id: str) -> requests.Response:
        """
        https://help.tableau.com/current/api/rest_api/en-us/REST/rest_api_ref_workbooks_and_views.htm#update_workbook_now
        """
        endpoint = f"sites/{self.site_id}/workbooks/{workbook_id}/refresh"
        return requests.request(
            method="POST",
            url=self.base_url + endpoint,
            headers=self.request_headers,
            data="{}",
        )

    def update_workbook(
        self,
        workbook_id: str,
        new_owner_id: str,
    ) -> requests.Response:
        """
        https://help.tableau.com/current/api/rest_api/en-us/REST/rest_api_ref_workbooks_and_views.htm#update_workbook

        Currently only set up to change the owner.
        """
        endpoint = f"sites/{self.site_id}/workbooks/{workbook_id}"
        body = {
            "workbook": {
                "owner": {
                    "id": new_owner_id,
                }
            }
        }
        return requests.request(
            method="PUT",
            url=self.base_url + endpoint,
            headers=self.request_headers,
            data=json.dumps(body),
        )
