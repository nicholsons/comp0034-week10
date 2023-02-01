import multiprocessing
import pytest
from selenium.webdriver.chrome.options import Options
from selenium.webdriver import Chrome
from paralympic_app import create_app
from paralympic_app.models import Region


# Used for Flask route tests and Selenium tests
@pytest.fixture(scope="session")
def app():
    """Create a Flask app configured for testing"""
    app = create_app()
    app.config.update(
        {
            "TESTING": True,
            "SQLALCHEMY_ECHO": True,
            "WTF_CSRF_ENABLED": False,
            "SERVER_NAME": "127.0.0.1:5000",
        }
    )
    yield app


# Used for Flask route tests
@pytest.fixture(scope="function")
def test_client(app):
    """Create a Flask test client"""
    with app.test_client() as testing_client:
        with app.app_context():
            yield testing_client


# Used for Selenium tests
@pytest.fixture(scope="session")
def chrome_driver():
    """Selenium webdriver with options to support running in GitHub actions
    Note:
        For CI: `headless` not commented out
        For running on your computer: `headless` to be commented out
    """
    options = Options()
    # options.add_argument("--headless")
    driver = Chrome(options=options)
    driver.maximize_window()
    yield driver
    driver.quit()


# Used for Selenium tests
@pytest.fixture(scope="session")
def init_multiprocessing():
    """Sets multiprocessing to fork once per session.

    If already set once then on subsequent calls a runtime error will be raised which should be ignored.

    Needed in Python 3.8 and later
    """
    try:
        multiprocessing.set_start_method("fork")
    except RuntimeError:
        pass


# Used for Selenium tests
@pytest.fixture(scope="session")
def run_app(app, init_multiprocessing):
    """
    Fixture to run the Flask app for Selenium tests
    """
    process = multiprocessing.Process(target=app.run, args=())
    process.start()
    yield process
    process.terminate()


# Data for any tests
@pytest.fixture(scope="module")
def region_json():
    """Creates a new region JSON for tests"""
    reg_json = {
        "NOC": "NEW",
        "region": "New Region",
        "notes": "Some notes about the new region",
    }
    return reg_json


# Data for any tests
@pytest.fixture(scope="module")
def region():
    """Creates a new region object for tests"""
    new_region = Region(
        NOC="NEW", region="New Region", notes="Some notes about the new region"
    )
    return new_region
