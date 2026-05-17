"""
API clients for the Sainsbury's Store Locator.

https://app.swaggerhub.com/apis-docs/JSainsburys/Storelocater_API_PROD/1.0.0

The user-friendly front-end is:

https://stores.sainsburys.co.uk/
"""

from sainsburys_store_locator.connector import StoreLocatorConnector

__all__ = [
    "StoreLocatorConnector",
]
