"""
Manual testing for the API clients.
"""

import datetime
import http
import os
import pathlib

import dotenv

from src.apis import amex

dotenv.load_dotenv()

HERE = pathlib.Path(__file__).parent


def _subtract_month(date: datetime.date) -> datetime.date:
    """
    Subtract a month from a date, handling year transitions, but not day
    overflow.
    """

    if date.month == 1:
        return datetime.date(date.year - 1, 12, date.day)
    return datetime.date(date.year, date.month - 1, date.day)


def main() -> None:
    """
    Manually test the API client.
    """

    amex_connector = amex.AmexConnector(
        account_key=os.environ["AMEX__ACCOUNT_KEY"],
        cookie=(HERE / "env/cookie").read_text().strip(),
    )

    # Get all statements
    date = datetime.date(2025, 6, 26)
    while date >= datetime.date(2025, 1, 26):
        transactions = amex_connector.get_statement(statement_end_date=date)
        if transactions.status_code != http.HTTPStatus.OK:
            raise RuntimeError(
                f"Failed to retrieve transactions for {date}: {transactions.status_code} {transactions.reason}"
            )
        target = HERE / f"data/activity-{date.strftime('%Y%m%d')}.csv"
        target.unlink(missing_ok=True)
        target.write_bytes(transactions.content)
        print(f"Saved transactions for {date} to {target}")
        date = _subtract_month(date)


if __name__ == "__main__":
    main()
