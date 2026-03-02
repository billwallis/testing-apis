"""
API clients for Jira.

Note that:

- the ``api_key`` should be your email address for your Atlassian account
- the ``api_secret`` should be a token that you generate for your Atlassian account

See the following documentation:

- https://id.atlassian.com/manage-profile/security/api-tokens
"""

import base64
import json

import requests


class JiraClient:
    """
    Bridge class for the Jira API.
    """

    domain: str
    base_url: str

    def __init__(self, domain: str, api_key: str, api_secret: str) -> None:
        self.domain = domain
        self.base_url = f"https://{domain}.atlassian.net/"
        self._api_key = api_key
        self._api_secret = api_secret

    @property
    def auth_basic(self) -> str:
        """
        Encode the key and secret following the Atlassian documentation:

        - https://developer.atlassian.com/cloud/jira/platform/basic-auth-for-rest-apis/#supply-basic-auth-headers
        """
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

    def graphql(
        self, query: str, variables: dict | None = None
    ) -> requests.Response:
        """
        https://developer.atlassian.com/platform/atlassian-graphql-api/graphql/#overview
        """

        endpoint = "gateway/api/graphql"
        return requests.post(
            url=self.base_url + endpoint,
            headers=self.request_headers,
            data=json.dumps(
                {
                    "query": query,
                    "variables": {} if variables is None else variables,
                },
            ),
        )

    def get_projects_paginated(self) -> requests.Response:
        """
        https://developer.atlassian.com/cloud/jira/platform/rest/v3/api-group-projects/#api-rest-api-3-project-search-get
        """
        endpoint = "rest/api/3/project/search"
        return requests.request(
            method="GET",
            url=self.base_url + endpoint,
            headers=self.request_headers,
            params={"maxResults": 50},
        )

    def get_issue(self, issue_key: str) -> requests.Response:
        """
        https://developer.atlassian.com/cloud/jira/platform/rest/v3/api-group-issues/#api-rest-api-3-issue-issueidorkey-get
        """
        endpoint = f"rest/api/3/issue/{issue_key}"
        return requests.request(
            method="GET",
            url=self.base_url + endpoint,
            headers=self.request_headers,
            data={},
        )

    def get_project_components(self, project_id: str) -> requests.Response:
        """
        https://developer.atlassian.com/cloud/jira/platform/rest/v3/api-group-project-components/#api-rest-api-3-project-projectidorkey-components-get
        """
        endpoint = f"rest/api/3/project/{project_id}/components"
        return requests.request(
            method="GET",
            url=self.base_url + endpoint,
            headers=self.request_headers,
            data={},
        )

    def create_issue(
        self,
        project_id: str,
        summary: str,
        description: str,
    ) -> requests.Response:
        """
        https://developer.atlassian.com/cloud/jira/platform/rest/v3/api-group-issues/#api-rest-api-3-issue-post

        For help with Jira IDs, either use the corresponding GET method, or see:

        - https://jaja.atlassian.net/wiki/spaces/AO/pages/2441904132/Jira+API+Guide
        """
        endpoint = "rest/api/3/issue"
        payload = json.dumps(
            {
                "update": {},
                "fields": {
                    "summary": summary,
                    "issuetype": {
                        "id": "10001"  # Task
                    },
                    # "components": [
                    #     {
                    #         "id": "10114"  # Analytics
                    #     }
                    # ],
                    "project": {"id": project_id},
                    "description": {
                        "type": "doc",
                        "version": 1,
                        "content": [
                            {
                                "type": "paragraph",
                                "content": [
                                    {"text": description, "type": "text"}
                                ],
                            }
                        ],
                    },
                    # "priority": {
                    #     "id": "3"  # P3 - Medium
                    # },
                    "labels": [],
                    "duedate": None,  # eg "2022-01-01"
                    # "assignee": {
                    #     "id": None  # Unassigned
                    # },
                },
            }
        )
        return requests.request(
            method="POST",
            url=self.base_url + endpoint,
            headers=self.request_headers,
            data=payload,
        )
