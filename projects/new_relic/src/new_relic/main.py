import os

import dotenv

import new_relic

dotenv.load_dotenv()


def main() -> None:
    """
    Manually test the API client.
    """
    new_relic_connector = new_relic.NewRelicConnector(
        account_id=os.environ["NEW_RELIC__ACCOUNT_ID"],
        api_key=os.environ["NEW_RELIC__API_KEY"],
    )
    print(new_relic_connector)


if __name__ == "__main__":
    main()
