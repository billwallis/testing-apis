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
JANUARY = 1
DECEMBER = 12


def _subtract_month(date: datetime.date) -> datetime.date:
    """
    Subtract a month from a date, handling year transitions, but not day
    overflow.
    """

    if date.month == JANUARY:
        return datetime.date(date.year - 1, DECEMBER, date.day)
    return datetime.date(date.year, date.month - 1, date.day)


def _add_month(date: datetime.date) -> datetime.date:
    """
    Add a month to a date, handling year transitions, but not day overflow.
    """

    if date.month == DECEMBER:
        return datetime.date(date.year + 1, JANUARY, date.day)
    return datetime.date(date.year, date.month + 1, date.day)


def _get_statement(conn: amex.AmexConnector, date: datetime.date):
    """
    Retrieve a statement for a given end date and save it to a file.
    """

    transactions = conn.get_statement(statement_end_date=date)
    if transactions.status_code != http.HTTPStatus.OK:
        raise RuntimeError(
            f"Failed to retrieve transactions for {date}: {transactions.status_code} {transactions.reason}"
        )
    target = HERE / f"data/activity-{date.strftime('%Y%m%d')}.csv"
    target.unlink(missing_ok=True)
    target.write_bytes(transactions.content)
    print(f"Saved transactions for {date} to {target}")


def get_statements_between(
    conn: amex.AmexConnector,
    start_date: datetime.date,
    end_date: datetime.date,
) -> None:
    """
    Retrieve statements between two dates (inclusive).
    """

    date = end_date
    while date >= start_date:
        _get_statement(conn, date)
        date = _subtract_month(date)


def get_statements_from(
    conn: amex.AmexConnector,
    start_date: datetime.date,
) -> None:
    """
    Retrieve statements from a start date to the current date.
    """

    date = start_date
    while date <= datetime.date.today():
        _get_statement(conn, date)
        date = _add_month(date)


def main() -> None:
    """
    Manually test the API client.
    """

    amex_connector = amex.AmexConnector(
        account_key=os.environ["AMEX__ACCOUNT_KEY"],
        cookie=(HERE / "env/cookie").read_text().strip(),
    )

    # get_statements_between(
    #     conn=amex_connector,
    #     start_date=datetime.date(2025, 1, 26),
    #     end_date=datetime.date(2025, 6, 26),
    # )

    get_statements_from(
        conn=amex_connector,
        start_date=datetime.date(2025, 6, 26),
    )


if __name__ == "__main__":
    main()
