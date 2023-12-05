import PySimpleGUI as sg
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import (
    TimeoutException,
    NoSuchElementException,
    ElementClickInterceptedException,
    ElementNotInteractableException,
)
import time
import lxml


ser = Service(r"chromedriver.exe")
driver = webdriver.Chrome(service=ser)
driver.set_window_size(800, 800)
driver.implicitly_wait(20)
driver.set_page_load_timeout(50)

def safe_click(by, value, timeout=10):
    try:
        element = WebDriverWait(driver, timeout).until(
            EC.element_to_be_clickable((by, value))
        )
        element.click()
        return True
    except TimeoutException:
        print(
            f"Timeout: Element with ({by}, {value}) not clickable after {timeout} seconds."
        )
    except NoSuchElementException:
        print(f"No such element: Element with ({by}, {value}) not found.")
    except ElementClickInterceptedException:
        print(
            f"Click intercepted: Element with ({by}, {value}) click intercepted by another element."
        )
    except ElementNotInteractableException:
        print(f"Not interactable: Element with ({by}, {value}) is not interactable.")
    except Exception as e:
        print(f"Unexpected error: {e}")
    return False


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

def click_header_tab():
    time.sleep(0.5)
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

def go_to_detail_header():
    detail_header_css = "#ops-auth-tabs > ul > li:nth-child(3) > a"
    safe_click( By.CSS_SELECTOR, detail_header_css)


def fetch_requested_dos():
    try:
        from_date = driver.find_element(By.ID, "FromDate").get_attribute("value")
        through_date = driver.find_element(By.ID, "ThroughDate").get_attribute("value")
        dos = f"{from_date}-{through_date}"
        return dos
    except Exception as e:
        print(f"Error updating requested_dos: {e}")


def get_number_of_detail_rows():
    table = driver.find_element(By.ID, 'authDetailsGrid')
    num_rows = len(table.find_elements(By.TAG_NAME, 'tr')) - 1
    return num_rows




def fetch_procedure_codes():
    # TODO: grab procedure codes from details tab and populate into multiline.
    go_to_detail_header()
    time.sleep(1)
    codes = []
    table_html = driver.find_element(By.ID, 'authDetailsGrid').get_attribute('outerHTML')
    soup = BeautifulSoup(table_html, 'html.parser')

    rows = soup.find_all('tr')[1:]
    for row in rows:
        columns = row.find_all('td')
        codes.append(columns[7].get_text(strip=True))

    return codes


