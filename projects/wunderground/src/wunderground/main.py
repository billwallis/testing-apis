import datetime
import json
import os
import pathlib
import time

import duckdb

from wunderground.client import WundergroundConnector

HERE = pathlib.Path(__file__).parent
TARGET_PATH = HERE / "data"
DELAY_SECONDS = 5


def _to_file(data: dict | list[dict], filename: str) -> None:
    (TARGET_PATH / filename).write_text(json.dumps(data, indent=2))


def _get_observations(
    client: WundergroundConnector,
    station_id: str,
    from_date: datetime.date,
    to_date: datetime.date,
) -> None:
    _to_file(
        client.get_summaries(station_id, from_date, to_date, "m"),
        f"summaries-{from_date}-{to_date}.json",
    )

    curr_date = from_date
    while curr_date <= to_date:
        print(f"Getting observations for {curr_date}")
        time.sleep(DELAY_SECONDS)
        _to_file(
            client.get_observations(station_id, curr_date, "m"),
            f"observations-{curr_date}.json",
        )
        curr_date += datetime.timedelta(days=1)


def _parse_files(target_path: pathlib.Path, unit_column: str) -> None:
    parser_sql = (HERE / "parser.sql").read_text()
    duckdb.sql(
        parser_sql.replace("{{ target_dir }}", str(target_path)).replace(
            "{{ unit_column }}", unit_column
        )
    )


def main() -> None:
    # https://www.wunderground.com/history/daily/gb/london/ILONDO440/date/2026-7-13
    print("Connecting to Wunderground...")

    api_key = os.environ["WUNDERGROUND_API_KEY"]
    to_date = datetime.date.today()

    _get_observations(
        client=WundergroundConnector(api_key),
        station_id="ILONDO440",
        from_date=to_date - datetime.timedelta(days=7),
        to_date=to_date,
    )

    _parse_files(
        target_path=TARGET_PATH,
        unit_column="metric",  # or "imperial", not set up for both yet
    )


if __name__ == "__main__":
    main()
