# Using Flask-Login

## Introduction

According to its [documentation](https://flask-login.readthedocs.io/en/latest/): “Flask-Login provides user session management for Flask. It handles the common tasks of logging in, logging out, and remembering your users’ sessions over extended periods of time. It will:

- Store the active user’s ID in the session, and let you log them in and out easily.
- Let you restrict views to logged-in (or logged-out) users.
- Handle the normally-tricky “remember me” functionality.
- Help protect your users’ sessions from being stolen by cookie thieves.”

Once you have configured Flask-Login and added some required functions and properties, Flask-login provides a route decorator that can be added to routes that require login e.g.

```python
@app.route('/edit_profile')
@login_required
```

When a user attempts to access a `login_required` view without being logged in, Flask-Login will flash a message and redirect them to the log in view. The name of the log in view can be set as `LoginManager.login_view`. If the login view is not set, it will abort with an HTTP 401 Unauthorised error.

### Functions and properties required by Flask-Login

Flask-Login requires the following properties and methods to be implemented:

- `is_authenticated` a property that is `True` if the user has valid credentials or `False` otherwise
- `is_active` a property that is `True` if the user's account is active or `False` otherwise
- `is_anonymous` a property that is `False` for regular users, and `True` for a special, anonymous user
- `get_id()` a method that returns a unique identifier for the user as a string (unicode, if using Python 2)
- `user_loader` used to reload the user object from the user ID stored in the session
- `is_safe_url` and `get_safe_redirect` used to validate the value of the `next` parameter to reduce vulnerability to
  open redirects.

### Optional functions and properties

Flask-Login also provides support for optional functions and properties such as `remember me`  and customising the error messages that are displayed.

## Implement Flask-Login for the iris app

In this activity we will explain the steps to configure and use Flask-Login, and illustrate this by applying them to the `iris_app`.

1. Configure the application to use Flask-Login
2. Add the required helper functions from UserMixin to the User class
3. Add the required user loader function to the routes
4. Add the required helper functions to manage safe redirects to the routes
5. Add templates and routes for login and logout
6. Add login/logout to the navbar

### 1. Configure the application to use Flask-Login

Install Flask-Login e.g. `pip install flask-login`

Go to `app/__init__.py` and review the code. You should see that you are already creating object for CSRFProtect and SQLAlchemy.

```python
db = SQLAlchemy()
```

Add a further object for login manager, e.g.

```python
from flask_login import LoginManager

login_manager = LoginManager()
```

The login manager now needs to be initialised for Flask in the `create_app()` function. Add a line to tell login manager which view to load if the user accesses a protected page and is not logged in (the 'login' route).

```python
def create_app(config_class):
    app = Flask(__name__)
    app.config.from_object(config_class)

    db.init_app(app)
    login_manager.login_view = 'login'
    login_manager.init_app(app)
```

### 2. Add the required helper functions from UserMixin to the User class

To make implementing a user class easier, you can inherit from `UserMixin`, which provides default implementations for the first four of the above properties and methods (`is_authenticated`, `is_active`, `is_anonymous`, `get_id()`). For example, modify the User class like the code below.

**Note:** Make sure the primary key field is called `id` and not anything else or you will find errors with the UserMixin functions when you run your app.

```python
class User(UserMixin, db.Model):
    """Class to represent users who have created a login"""

    __tablename__ = "user"
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.Text, unique=True, nullable=False)
    password = db.Column(db.Text, nullable=False)

    def __init__(self, email: str, password: str):
        """
        Create a new User object hashing the plain text password.
        """
        self.email = email
        self.password = generate_password_hash(password)

    def check_password(self, password):
        """Check the plain text password matches the hashed password

        :return Boolean:
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

### 3. User loader

#### What are sessions?

Before moving to the next step you need to understand what sessions are.

A session is an abstract concept to represent a series of HTTP requests and responses between a specific Web browser and server. HTTP doesn't support the notion of a session, but Python does.

A cookie is a small piece of data stored on the client's computer. A session's data is stored on the server (one session per client). Sessions are often built on top of cookies. A client's browser makes an initial request to the server. The server notes client's IP address/browser, stores some local session data, and sends a session ID back to client. The client stores a cookie holding a unique session ID. On each subsequent page request, the client sends its session ID cookie, and the server uses this to find and retrieve the client's session data.

Sessions in Flask are a way to store information about a specific user from one request to the next. They work by storing a cryptographically signed cookie on the users browser and decoding it on every request. The session object can be treated just like a dictionary that persists across requests, making it an ideal place to store non-sensitive user data. The user could look at the contents of your cookie but not modify it, unless they know the secret key used for
signing.

However, the session object is NOT a secure way to store data. It's a base64 encoded string and can easily be decoded, thus not making it a secure way to save or access sensitive information. An example of decoding the session data is shown at the end of this [tutorial by Julian Nash on pythonise.com](https://pythonise.com/series/learning-flask/flask-session-object).

#### Implement user_loader

You do not have to do anything to establish and use sessions, Flask-Login handles this for you.

You will have to provide a `user_loader` callback function that reloads a user from the session that takes a user ID and returns a user object or None if the user does not exist.

For example, add the following code to `routes.py`:

```python
from iris_app import login_manager


@login_manager.user_loader
def load_user(user_id):
    """Takes a user ID and returns a user object or None if the user does not exist"""
    if user_id is not None:
        user = db.get_or_404(User, user_id)
        return user
    return None
```

### 4. Helper functions to manage safe redirects

Flask-login warns: “You MUST validate the value of the `next` parameter. If you do not, your application will be vulnerable to open redirects.”

We also need a way to implement the redirect back from the successful login to the page the user wanted to access. When a user that is not logged in accesses a view function protected with the `@login_required` decorator, the decorator is going to redirect to the login page, but it is going to include some extra information in this redirect so that the application can then return to the first page. If the user navigates to ’/some_page’ with the `@login_required`
decorator, the decorator will intercept the request and respond with a redirect to '/login'. It will add a query string argument to this URL, making the complete redirect URL '/login?next=/some_page'. The next query string argument is set to the original URL, so the application can use that to redirect back after login.

Any HTTP parameter can be controlled by the user, and could be abused by attackers to redirect a user to a malicious site e.g. in a phishing attack an attacker could redirect a user from a legitimate login form to a fake, attacker controlled, login form. If the page looks enough like the target site, and tricks the user into believing they mistyped their password, the attacker can convince the user to re-enter their credentials and send them to the attacker e.g.
<https://good.com/login?next=http://bad.com/phonylogin>

To counter this type of attack URLs must be validated to ensure they are valid pages within your site before being used to redirect the user.

Fortunately there is a Flask code snippets link on [Flask-Login (Login Example section)](https://flask-login.readthedocs.io/en/latest/#login-example) for a function to validate `next`. If that URL is broken, go to [GitHub flask snippets](https://github.com/fengsp/flask-snippets/blob/master/security/redirect_back.py)
or [Unvalidated URL redirect](https://security.openstack.org/guidelines/dg_avoid-unvalidated-redirects.html) instead.

You will need to add the code for the functions `is_safe_url` and `get_safe_redirect` to your authentication module.

Add the following from [Flask snippets](https://github.com/fengsp/flask-snippets/blob/master/security/redirect_back.py)
to `routes.py`:

```python
from urllib.parse import urlparse, urljoin
from flask import request


def is_safe_url(target):
    host_url = urlparse(request.host_url)
    redirect_url = urlparse(urljoin(request.host_url, target))
    return redirect_url.scheme in ('http', 'https') and host_url.netloc == redirect_url.netloc


def get_safe_redirect():
    url = request.args.get('next')
    if url and is_safe_url(url):
        return url
    url = request.referrer
    if url and is_safe_url(url):
        return url
    return '/'
```

### 5. Add the templates and routes for login and logout to the auth routes

#### Create the login template and form class

Create the Login form class in forms.py. This includes some custom validators to check that the email address and password are correct.

```python
from flask_wtf import FlaskForm
from wtforms import (
    EmailField,
    PasswordField,
    BooleanField,
)
from wtforms.validators import DataRequired, ValidationError
from iris_app.models import User
from iris_app import db

class LoginForm(FlaskForm):
    email = EmailField(label="Email address", validators=[DataRequired()])
    password = PasswordField(label="Password", validators=[DataRequired()])
    remember = BooleanField(label="Remember me")

```

Create the `login.html` template. The form has email, password and a remember me checkbox. The following version uses a Jinja macro to generate the fields.

```jinja
{% extends 'layout.html' %}
{% from "_formhelpers.html" import render_field %}
{% block content %}
<form method=post action="{{ url_for('login') }}">
    {{ form.csrf_token }}
    {{ render_field(form.email, class="form-control") }}
    {{ render_field(form.password, class="form-control") }}
    {{ render_field(form.remember, class="form-check-input") }}
    <p><button type="submit" class="btn btn-primary">Login</button></p>
</form>
{% endblock %}
```

Create `_loginhelpers.html`:

```jinja
{% macro render_field(field) %}
<dt>{{ field.label }}
<dd>{{ field( **kwargs)|safe }}
    {% if field.errors %}
    <ul class=errors>
        {% for error in field.errors %}
        <li>{{ error }}</li>
        {% endfor %}
    </ul>
    {% endif %}
</dd>
{% endmacro %}
```

#### Create the login route

When the login form is submitted and is valid then query the database to find the user. For the query syntax refer to [Flask-SQLAlchemy](https://flask-sqlalchemy.palletsprojects.com/en/3.0.x/queries/#queries-for-views).

You can then use the [Flask-Login `login_user()` function](https://flask-login.readthedocs.io/en/latest/#login-mechanisms) to login the user.

As we have a `remember me` checkbox in the login form then we need to pass additional parameters to login e.g. `login_user(user, remember=form.remember.data, duration=timedelta(minutes=1))`. This is used so that if the user accidentally closes their browser they are not logged out, instead if they re-open the browser within a minute then they will still be logged in.

You then provide function to validate the `next` parameter (i.e. the URL you are going to next). If this isn't safe then the function will abort, otherwise the user will be logged in and redirected to the home page.

Add the following to `routes.py`. This version is longer than the [example in the Flask-Login documentation](https://flask-login.readthedocs.io/en/latest/#login-example). Extra code has been added to handle the case where the email address does not exist or the password is incorrect.

The solution also uses Flask flash messaging to pass the error messages which is documented in a separate activity. You can remove these if you are not using flash messages.

```python
from datetime import timedelta
from flask import abort
from flask_login import login_user
from sqlalchemy.exc import NoResultFound
from iris_app.forms import LoginForm


@app.route("/login", methods=["GET", "POST"])
def login():
    """Login the user if the password and email are valid."""
    login_form = LoginForm()

    if login_form.validate_on_submit():
        try:
            # Query if the user exists. If not raise a NoResultFound error and return to the login form
            user = db.session.execute(
                db.select(User).filter_by(email=login_form.email.data)
            ).scalar_one()

            if user and user.check_password(login_form.password.data):
                # If the user exists and their password is correct, login the user
                login_user(
                    user,
                    remember=login_form.remember.data,
                    duration=timedelta(minutes=1),
                )
                # If they came to login from another page, return them to that page after login, otherwise go to home
                next = request.args.get("next")
                if not is_safe_url(next):
                    return abort(400)
                return redirect(next or url_for("index"))
            else:
                # Message to show if the password was incorrect
                flash("Incorrect password")
        except NoResultFound:
            flash("Email address not found")
    return render_template("login.html", title="Login", form=login_form)
```

#### Create `logout` route

Logout should only occur if a user is logged in, so use the Flask-Login `@login_required` decorator.

Flask-Login provides a `logout_user()` function.

```python
from flask_login import logout_user, login_required


@app.route('/logout')
@login_required
def logout():
    """ Logs out the user and returns them to the home page"""
    logout_user()
    return redirect(url_for('index'))
```

### 6. Add login/logout to the navbar

Modify the navbar so that when the user is not logged in the navbar displays login, whereas once they are logged in it should display logout.

The `is_anonymous` attribute was added to user objects when we inherited the UserMixin class.

The `current_user.is_anonymous` expression will be `True` when the user is not logged in.

We can use this to check which of the options to display in the navbar e.g.

```jinja2
{% if current_user.is_anonymous %}
    <li class="nav-item">
        <a class="nav-link" href="{{ url_for('login') }}">Login</a>
    </li>
    <li class="nav-item">
         <a class="nav-link" href="{{ url_for('register') }}">Register</a>
    </li>
{% else %}
   <li class="nav-item">
       <a class="nav-link" href="{{ url_for('logout') }}">Logout</a>
   </li>
{% endif %}
```

### 7. Try it

Restart the Flask app.

Try out the following:

- Sign up a new user
- Try to login with an incorrect email address (error message should be displayed on the form)
- Try to login with an incorrect password (error message should be displayed on the form)
- Logon with correct details and tick remember me
- Close the browser and reopen within a minute, you should still be logged in (logout shows in the navbar)
- Close the browser and wait longer than a minute, you should be logged out (login shows in the navbar)
- Choose Logout from the navbar, you should be logged out (login shows in the navbar)

You have already used the `@login_required` decorator to the logout function. Add this to any other routes where you want the user to be logged in before they can view it.
