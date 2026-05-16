from sainsburys_store_locator import connector


def test__connector_properties_are_correct():
    connection = connector.StoreLocatorConnector()

    assert connection.base_url == "https://api.stores.sainsburys.co.uk/v1/"
    assert connection.request_headers == {
        "Content-Type": "application/json",
        "Accept": "application/json",
    }
