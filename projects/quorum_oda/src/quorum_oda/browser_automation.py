import contextlib
import datetime
import logging
import os
import pathlib
import time

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver

logger = logging.getLogger(__name__)
logging.basicConfig(
    level=logging.INFO,
    format="\033[38;5;240m%(asctime)s\033[0m  %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)

HERE = pathlib.Path(__file__).resolve().parent
HOME = pathlib.Path.home().resolve()
LOGIN_EMAIL = os.environ["MICROSOFT_EMAIL"]
LOGIN_PASSWORD = os.environ["MICROSOFT_PASSWORD"]
QUORUM_HOME_URL = "https://quorum.okta.com/app/UserHome"
QUORUM_SELECT_TENANT_URL = "https://od.ogsys.com/select_tenant"
QUORUM_COMPANIES_URL = "https://od.ogsys.com/166/companies"
QUORUM_TRIAL_BALANCE_REPORT_URL = (
    "https://od.ogsys.com/166/reports/trial_balance_report/c/212"
)
QUORUM_OUTPUT_MANAGER_URL = "https://od.ogsys.com/166/reports/output/manage"
QUORUM_AUTH_URL = "https://quorum.okta.com/oauth2/v1/authorize"
MICROSOFT_SSO_URL = "https://login.microsoftonline.com/"
MICROSOFT_STAY_SIGNED_IN_URL = (
    "https://login.microsoftonline.com/common/SAS/ProcessAuth"
)
EXCEL_REPORT_DOWNLOAD_PATH = HOME / "Downloads/Multi-Company Trial Balance.xlsx"
EXCEL_REPORT_TARGET_DIR = HERE / "data"


def microsoft_sso(driver: WebDriver) -> None:
    logger.info("Entering Microsoft email into Microsoft SSO text box")
    microsoft_email_text_box = driver.find_element(by=By.NAME, value="loginfmt")
    microsoft_email_text_box.clear()
    microsoft_email_text_box.send_keys(LOGIN_EMAIL)

    logger.info("Clicking email `Submit` button for Microsoft SSO")
    driver.find_element(by=By.ID, value="idSIButton9").click()
    time.sleep(3)

    logger.info("Entering Microsoft password into Microsoft SSO text box")
    microsoft_password_text_box = driver.find_element(
        by=By.NAME,
        value="passwd",
    )
    microsoft_password_text_box.clear()
    microsoft_password_text_box.send_keys(LOGIN_PASSWORD)

    logger.info("Clicking password `Submit` button for Microsoft SSO")
    driver.find_element(by=By.ID, value="idSIButton9").click()
    time.sleep(3)

    logger.info("Clicking `Text <mobile number>` button")
    driver.find_element(
        by=By.XPATH,
        value="/html/body/div/form[1]/div/div/div[2]/div[1]/div/div/div/div/div/div[2]/div[2]/div/div[2]/div/div[2]/div/div[1]/div",
    ).click()
    while driver.current_url != MICROSOFT_STAY_SIGNED_IN_URL:
        logger.info("Waiting for OTP to be entered...")
        time.sleep(3)

    logger.info('Clicking `Yes` button for "Stay signed in?"')
    driver.find_element(by=By.ID, value="idSIButton9").click()
    time.sleep(5)


def quorum_sign_in(driver: WebDriver) -> None:
    logger.info("Entering Microsoft email into Quorum sign-in text box")
    username_text_box = driver.find_element(by=By.ID, value="input28")
    username_text_box.clear()
    username_text_box.send_keys(LOGIN_EMAIL)

    logger.info("Clicking `Keep me signed in` checkbox")
    driver.find_element(
        by=By.XPATH,
        value="/html/body/div[2]/div[2]/main/div[2]/div/div/div[2]/form/div[1]/div[3]/div[2]/div/span/div/label",
    ).click()

    logger.info("Clicking `Submit` button for Quorum sign-in")
    driver.find_element(by=By.CLASS_NAME, value="button-primary").click()
    time.sleep(5)

    # Microsoft SSO
    if driver.current_url.startswith(MICROSOFT_SSO_URL):
        logger.info("Logging in with Microsoft SSO")
        microsoft_sso(driver)


def go_to_trial_balance_report(driver: WebDriver) -> None:
    logger.info("Navigating to Quorum home page")
    driver.get(QUORUM_HOME_URL)
    time.sleep(3)
    if driver.current_url.startswith(QUORUM_AUTH_URL):
        logger.info("Signing in to Quorum")
        quorum_sign_in(driver)

    logger.info("Clicking the ODA application link (opens new tab)")
    driver.find_element(
        by=By.XPATH,
        value="/html/body/div[2]/div/div/div/div/section/main/div/section/section/section/section/div/section/div[2]/a/article/section/img",
    ).click()
    time.sleep(5)

    logger.info("Switching to the new tab")
    original_window_handle = driver.current_window_handle
    new_window_handle = (
        set(driver.window_handles) - {original_window_handle}
    ).pop()
    driver.switch_to.window(new_window_handle)
    assert driver.current_window_handle == new_window_handle

    while driver.current_url != QUORUM_COMPANIES_URL:
        logger.info("Waiting for ODA landing page to load...")
        driver.refresh()
        time.sleep(3)

        if driver.current_url == QUORUM_SELECT_TENANT_URL:
            logger.info("Selecting ODA tenant")

            logger.info("Clicking the `Database` box to list the options")
            driver.find_element(
                by=By.XPATH,
                value="/html/body/div[1]/section/article/div/div/form/fieldset/div/div",
            ).click()
            time.sleep(1)

            logger.info(
                "Clicking the `166: Formentera Operations Production` option"
            )
            driver.find_element(
                by=By.XPATH,
                value="/html/body/div[3]/ul/li[1]/div",
            ).click()
            time.sleep(1)

            logger.info("Clicking the `Select Database` button")
            driver.find_element(
                by=By.XPATH,
                value="/html/body/div[1]/section/article/div/div/form/div[3]/div/button",
            ).click()

    logger.info("Navigating to ODA trial balance report page")
    driver.get(QUORUM_TRIAL_BALANCE_REPORT_URL)
    time.sleep(3)


def trigger_trial_balance_report(driver: WebDriver) -> None:
    logger.info("Clicking the `Basis` box to list the options")
    driver.find_element(
        by=By.XPATH,
        value="/html/body/div[1]/section/article/form/div[4]/div/fieldset/span/span/span[1]",
    ).click()
    time.sleep(1)

    logger.info("Selecting the `Accrual-Date With Closed Items ` option")
    driver.find_element(
        by=By.XPATH,
        value="/html/body/div[10]/div/div[2]/ul/li[3]",
    ).click()
    time.sleep(1)

    logger.info("Clicking `Company Code` checkbox")
    driver.find_element(
        by=By.XPATH,
        value="/html/body/div[1]/section/article/form/div[11]/div/fieldset/div[2]/label",
    ).click()
    time.sleep(1)

    logger.info("Clicking `Run Report` button")
    driver.find_element(
        by=By.XPATH,
        value="/html/body/div[1]/section/article/form/p/button",
    ).click()
    time.sleep(3)


def download_trial_balance_report(driver: WebDriver) -> None:
    # Check we're in the output manager
    assert driver.current_url == QUORUM_OUTPUT_MANAGER_URL
    logger.info("Waiting for trial balance report to generate...")
    time.sleep(45)

    latest_report_row = None
    status_cell_status = ""
    while status_cell_status != "status-icon active":
        logger.info("Checking whether the report is ready to download...")
        driver.refresh()
        time.sleep(3)
        latest_report_row = driver.find_element(
            by=By.XPATH,
            value="/html/body/div[1]/section/article/div/div[1]/div/div/div[2]/table/tbody/tr[1]",
        )
        status_cell = latest_report_row.find_element(by=By.XPATH, value="td[4]")
        assert status_cell.get_attribute(name="data-field") == "Status"
        status_cell_contents = status_cell.find_elements(
            by=By.TAG_NAME,
            value="span",
        )
        assert len(status_cell_contents) == 1
        status_cell_status = status_cell_contents[0].get_attribute(name="class")

    logger.info("Clicking the report's download button")
    assert latest_report_row is not None
    latest_report_row.find_element(by=By.XPATH, value="td[11]/ul/li/a").click()
    time.sleep(3)

    while not EXCEL_REPORT_DOWNLOAD_PATH.exists():
        logger.info("Waiting for report to download")
        time.sleep(3)


def trigger_and_download_report(driver: WebDriver) -> None:
    go_to_trial_balance_report(driver)
    trigger_trial_balance_report(driver)
    download_trial_balance_report(driver)


def copy_to_archive(
    source_file: pathlib.Path,
    target_directory: pathlib.Path,
) -> None:
    assert source_file.exists()

    target_file = source_file.with_stem(
        f"{source_file.stem} {datetime.datetime.now(datetime.UTC).isoformat()}"
    )
    source_file.rename(target_file)
    target_file.move_into(target_directory)
    logger.info(
        f"Copied file '{source_file}' to '{target_directory}' directory"
    )


@contextlib.contextmanager
def chrome_driver() -> WebDriver:
    driver = webdriver.Chrome()
    try:
        yield driver
    finally:
        driver.quit()


def main() -> int:
    if EXCEL_REPORT_DOWNLOAD_PATH.exists():
        logger.error(
            f"error: a copy of the report already exists at {EXCEL_REPORT_DOWNLOAD_PATH}"
        )
        return 1

    rc = 0
    with chrome_driver() as driver:
        try:
            trigger_and_download_report(driver)
        except Exception as err:
            logger.error(err)
            rc = 1

    if rc != 0:
        return rc

    copy_to_archive(
        source_file=EXCEL_REPORT_DOWNLOAD_PATH,
        target_directory=EXCEL_REPORT_TARGET_DIR,
    )

    return 0


if __name__ == "__main__":
    raise SystemExit(main())  # pragma: no cover
