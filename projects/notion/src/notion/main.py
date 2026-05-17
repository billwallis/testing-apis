"""
Manual testing for the API clients.
"""

import os

import dotenv
import utils

import notion

dotenv.load_dotenv()


def main() -> None:
    """
    Manually test the API client.
    """
    notion_connector = notion.NotionConnector(
        api_token=os.environ["NOTION__API_TOKEN"],
    )
    utils.pprint(notion_connector.get_users().json())


if __name__ == "__main__":
    main()
