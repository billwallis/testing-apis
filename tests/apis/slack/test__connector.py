import http
from types import SimpleNamespace

import pytest

from src.apis.slack import connector

WEBHOOK_URL = "https://hooks.slack.com/services/A1B2C3D4/E5F6G7H8/i9j0k1l2"


@pytest.fixture
def connection() -> connector.SlackConnector:
    return connector.SlackConnector(WEBHOOK_URL)


def test__connector_properties_are_correct(
    connection: connector.SlackConnector,
):
    assert connection.webhook_url == WEBHOOK_URL


def test__message_can_be_posted_successfully(
    monkeypatch: pytest.MonkeyPatch,
    connection: connector.SlackConnector,
):
    posted_data = []

    def mock_post(url: str, data: str) -> SimpleNamespace:
        posted_data.append({"url": url, "data": data})
        return SimpleNamespace(
            status_code=http.HTTPStatus.OK,
            text="Posted successfully!",
        )

    monkeypatch.setattr(connector, "requests", SimpleNamespace(post=mock_post))
    connection.post_message(
        text="some text",
        username="some-user",
        icon_emoji="some-icon",
    )

    assert len(posted_data) == 1
    assert posted_data[0] == {
        "url": WEBHOOK_URL,
        "data": '{"text": "some text", "username": "some-user", "icon_emoji": "some-icon"}',
    }


def test__message_raises_exception_on_error(
    monkeypatch: pytest.MonkeyPatch,
    connection: connector.SlackConnector,
):
    posted_data = []

    def mock_post(url: str, data: str) -> SimpleNamespace:
        posted_data.append({"url": url, "data": data})
        return SimpleNamespace(
            status_code=http.HTTPStatus.BAD_REQUEST,
            text="I'm a doctor, Jim, not a postman!",
        )

    monkeypatch.setattr(connector, "requests", SimpleNamespace(post=mock_post))

    with pytest.raises(RuntimeError):
        connection.post_message(text="text", username="user")

    assert len(posted_data) == 1
    assert posted_data[0] == {
        "url": WEBHOOK_URL,
        "data": '{"text": "text", "username": "user"}',
    }
