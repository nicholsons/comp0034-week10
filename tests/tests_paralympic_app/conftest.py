import multiprocessing
import pytest
from selenium.webdriver.chrome.options import Options
from selenium.webdriver import Chrome
from paralympic_app import create_app
from paralympic_app.models import Region


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


@pytest.fixture(scope="function")
def test_client(app):
    """Create a Flask test client"""
    with app.test_client() as test_client:
        with app.app_context():
            yield test_client


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


@pytest.fixture(scope="module")
def run_app(app, init_multiprocessing):
    """
    Fixture to run the Flask app for Selenium tests
    """
    process = multiprocessing.Process(target=app.run, args=())
    process.start()
    yield process
    process.terminate()


@pytest.fixture(scope="module")
def region_json():
    """Creates a new region JSON for tests"""
    reg_json = {
        "NOC": "NEW",
        "region": "New Region",
        "notes": "Some notes about the new region",
    }
    return reg_json


@pytest.fixture(scope="module")
def region():
    """Creates a new region object for tests"""
    new_region = Region(
        NOC="NEW", region="New Region", notes="Some notes about the new region"
    )
    return new_region
