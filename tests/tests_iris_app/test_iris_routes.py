from iris_app.models import User
from iris_app import db


def test_index_success(test_client):
    """
    GIVEN a running Flask app
    WHEN an HTTP GET request is made to '/'
    THEN the status code should be 200
    AND the page should contain the the html <title>Iris Home</title>"
    """
    response = test_client.get("/")
    assert response.status_code == 200
    assert b"<title>Iris Home</title>" in response.data


def test_prediction_when_form_submitted(test_client, app):
    """
    GIVEN a running Flask app
    WHEN an HTTP POST request is made to '/' with form data
    THEN the page should return a prediction result with the test "Predicted Iris type"
    AND the status code should be 200 OK
    """
    form_data = {
        "sepal_length": 5.0,
        "sepal_width": 3.3,
        "petal_length": 1.4,
        "petal_width": 0.2,
    }
    response = test_client.post("/", data=form_data)
    assert response.status_code == 200
    assert b"Predicted Iris type" in response.data


def test_iris_contains_table(test_client):
    """
    GIVEN a running Flask app
    WHEN an HTTP GET request is made to '/iris'
    THEN the page should have a table
    AND the status code should be 200 OK
    """
    response = test_client.get("/iris")
    assert response.status_code == 200
    assert b"<table>" in response.data
    assert b"</table>" in response.data


def test_new_user_created_when_form_submitted(test_client):
    """
    GIVEN a running Flask app
    WHEN an HTTP POST request is made to '/register' with form data
    THEN the page should return a message "You are registered!"
    AND the text of the email should be on the page
    AND the status code should be 200 OK
    """

    form_data = {"email": "joshuany@jamble.com", "password": "birthday"}
    response = test_client.post("/register", data=form_data)
    assert response.status_code == 200
    assert b"You are registered!" in response.data
    assert b"joshuany@jamble.com" in response.data

    # Delete the new user from the database
    # It would be better to handle this with a fixture for the database that includes a finaliser that deletes testing entries from the database
    exists = db.session.execute(
        db.select(User).filter_by(email="joshuany@jamble.com")
    ).scalar()
    if exists:
        db.session.execute(
            db.delete(User).where(User.email == "joshuany@jamble.com")
        )
        db.session.commit()


def test_error_when_register_form_email_format_not_valid(test_client):
    """
    GIVEN a running Flask app
    WHEN an HTTP POST request is made to '/register' with form data where the email is not an email address format
    THEN the page should return a message "This field is required."
    AND the status code should be 200 OK
    """
    form_data = {"username": "james", "password": "secret"}
    response = test_client.post("/register", data=form_data)
    assert response.status_code == 200
    assert "This field is required." in response.data.decode()
