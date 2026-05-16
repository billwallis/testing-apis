"""
http://localhost:3000/dashboard/1-property-dashboard
"""

import os
import time

import dotenv
import jwt

dotenv.load_dotenv()

METABASE_SITE_URL = "http://localhost:3000"
METABASE_SECRET_KEY = os.environ["METABASE_SECRET_KEY"]


def main() -> None:
    payload = {
        "resource": {"dashboard": 1},
        "params": {},
        "exp": round(time.time()) + (60 * 10),  # 10 minute expiration
    }
    token = jwt.encode(payload, METABASE_SECRET_KEY, algorithm="HS256")
    iframe_url = f"{METABASE_SITE_URL}/embed/dashboard/{token}#theme=night&bordered=false&titled=true"

    print(iframe_url)


if __name__ == "__main__":
    main()
