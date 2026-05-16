"""
Manual testing for the API clients.
"""

import os
import pathlib

import dotenv
import utils

import jira

dotenv.load_dotenv()

HERE = pathlib.Path(__file__).parent
QUERIES = HERE / "queries"


def _get_query(query_name: str) -> str:
    return (QUERIES / "query_name").read_text()


def _test_rest_requests(jira_client: jira.JiraClient) -> None:
    project_id = "10000"

    utils.pprint(jira_client.get_projects_paginated().json())
    utils.pprint(jira_client.get_issue(issue_key="DEV-67").json())
    utils.pprint(
        jira_client.get_project_components(project_id=project_id).json()
    )
    # utils.pprint(
    #     jira_client.create_issue(
    #         project_id=project_id,
    #         summary="A test from the API",
    #         description="Some basic description",
    #     ).json()
    # )


def _test_graphql_queries(jira_client: jira.JiraClient) -> None:
    # Get self
    utils.pprint(
        jira_client.graphql(query=_get_query("me.graphql")).json()["data"]
    )

    # Get tenant details
    jira_tenant = jira_client.graphql(
        query=_get_query("tenant.graphql"),
        variables={"host": f"{jira_client.domain}.atlassian.net"},
    ).json()["data"]
    utils.pprint(jira_tenant)

    # Get projects
    cloud_id = jira_tenant["tenantContexts"][0]["cloudId"]
    utils.pprint(
        jira_client.graphql(
            query=_get_query("projects.graphql"),
            variables={"cloudId": cloud_id},
        ).json()
    )


def main() -> None:
    jira_client = jira.JiraClient(
        domain=os.environ["ATLASSIAN__DOMAIN"],
        api_key=os.environ["ATLASSIAN__API_KEY"],
        api_secret=os.environ["ATLASSIAN__API_SECRET"],
    )
    _test_rest_requests(jira_client)
    _test_graphql_queries(jira_client)


if __name__ == "__main__":
    main()
