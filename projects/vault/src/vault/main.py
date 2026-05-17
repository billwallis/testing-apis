import os

import dotenv
import utils

import vault

dotenv.load_dotenv()


def main() -> None:
    """
    Manually test the API client.
    """
    vault_connector = vault.VaultConnector(
        domain=os.environ["VAULT__DOMAIN"],
        api_key=os.environ["VAULT__API_KEY"],
        api_secret=os.environ["VAULT__API_SECRET"],
    )

    utils.pprint(vault_connector.list_roles().json())
    utils.pprint(vault_connector.list_connections().json())

    response = vault_connector.read_secret(role_name="dwh_someone")
    utils.pprint(response.json())


if __name__ == "__main__":
    main()
