import json
import pathlib

import utils

import sainsburys_store_locator

# The public API is limited to 20 results per request
CHUNK_SIZE = 20


def get_all_stores(
    store_locator: sainsburys_store_locator.StoreLocatorConnector,
) -> list[dict]:
    """
    Get all stores from the API by making multiple requests.
    """

    stores, results = [], -1
    while results != 0:
        print("•", end="")
        params = {
            "limit": CHUNK_SIZE,
            "offset": len(stores),
            "fields": "closed,code,contact,location,name,other_name,store_type",
        }
        response = store_locator.get_stores(params).json()["results"]
        results = len(response)
        stores.extend(response)
    print()

    return stores


def main() -> None:
    """
    Manually test the API client.
    """

    store_locator = sainsburys_store_locator.StoreLocatorConnector()

    utils.pprint(store_locator.get_stores().json())
    utils.pprint(store_locator.get_store_by_id(store_id=2).json())

    all_stores = get_all_stores(store_locator)
    print(len(all_stores))
    f = pathlib.Path("data/sainsburys-stores.json")
    f.write_text(json.dumps(all_stores), encoding="utf-8")


if __name__ == "__main__":
    main()
