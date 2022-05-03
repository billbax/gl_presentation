from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
from selenium.common.exceptions import UnexpectedTagNameException
import pandas as pd
import os
import time


def create_driver(system_id):
    s = Service("C:/Program Files (x86)/chromedriver.exe")
    options = webdriver.ChromeOptions()
    options.add_argument("headless")
    options.add_argument("--window-size=1920,1080")
    driver = webdriver.Chrome(service=s, options=options)
    driver.get(f"https://sysadmin.cmaphq.com/Clients/Client/{system_id}")
    driver.find_element(By.ID, "username").send_keys(os.environ["EMAIL"])
    driver.find_element(By.ID, "password").send_keys(os.environ["PW"], Keys.RETURN)

    # Create a list containing all the offices set up within the system
    office_elements = driver.find_elements(By.CSS_SELECTOR, "div.content-body.orgmap h4")
    offices_list = [office.get_attribute("textContent").rstrip(" +") for office in office_elements]

    # Create a list containing all the teams set up within the system
    team_elements = driver.find_elements(By.CSS_SELECTOR, "div.content-body.orgmap ul li")
    teams_list = [team.get_attribute("textContent") for team in team_elements]

    # Create a list containing all of the admins currently set up within the system
    admin_elements = driver.find_elements(By.CSS_SELECTOR, "div#side-wrapper ul#admins li div a")
    admin_list = [admin.text for admin in admin_elements]

    driver.find_elements(By.XPATH, "//a[contains(@href, '/Clients/LoginAs?punter=')]")[1].click()
    driver.switch_to.window(driver.window_handles[1])
    driver.find_element(By.XPATH, "//a[@href='/Admin']").click()

    # Go to expenses section and return a list of all options
    driver.find_element(By.XPATH, "//a[@href='/Admin/Admin/ListEditor?id=2']").click()
    expenses_list = [item.text for item in driver.find_elements(By.CLASS_NAME, "label")]

    # Go to internal codes section and return a list of all options
    driver.find_element(By.XPATH, "//a[@href='/Admin/Admin/ListEditor?id=3']").click()
    internal_codes_list = [item.text for item in driver.find_elements(By.CLASS_NAME, "label")]

    # Go to dropdown options section and return sector and project types
    driver.find_element(By.XPATH, "//a[@href='/Admin/Admin/DropdownListEditor']").click()
    # Get Project types
    Select(driver.find_element(By.ID, "selected-listid")).select_by_visible_text("Project Types")
    time.sleep(0.5)
    proj_type_list = [item.text for item in driver.find_elements(By.CLASS_NAME, "label")]
    # Get sectors
    Select(driver.find_element(By.ID, "selected-listid")).select_by_visible_text("Sectors")
    time.sleep(0.5)
    sector_list = [item.text for item in driver.find_elements(By.CLASS_NAME, "label")]

    driver.find_element(By.XPATH, "//a[@href='/Finance']").click()
    try:
        Select(driver.find_element(By.ID, "officeId")).select_by_index(1)
        time.sleep(2.5)
    except UnexpectedTagNameException:
        print("No Office Option")
    finally:
        Select(driver.find_element(By.ID, "businessId")).select_by_index(1)
        time.sleep(2.5)
    role_elements = driver.find_elements(By.CSS_SELECTOR, "tbody#budgetlist tr td:nth-child(2)")
    roles_list = [item.get_attribute("textContent") for item in role_elements]

    driver.quit()

    d = dict(Admins=admin_list, expense_categories=expenses_list, internal_codes=internal_codes_list,
             Project_Type=proj_type_list, Sector=sector_list, Role=roles_list, Office=offices_list, Team=teams_list)

    config_df = pd.DataFrame({k: pd.Series(v) for k, v in d.items()})
    config_df.rename({"Admins": "Person", "expense_categories": "Category", "internal_codes": "Internal Code",
                      "Project_Type": "Project Type"}, axis=1, inplace=True)

    return config_df


