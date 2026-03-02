"""
API clients for HashiCorp Vault.
"""

import json

import requests


class VaultConnector:
    """
    Bridge class for the HashiCorp Vault REST API.
    """

    def __init__(self, domain: str, api_key: str, api_secret: str) -> None:
        self.base_url = f"https://{domain}/v1/"
        self.api_key = api_key
        self.api_secret = api_secret
        self.auth_token = self.sign_in().json()["auth"]["client_token"]

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
            headers["X-Vault-Token"] = t

        return headers

    def sign_in(self) -> requests.Response:
        """
        https://www.vaultproject.io/api-docs/auth/ldap
        """
        endpoint = f"auth/ldap/login/{self.api_key}"
        body = {"password": self.api_secret}
        return requests.request(
            method="POST",
            url=self.base_url + endpoint,
            headers=self.request_headers,
            data=json.dumps(body),
        )

    def sign_in_userpass(self) -> requests.Response:
        """
        Sign in using LDAP rather than Username & Password.

        https://www.vaultproject.io/api-docs/auth/userpass
        """
        endpoint = f"auth/userpass/login/{self.api_key}"
        body = {"password": self.api_secret}
        return requests.request(
            method="POST",
            url=self.base_url + endpoint,
            headers=self.request_headers,
            data=json.dumps(body),
        )

    def list_roles(self) -> requests.Response:
        """
        https://www.vaultproject.io/api-docs/auth/ldap
        """
        endpoint = "database/roles"
        return requests.request(
            method="LIST",
            url=self.base_url + endpoint,
            headers=self.request_headers,
        )

    def list_secrets(self, secret_path: str) -> requests.Response:
        """
        https://www.vaultproject.io/api-docs/secret/kv/kv-v2#list-secrets
        """
        endpoint = f"secret/metadata/{secret_path}"
        return requests.request(
            method="LIST",
            url=self.base_url + endpoint,
            headers=self.request_headers,
        )

    def list_connections(self) -> requests.Response:
        """
        https://www.vaultproject.io/api/secret/databases#list-connections
        """
        endpoint = "database/config"
        return requests.request(
            method="LIST",
            url=self.base_url + endpoint,
            headers=self.request_headers,
        )

    def read_secret(self, role_name: str) -> requests.Response:
        endpoint = f"database/static-creds/{role_name}"
        return requests.request(
            method="POST",
            url=self.base_url + endpoint,
            headers=self.request_headers,
        )
