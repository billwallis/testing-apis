"""
Manual testing for the API clients.
"""

import os

import dotenv

import slack

dotenv.load_dotenv()


def main() -> None:
    """
    Manually test the API client.
    """

    slack_connector = slack.SlackConnector(
        webhook_url=os.environ["SLACK__WEBHOOK_URL"],
    )
    slack_connector.post_message(
        text="This is a *test* success message with a link: <https://www.google.com|Google>",
        username="testing-apis",
    )
    slack_connector.post_message(
        text="This is another **test** message.",
        username="testing-apis",
        icon_emoji=":robot_face:",
    )


if __name__ == "__main__":
    main()
