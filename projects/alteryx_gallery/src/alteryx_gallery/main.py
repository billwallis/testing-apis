"""
Manual testing for the API clients.
"""

import os

import dotenv
import utils

import alteryx_gallery

dotenv.load_dotenv()

BASE_URL = "http://172.28.67.186/api/"
USAGE_REPORT_ID = "61923e7325d33410083f8932"


def main() -> None:
    """
    Manually test the API client.
    """
    conn = alteryx_gallery.GalleryConnector(
        base_url=BASE_URL,
        api_key=os.environ["ALTERYX_GALLERY__API_KEY"],
        api_secret=os.environ["ALTERYX_GALLERY__API_SECRET"],
    )
    utils.pprint(conn.get_shared_credentials().json())
    utils.pprint(conn.enqueue(workflow_id=USAGE_REPORT_ID).json())


if __name__ == "__main__":
    main()
