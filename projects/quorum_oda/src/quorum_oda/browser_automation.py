import datetime
import os
import pathlib
import time

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver

HERE = pathlib.Path(__file__).resolve().parent
HOME = pathlib.Path.home().resolve()
LOGIN_EMAIL = os.environ["MICROSOFT_EMAIL"]
LOGIN_PASSWORD = os.environ["MICROSOFT_PASSWORD"]
QUORUM_HOME_URL = "https://quorum.okta.com/app/UserHome"
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
    microsoft_email_text_box = driver.find_element(by=By.NAME, value="loginfmt")
    microsoft_email_text_box.clear()
    microsoft_email_text_box.send_keys(LOGIN_EMAIL)

    # Click `Submit` button
    driver.find_element(by=By.ID, value="idSIButton9").click()
    time.sleep(3)

    microsoft_password_text_box = driver.find_element(
        by=By.NAME,
        value="passwd",
    )
    microsoft_password_text_box.clear()
    microsoft_password_text_box.send_keys(LOGIN_PASSWORD)

    # Click `Submit` button
    driver.find_element(by=By.ID, value="idSIButton9").click()
    time.sleep(3)

    # Click `Text <mobile number>` button
    driver.find_element(
        by=By.XPATH,
        value="/html/body/div/form[1]/div/div/div[2]/div[1]/div/div/div/div/div/div[2]/div[2]/div/div[2]/div/div[2]/div/div[1]/div",
    ).click()
    while driver.current_url != MICROSOFT_STAY_SIGNED_IN_URL:
        time.sleep(3)

    # Click `Yes` button for "Stay signed in?"
    driver.find_element(by=By.ID, value="idSIButton9").click()
    time.sleep(5)


def quorum_sign_in(driver: WebDriver) -> None:
    username_text_box = driver.find_element(by=By.ID, value="input28")
    username_text_box.clear()
    username_text_box.send_keys(LOGIN_EMAIL)

    # Click `Keep me signed in` checkbox
    driver.find_element(
        by=By.XPATH,
        value="/html/body/div[2]/div[2]/main/div[2]/div/div/div[2]/form/div[1]/div[3]/div[2]/div/span/div/label",
    ).click()

    # Click `Submit` button
    driver.find_element(by=By.CLASS_NAME, value="button-primary").click()
    time.sleep(5)

    # Microsoft SSO
    if driver.current_url.startswith(MICROSOFT_SSO_URL):
        microsoft_sso(driver)


def go_to_trial_balance_report(driver: WebDriver) -> None:
    driver.get(QUORUM_HOME_URL)
    time.sleep(3)
    # driver.implicitly_wait(5)

    if driver.current_url.startswith(QUORUM_AUTH_URL):
        quorum_sign_in(driver)

    ### Navigate to ODA

    # Click the ODA application link which opens a new tab
    driver.find_element(
        by=By.XPATH,
        value="/html/body/div[2]/div/div/div/div/section/main/div/section/section/section/section/div/section/div[2]/a/article/section/img",
    ).click()
    time.sleep(5)

    # Switch to the new tab
    original_window_handle = driver.current_window_handle
    new_window_handle = (
        set(driver.window_handles) - {original_window_handle}
    ).pop()
    driver.switch_to.window(new_window_handle)
    assert driver.current_window_handle == new_window_handle

    # Close the previous tab
    # driver.close()

    while driver.current_url != QUORUM_COMPANIES_URL:
        driver.refresh()
        time.sleep(3)

    driver.get(QUORUM_TRIAL_BALANCE_REPORT_URL)
    time.sleep(3)


def trigger_trial_balance_report(driver: WebDriver) -> None:
    # Click the Basis box to list the options
    driver.find_element(
        by=By.XPATH,
        value="/html/body/div[1]/section/article/form/div[4]/div/fieldset/span/span/span[1]",
    ).click()
    time.sleep(1)

    # Select the `Accrual-Date With Closed Items ` option
    driver.find_element(
        by=By.XPATH,
        value="/html/body/div[10]/div/div[2]/ul/li[3]",
    ).click()
    time.sleep(1)

    # Click `Company Code` checkbox
    driver.find_element(
        by=By.XPATH,
        value="/html/body/div[1]/section/article/form/div[11]/div/fieldset/div[2]/label",
    ).click()
    time.sleep(1)

    # Click `Run Report` button
    driver.find_element(
        by=By.XPATH,
        value="/html/body/div[1]/section/article/form/p/button",
    ).click()
    time.sleep(3)


def download_trial_balance_report(driver: WebDriver) -> None:
    # Check we're in the output manager
    assert driver.current_url == QUORUM_OUTPUT_MANAGER_URL
    time.sleep(45)

    latest_report_row = None
    status_cell_status = ""
    while status_cell_status != "status-icon active":
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

    # Click the report's download button
    assert latest_report_row is not None
    latest_report_row.find_element(by=By.XPATH, value="td[11]/ul/li/a").click()
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
        f"{source_file.stem} {datetime.datetime.now().isoformat()}"
    )
    source_file.rename(target_file)
    target_file.move_into(target_directory)


def main() -> int:
    if EXCEL_REPORT_DOWNLOAD_PATH.exists():
        print(
            f"error: a copy of the report already exists at {EXCEL_REPORT_DOWNLOAD_PATH}"
        )
        return 1

    rc = 0
    chrome_driver = webdriver.Chrome()  # TODO: wrap this in a context manager
    try:
        trigger_and_download_report(chrome_driver)
    except Exception as err:
        print(err)
        rc = 1
    chrome_driver.quit()
    if rc != 0:
        return rc

    copy_to_archive(
        source_file=EXCEL_REPORT_DOWNLOAD_PATH,
        target_directory=EXCEL_REPORT_TARGET_DIR,
    )

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
