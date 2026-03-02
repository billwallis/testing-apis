"""
Manual testing for the API clients.
"""

import os

import dotenv

from src import utils
from src.apis import jira

dotenv.load_dotenv()


def main() -> None:
    jira_connector = jira.JiraClient(
        domain=os.getenv("ATLASSIAN__DOMAIN"),
        api_key=os.getenv("ATLASSIAN__API_KEY"),
        api_secret=os.getenv("ATLASSIAN__API_SECRET"),
    )
    project_id = "10000"

    utils.pprint(jira_connector.get_projects_paginated().json())
    utils.pprint(jira_connector.get_issue(issue_key="DEV-67").json())
    utils.pprint(
        jira_connector.get_project_components(project_id=project_id).json()
    )
    # utils.pprint(
    #     jira_connector.create_issue(
    #         project_id=project_id,
    #         summary="A test from the API",
    #         description="Some basic description",
    #     ).json()
    # )


if __name__ == "__main__":
    main()
