import pytest
from selenium.webdriver.chrome.options import Options
from selenium.webdriver import Chrome
from iris_app import create_app


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
            "PRESERVE_CONTEXT_ON_EXCEPTION": False,
        }
    )
    yield app


@pytest.fixture(scope="function")
def test_client(app):
    """Create a Flask test test_client"""
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
def form_data():
    """Data for a prediction.

    Uses: 7.0,3.2,4.7,1.4,versicolor
    """
    form_data = {
        "sepal_length": 7.0,
        "sepal_width": 3.2,
        "petal_length": 4.7,
        "petal_width": 1.4,
    }
    yield form_data