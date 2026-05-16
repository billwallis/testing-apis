import contextlib
import json
import os
import pathlib

import dotenv

import companies_house

dotenv.load_dotenv()

HERE = pathlib.Path(__file__).parent


def _write_json(data: dict, filename: str) -> None:
    (HERE / filename).write_text(json.dumps(data), encoding="utf-8")


def main() -> None:
    """
    Manually test the API client.
    """
    ch_conn = companies_house.CompaniesHouseConnector(
        api_key=os.environ["COMPANIES_HOUSE__API_KEY"],
    )

    company_number = companies_house.CompanyNumber(7706156)
    allica_bank = companies_house.Company(
        companies_house_connector=ch_conn,
        company_number=company_number,
    )

    disallowed_company_properties = [
        "previous_company_names",
        "sic_codes",
        "foreign_company_details",
    ]
    disallowed_officer_properties = ["former_names"]
    profile_json = allica_bank.get_company_profile()
    officers_json = allica_bank.get_company_officers()
    with contextlib.suppress(KeyError):
        [profile_json.pop(key) for key in disallowed_company_properties]
        [officers_json.pop(key) for key in disallowed_officer_properties]

    _write_json(profile_json, f"data/{company_number}-profile.json")
    _write_json(officers_json, f"data/{company_number}-officers.json")


if __name__ == "__main__":
    main()
