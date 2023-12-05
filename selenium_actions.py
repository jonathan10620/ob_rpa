import PySimpleGUI as sg
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.common.exceptions import (
    TimeoutException,
    NoSuchElementException,
    ElementClickInterceptedException,
    ElementNotInteractableException,
)
import time


ser = Service(r"chromedriver.exe")
driver = webdriver.Chrome(service=ser)
driver.set_window_size(800, 800)
driver.implicitly_wait(20)
driver.set_page_load_timeout(50)


def load_ticket_page(auth, portal):
    """
    Load Ticket Page

    This function navigates the web driver to a specific ticket page for authorization using the provided authentication
    number and portal ID.
    """
    try:
        driver.get(
            f"https://operations.tmhp.net/PA/PawfTicket/LoadTicketForAuthorization?authorizationNumber={auth}&portalId={portal}&refererSource=SearchResults"
        )
    except TimeoutException as e:
        sg.popup("Page took too long to load.")
    except Exception as e:
        sg.popup(f"An unexpected error occurred: {e}")
    driver.execute_script("document.body.style.zoom=' 50%'")

def click_header_tab():
    css_selector = "#ops-auth-tabs > ul > li:nth-child(2) > a"
    xpath = '//*[@id="ops-auth-tabs"]/ul/li[2]/a'
    full_x = "/html/body/div[1]/main/div[3]/ul/li[2]/a"

    for method, value in [
        (By.CSS_SELECTOR, css_selector),
        (By.XPATH, xpath),
        (By.XPATH, full_x),
    ]:
        try:
            driver.find_element(method, value).click()
            return
        except Exception as e:
            print(f"Clicking header tab failed for {method}: {value}")

def fetch_requested_dos():
    try:
        from_date = driver.find_element(By.ID, "FromDate").get_attribute("value")
        through_date = driver.find_element(By.ID, "ThroughDate").get_attribute("value")
        dos = f"{from_date}-{through_date}"
        return dos
    except Exception as e:
        print(f"Error updating requested_dos: {e}")







def fetch_procedure_codes():
    # TODO: grab procedure codes from details tab and populate into multiline.
    return '76814\n76815\n76811'