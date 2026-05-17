import pytest
from notion import connector


@pytest.fixture
def connection(monkeypatch: pytest.MonkeyPatch) -> connector.NotionConnector:
    return connector.NotionConnector(
        api_token="a1b2-c3d4",
    )


def test__connector_properties_are_correct(
    connection: connector.NotionConnector,
):
    assert connection.base_url == "https://api.notion.com/v1/"
    assert connection.notion_version == "2022-06-28"
    assert connection.request_headers == {
        "Content-Type": "application/json",
        "Accept": "application/json",
        "Authorization": "Bearer a1b2-c3d4",
        "Notion-Version": "2022-06-28",
    }
