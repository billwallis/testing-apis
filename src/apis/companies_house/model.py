"""
Domain objects for working with the Companies House API.
"""

import enum
import http
import re
from typing import Protocol

import requests


class OfficerRegisterType(enum.Enum):
    DIRECTORS = "directors"
    SECRETARIES = "secretaries"
    LLP_MEMBERS = "llp-members"


class OfficerOrderBy(enum.Enum):
    APPOINTED_ON = "appointed_on"
    RESIGNED_ON = "resigned_on"
    SURNAME = "surname"


class CompanyNumberValueError(Exception):
    """
    Invalid company number.
    """

    def __init__(self, company_number: str | int) -> None:
        super().__init__(
            f"The company number must be exactly 8 characters long and include the leading 0."
            f" The company number {company_number} is invalid"
        )


def _is_valid_company_number(company_number: str | int) -> bool:
    """
    Return whether a company number is valid.
    """
    valid_length = 8

    if isinstance(company_number, str):
        length = len(company_number)
        return length == valid_length or (
            length < valid_length and re.match(r"\D", company_number) is None
        )
    if isinstance(company_number, int):
        return company_number > 0 and len(str(company_number)) <= valid_length
    return False


def _format_company_number(company_number: str | int) -> str:
    """
    Format a company number as required by the API.
    """
    return str(company_number).zfill(8)


class CompanyNumber:
    def __init__(self, company_number: str | int) -> None:
        if not _is_valid_company_number(company_number):
            raise CompanyNumberValueError(company_number)
        self.company_number = _format_company_number(company_number)

    def __str__(self) -> str:
        return self.company_number


class ICompaniesHouseConnector(Protocol):
    """
    Interface for the Companies House Connector.
    """

    def get_company_profile(
        self, company_number: CompanyNumber
    ) -> requests.Response: ...

    def get_company_officers(
        self,
        company_number: CompanyNumber,
        items_per_page: int = 35,
        register_type: OfficerRegisterType = "",
        register_view: bool = False,
        start_index: int = 0,
        order_by: OfficerOrderBy = "",
    ) -> requests.Response: ...


class Company:
    def __init__(
        self,
        companies_house_connector: ICompaniesHouseConnector,
        company_number: CompanyNumber,
        validate_company_number_on_init: bool = True,
    ) -> None:
        self._connector = companies_house_connector
        self._company_number = company_number
        self._company_profile: dict or None = None
        self._company_officers: list[dict] or None = None

        if validate_company_number_on_init:
            self.set_company_number()

    def set_company_number(self) -> None:
        self._company_number = self.get_company_profile()["company_number"]

    @property
    def company_number(self) -> str or int:
        return self._company_number

    def get_company_profile(self, force_update: bool = False) -> dict:
        """
        Get the profile of the company.
        """
        if force_update or self._company_profile is None:
            company_profile = self._connector.get_company_profile(
                company_number=self.company_number,
            )
            if company_profile.status_code == http.HTTPStatus.NOT_FOUND:
                raise ValueError(
                    f"Company number {self.company_number} not found"
                )
            self._company_profile = company_profile.json()
        return self._company_profile

    def get_company_officers(
        self,
        force_update: bool = False,
        page_size: int = 100,
    ) -> dict:
        """
        Retrieve the full list of officers.

        TODO: Split this into smaller methods and introduce an Officer class (maybe)
        """
        if force_update or self._company_officers is None:
            enumerated_items = 0
            self._company_officers = []
            total_items = self._connector.get_company_officers(
                company_number=self.company_number,
                items_per_page=1,
            ).json()["total_results"]
            while enumerated_items < total_items:
                self._company_officers += self._connector.get_company_officers(
                    company_number=self.company_number,
                    items_per_page=page_size,
                    start_index=enumerated_items,
                ).json()["items"]
                enumerated_items += page_size
            for officer in self._company_officers:
                appointments = officer["links"]["officer"]["appointments"]
                # officer["id"] = appointments[10:-12]  # Not sure if it's always a specific position/length
                for replacement in ["/officers/", "/appointments"]:
                    appointments = appointments.replace(replacement, "")
                officer["officer_id"] = appointments
        return self._company_officers
