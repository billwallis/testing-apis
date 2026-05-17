"""
Manual testing for the API clients.
"""

import os

import dotenv
import utils

import braze

dotenv.load_dotenv()

BASE_URL = "https://rest.fra-01.braze.eu/"
API_KEYS = {
    "test": os.environ["BRAZE__TEST__API_KEY"],
    "jaja": os.environ["BRAZE__JAJA__API_KEY"],
    "boi": os.environ["BRAZE__BOI__API_KEY"],
    "aa": os.environ["BRAZE__AA__API_KEY"],
}


def main() -> None:
    """
    Manually test the API client.
    """

    brand = "jaja"
    braze_connector = braze.BrazeConnector(
        base_url=BASE_URL,
        brand=brand,
        api_key=API_KEYS[brand],
    )

    # Campaign list
    utils.pprint(braze_connector.get_campaigns_list().text)

    # User Export by Identifier
    user_export_body = {
        "external_ids": [
            "100194",
            "635844",
            "NotInODS_100102",
            "PayB_575974",
            "Jaja_105",
        ],
        "fields_to_export": [
            "external_id",
            "braze_id",
            "campaigns_received",
            "custom_attributes",
            "custom_events",
        ],
    }
    utils.pprint(
        braze_connector.user_profile_export_by_identifier(
            body=user_export_body
        ).json()
    )

    # User Export by Segment
    jaja_segment = "7a09f4c1-0f7a-4dfc-8dec-bba78c73d5c9"
    utils.pprint(
        braze_connector.user_profile_export_by_segment(
            segment_id=jaja_segment
        ).json()
    )


if __name__ == "__main__":
    main()
