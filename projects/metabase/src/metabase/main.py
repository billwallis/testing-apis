"""
Manual testing for the API clients.
"""

import os

import dotenv
import utils

import metabase

dotenv.load_dotenv()

BASE_URL = "http://localhost:3000/api/"


def list_databases(mb_connector: metabase.MetabaseConnector) -> None:
    """
    List all databases defined in Metabase.
    """
    for db in mb_connector.get_databases().json()["data"]:
        utils.pprint(db)
        print(db["id"], db["name"], db["updated_at"])


def main() -> None:
    """
    Manually test the API client.
    """
    metabase_connector = metabase.MetabaseConnector(
        base_url=BASE_URL,
        api_key=os.environ["METABASE__API_KEY"],
        api_secret=os.environ["METABASE__API_SECRET"],
    )

    utils.pprint(metabase_connector.get_user_current().json())
    utils.pprint(metabase_connector.get_databases().json())
    utils.pprint(metabase_connector.get_database_by_id(2).json())

    list_databases(metabase_connector)


if __name__ == "__main__":
    main()
