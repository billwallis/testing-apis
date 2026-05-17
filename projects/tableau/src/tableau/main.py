"""
Manual testing/running of the API clients.
"""

import os

import dotenv
import utils

import tableau

dotenv.load_dotenv()


def change_objects_owner(tableau_connector: tableau.TableauConnector) -> None:
    """
    Change the owners of objects in Tableau.
    """

    someone_id = "c8294636-5960-45f8-bc0a-1758f202eac6"
    someone_else_id = "92c5b714-6c29-43db-a34c-a97d18919cc8"

    # Change datasources owner
    # utils.pprint(tableau_connector.query_data_sources().text)
    resp = tableau_connector.query_data_sources().json()
    for datasource in resp["datasources"]["datasource"]:
        if datasource["owner"]["id"] == someone_id:
            # utils.pprint(data_source)
            utils.pprint(
                tableau_connector.update_data_source(
                    datasource_id=datasource["id"],
                    new_owner_id=someone_else_id,
                ).text
            )

    # Change workbooks owner
    resp = tableau_connector.query_workbooks_for_user(someone_id).json()
    for workbook in resp["workbooks"]["workbook"]:
        utils.pprint(
            tableau_connector.update_workbook(
                workbook_id=workbook["id"],
                new_owner_id=someone_else_id,
            ).json()
        )


def change_connection_passwords(
    tableau_connector: tableau.TableauConnector,
) -> None:
    """
    Change the password of database connections in Tableau.
    """

    new_password = "A1a-pB7F7jiP596ngMgj"  # noqa: S105

    # fmt: off
    datasources = tableau_connector.query_data_sources().json()["datasources"]["datasource"]
    workbooks = tableau_connector.query_workbooks_for_site().json()["workbooks"]["workbook"]
    # fmt: on

    # Update datasources
    for datasource in datasources:
        if datasource["type"] == "redshift":
            # utils.pprint(datasource)
            connection_response = (
                tableau_connector.query_data_source_connections(
                    datasource_id=datasource["id"]
                ).json()
            )
            # utils.pprint(connection_response)
            connections = connection_response["connections"]["connection"]
            for connection in connections:
                if connection["userName"] == "tableau":
                    utils.pprint(
                        tableau_connector.update_data_source_connection(
                            datasource_id=datasource["id"],
                            connection_id=connection["id"],
                            new_password=new_password,
                        ).text
                    )

    # Update workbooks
    for workbook in workbooks:
        # utils.pprint(workbook)
        connection_response = tableau_connector.query_workbook_connections(
            workbook_id=workbook["id"]
        ).json()
        # utils.pprint(connection_response)
        connections = connection_response["connections"]["connection"]
        for connection in connections:
            if (
                connection["type"] == "redshift"
                and connection["userName"] == "tableau"
            ):
                utils.pprint(
                    tableau_connector.update_workbook_connection(
                        workbook_id=workbook["id"],
                        connection_id=connection["id"],
                        new_password=new_password,
                    ).text
                )


def get_user_email_list(tableau_connector: tableau.TableauConnector) -> None:
    """
    Get the emails for the licensed users in the server.
    """

    users = tableau_connector.get_users_on_site().json()["users"]["user"]
    emails = [
        user["email"] for user in users if user["siteRole"] != "Unlicensed"
    ]
    utils.pprint(emails)  # type: ignore


def main() -> None:
    """
    Manually test/use the API client.
    """

    agency_payments_workbook_id = (
        "60e884e0-2660-44e1-a1b2-56d855d6d91d"  # Just an example
    )
    tableau_connector = tableau.TableauConnector(
        domain="tableau.prod.company",
        api_key=os.environ["TABLEAU__API_KEY"],
        api_secret=os.environ["TABLEAU__API_SECRET"],
        auth_type=os.environ["TABLEAU__AUTH_TYPE"],
    )

    utils.pprint(tableau_connector.query_data_sources().text)
    utils.pprint(tableau_connector.query_workbooks_for_site().text)
    utils.pprint(
        tableau_connector.query_workbook_connections(
            agency_payments_workbook_id
        ).text
    )

    utils.pprint(tableau_connector.get_users_on_site().text)
    # utils.pprint(tableau_connector.update_workbook_now(workbook_id=agency_payments_workbook_id).text)
    # utils.pprint(tableau_connector.query_workbook_connections(workbook_id=agency_payments_workbook_id).text)

    # change_objects_owner(tableau_connector)
    # change_connection_passwords(tableau_connector)
    # get_user_email_list(tableau_connector)


if __name__ == "__main__":
    main()
