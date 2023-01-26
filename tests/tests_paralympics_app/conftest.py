import pytest
from paralympic_app import create_app
from paralympic_app.models import Region


@pytest.fixture()
def app():
    """Create and configure Flask app for testing"""

    app = create_app()

    app.config.update(
        {"TESTING": True, "SQLALCHEMY_ECHO": True, "WTF_CSRF_ENABLED": False}
    )
    with app.app_context():
        yield app


@pytest.fixture()
def client(app):
    """Create a Flask test client"""
    return app.test_client()


@pytest.fixture(scope="module")
def new_region():
    """Creates a new region object for tests"""
    region = Region(
        NOC="NEW", region="New Region", notes="Some notes about the new region"
    )
    return region
