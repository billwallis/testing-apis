from tfl import connector


def test__connector_properties_are_correct():
    connection = connector.TFLConnector()

    assert connection.base_url == "https://api.tfl.gov.uk/"
    assert connection.request_headers == {
        "Content-Type": "application/json",
        "Accept": "application/json",
    }
