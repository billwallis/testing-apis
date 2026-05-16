"""
API clients for Slack.

The "Incoming Webhooks" option is easy to use (just post to the URL!),
but it's very limited and may be removed in a future version of Slack.

You can generate a webhook URL by navigating to the channel you want to
post to and configuring the "Incoming Webhooks" app.
"""

import http
import json

import requests


class SlackConnector:
    """
    Post a message to a Slack channel.
    """

    webhook_url: str

    def __init__(self, webhook_url: str) -> None:
        self.webhook_url = webhook_url

    def post_message(
        self,
        text: str,
        username: str,
        icon_emoji: str | None = None,
    ) -> None:
        """
        Post a message to the configured channel using the Incoming Webhooks
        Slack app.

        The message can be formatted using Markdown.
        """
        payload = {
            "text": text,
            "username": username,
        }
        if icon_emoji is not None:
            payload["icon_emoji"] = icon_emoji

        response = requests.post(
            url=self.webhook_url,
            data=json.dumps(payload),
        )
        if response.status_code != http.HTTPStatus.OK:
            raise RuntimeError(
                f"{response.status_code}: Failed to post message to Slack\n\n{response.text}"
            )
