from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait


def test_home_page_title(chrome_driver, run_app):
    """
    GIVEN a running app
    WHEN the homepage is accessed
    THEN the value of the page title should be "Paralympics Home"
    """
    # Change the url if you configured a different port!
    chrome_driver.get("http://127.0.0.1:5000/")
    chrome_driver.implicitly_wait(3)
    assert chrome_driver.title == "Paralympics Home"


def test_event_detail_page_selected(chrome_driver, run_app):
    """
    GIVEN a running app
    WHEN the homepage is accessed
    AND the user clicks on the event with the id="1"
    THEN a page with the title "Rome" should be displayed
    AND the page should contain an element with the id "highlights" should be displayed and contain a text value "First Games"
    """
    chrome_driver.get("http://127.0.0.1:5000/")
    # Wait until the element with id="1" is on the page  https://www.selenium.dev/documentation/webdriver/waits/ and then click on it
    el_1 = WebDriverWait(chrome_driver, timeout=3).until(
        lambda d: d.find_element(By.ID, "1")
    )
    el_1.click()
    # Find the text value of the event highlights
    text = chrome_driver.find_element(By.ID, "highlights").text
    assert "First Games" in text


def test_home_nav_link_returns_home(chrome_driver, run_app):
    """
    GIVEN a running app
    WHEN the homepage is accessed
    AND then the user clicks on the event with the id="1"
    AND then the user clicks on the navbar in the 'Home' link
    THEN the page url should be "http://127.0.0.1:5000/"
    """
    chrome_driver.get("http://127.0.0.1:5000/")
    # Wait until the element with id="1" is on the page  https://www.selenium.dev/documentation/webdriver/waits/ and then click on it
    el_1 = WebDriverWait(chrome_driver, timeout=3).until(
        lambda d: d.find_element(By.ID, "1")
    )
    el_1.click()
    nav_home = el_1 = WebDriverWait(chrome_driver, timeout=3).until(
        lambda d: d.find_element(By.ID, "nav-home")
    )
    nav_home.click()
    url = chrome_driver.current_url
    assert url == "http://127.0.0.1:5000/"
