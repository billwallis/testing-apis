"""
Manual testing for the API clients.
"""

import os

import dotenv

from src import utils
from src.apis import twilio

dotenv.load_dotenv()


def main() -> None:
    """
    Manually test the API client.
    """
    twilio_connector = twilio.TwilioConnector(
        workspace=os.getenv("TWILIO__WORKSPACE"),
        api_key=os.getenv("TWILIO__API_KEY"),
        api_secret=os.getenv("TWILIO__API_SECRET"),
    )

    utils.pprint(
        twilio_connector.list_all_events(
            start_datetime="2021-11-29T00:00:00Z",
            end_datetime="2021-11-29T23:59:59Z",
        ).json()
    )


if __name__ == "__main__":
    main()
