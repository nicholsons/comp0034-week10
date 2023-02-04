# JWT

## Overview

Flask-Login uses sessions and cookies. JSON Web Token (JWT) provides an alternate authentication mechanism to sessions. The user’s state is stored inside the token on the client side instead of on the server.
Many web and mobile applications use JWT for authentication, for reasons including scalability (e.g. stored on client not server, can load balance across servers) and device authentication.

JWT works as follows:

- User requests access (e.g. with username / password)
- Server validates credentials
- Server creates a JWT (token) and sends it to the client
- Client stores that token and sends it in all subsequent HTTP requests in the header (until it expires)
- Server verifies the token and responds with data

The structure of a token is defined in [RFC 7519](https://www.rfc-editor.org/rfc/rfc7519); for an easier to read explanation try {Introduction to JWT](https://jwt.io/introduction/). In summary:

There are three parts, the Header, the Payload, and the Signature, separated by dots (.); i.e. Header.Payload.Signature.

- Header: the token type (JWT) and the algorithm used to sign the token
- Payload: the information to be transmitted
- Signature: key that is generated using the algorithm applied to the header and payload

## Implement PyJWT for the paralympics REST API

This activity is applied to the paralympics REST API app.

It uses a python package [PyJWT](https://pypi.org/project/PyJWT/). Other packages exist as alternatives. There are also packages that extend PyJWT specifically for Flask. You can use any package you wish.

This activity uses the following approach to implement PyJWT. There are tutorials that take other approaches; this is not the only way to implement the code.

- Install PyJWT
- Add a User class to models.py
- Add add login route
- Add a function to identify the user from a token
- Secure endpoints (routes) a decorator

### Install JWT

[PyJWT](https://pypi.org/project/PyJWT/)

Install pyJWT e.g. `pip install PyJWT`

### Add a user class to models.py

Add a User class to `model.py`. The following is a simple model with only email and password e.g.

```python
class User(db.Model):
    """User model for use with login"""

    __tablename__ = "user"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    email = db.Column(db.String(255), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)

    def __init__(self, email, password):
        self.email = email
        self.password = generate_password_hash(password)

    def check_password(self, password):
        """Checks the text matches the hashed password.

        :return: Boolean
        """
        return check_password_hash(self.password, password)

    def __repr__(self):
        """
        Returns the attributes of a User as a string, except for the password
        :returns str
        """
        clsname = self.__class__.__name__
        return f"{clsname}: <{self.id}, {self.email}>"
```

You need to to modify the `create_app()` function in `__init__.py` to create the User table in the database.

Add the following AFTER the code that initialises the app for the database.

```python
# Creates the User table in the database
    with app.app_context():
        from paralympic_app.models import User

        db.create_all()
```

Ignore the linter warning that the import is not used.

### Add routes to register and login a user

Unlike the Flask-Login version that creates forms on pages, for the REST API the routes use JSON only.

Add the following to the `routes.py` (or `api_routes.py` if you created Blueprints).

```python
from datetime import datetime, timedelta
import jwt
from functools import wraps
from flask import (
    request,
    make_response,
    jsonify,
    Blueprint,
    current_app as app,
)
from paralympic_app.models import User

@api_bp.route("/register", methods=["GET", "POST"])
def register():
    """Register a new user for the REST API"""
    # Get the JSON data from the request
    post_data = request.get_json()
    # Check if user already exists, returns None if the user does not exist
    user = db.session.execute(
        db.select(User).filter_by(email=post_data.get("email"))
    ).scalar_one_or_none()
    if not user:
        try:
            user = User(
                email=post_data.get("email"),
                password=post_data.get("password"),
            )
            # Add user to the database
            db.session.add(user)
            db.session.commit()
            # Return success message
            response = {
                "status": "success",
                "message": "Successfully registered.",
            }
            return make_response(jsonify(response)), 201
        except Exception as err:
            response = {
                "status": "fail",
                "message": "An error occurred. Please try again.",
            }
            return make_response(jsonify(response)), 401
    else:
        response = {
            "status": "fail",
            "message": "User already exists. Please Log in.",
        }
        return make_response(jsonify(response)), 202


@api_bp.route("/login", methods=["GET", "POST"])
def login():
    """Login for the REST API"""
    # Get the request JSON data
    data = request.get_json()
    try:
        # Get the user data
        email = data.get("email")
        password = data.get("password")
        user = db.session.execute(
            db.select(User).filter_by(email=email)
        ).scalar_one_or_none()
        if user and user.check_password(password):
            payload = {
                "exp": datetime.utcnow() + timedelta(minutes=5),
                "iat": datetime.utcnow(),
                "sub": user.id,
            }
            auth_token = jwt.encode(
                payload, app.config.get("SECRET_KEY"), algorithm="HS256"
            )
            if auth_token:
                response = {
                    "status": "success",
                    "message": "Successfully logged in.",
                }
                return make_response(jsonify(response)), 200
    except Exception as err:
        print(err)
        response = {"status": "fail", "message": "Try again"}
        return make_response(jsonify(response)), 500
```

### Add a decorator for routes that requires a user to be logged in

You need to define the decorator before using it in a route.

Add this to `routes.py` before the route definitions.

This decodes the token and if it is correct then the user can use the route.

```python
# Custom decorator
def token_required(f):
    """Require valid jwt for a route

    Decorator to protect routes using jwt
    """

    @wraps(f)
    def decorator(*args, **kwargs):
        token = request.headers.get("Authorization")

        if not token:
            response = {"message": "Token invalid"}
            return make_response(response, 401)
        try:
            data = jwt.decode(token, app.config["SECRET_KEY"])
            user = db.session.execute(
                db.select(User).filter_by(email=data.get("email"))
            ).scalar_one_or_none()
        except Exception as err:
            response = {"message": "Token invalid"}
            return make_response(response, 401)
        return f(user, *args, **kwargs)

    return decorator
```

### Secure endpoints using the decorator

Add `@token_required` to one or more routes. For example, users must be registered before they are allowed 'delete' rights.

```python
@api_bp.delete("/noc/<code>")
@token_required
def noc_delete(code):
    """Removes a NOC record from the dataset."""
    region = db.one_or_404(db.select(Region).filter_by(NOC=code))
    db.session.delete(region)
    db.session.commit()
    text = jsonify({"Successfully deleted": region.NOC})
    response = make_response(text, 200)
    response.headers["Content-type"] = "application/json"
    return response
```

### Test the functionality

Run the paralympic app.

You will need to use Postman or similar to register a new user.

Provide JSON in the body of the request e.g.

```json
{
    "email": "test@test.com",
    "password" : "test"
}
```

Screenshot using the week 10 solution code. This version uses a blueprint so you need to prepend the routes with /api e.g. /api/register instead of /register

![Postman screenshot to the register route](/activities/jwt-register.png)

Then try and login using postman:

## Other tutorials

- [Real Python](https://realpython.com/token-based-authentication-with-flask)
- [PrettyPrinted](https://www.youtube.com/watch?v=J5bIPtEbS0Q)
