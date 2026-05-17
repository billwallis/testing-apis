"""
Post to a Microsoft Teams channel using the Microsoft Teams Webhook,
enabled via Workflows:

- https://learn.microsoft.com/en-us/connectors/teams/#microsoft-teams-webhook
"""

import os
from typing import Literal, TypedDict

import requests

type AdaptiveCard = dict


class MessagePayload(TypedDict):
    type: Literal["message"]
    attachments: list[AdaptiveCard]


def _create_adaptive_card(message: str) -> AdaptiveCard:
    # https://adaptivecards.io/samples/
    return {
        "contentType": "application/vnd.microsoft.card.adaptive",
        "contentUrl": None,
        "content": {
            "$schema": "http://adaptivecards.io/schemas/adaptive-card.json",
            "type": "AdaptiveCard",
            "version": "1.2",
            "body": [
                {
                    "type": "TextBlock",
                    "style": "heading",
                    "text": "Sent from Python",
                },
                {
                    "type": "TextBlock",
                    "text": message,
                    "wrap": True,
                },
            ],
        },
    }


def _create_message_payload(attachments: list[AdaptiveCard]) -> MessagePayload:
    # https://learn.microsoft.com/en-us/connectors/teams/?tabs=text1,dotnet#request-body-example
    return {
        "type": "message",
        "attachments": attachments,
    }


def microsoft_teams_message(message: str) -> None:
    """
    Send a message to the configured Microsoft Teams channel.
    """

    requests.post(
        url=os.environ["MICROSOFT_TEAMS_WEBHOOK_URL"],
        json=_create_message_payload(
            attachments=[_create_adaptive_card(message=message)],
        ),
    )
