# Flask HTTP error handling with custom messages

To improve the experience for your users, Flask provides a way for you to [customise errors](https://flask.palletsprojects.com/en/2.2.x/errorhandling/#error-handlers) using either `@app.errorhandler` decoration; or `app.register_error_handler()`.

Note for those using Blueprints. Handlers registered on a Blueprint take precedence over those registered globally on the application, assuming a Blueprint is handling the request that raises the exception. A Blueprint cannot handle 404 routing errors because the 404 occurs at the routing level before the Blueprint can be determined.

Some of the common HTTP status codes to consider provding custom messages for are:

- 404 Not Found
- 401 Unauthorised
- 500 Internal Server Error

To create the error you need to:

1. Define the custom error templates
2. Define and register the error handlers on the app

## Define the error templates

Create these as you do for any other template. You could even use a parent/child inheritance and have a base error page that is inherited by the specific error pages.

```jinja
{% extends "layout_errors.html" %}
{% block title %}404 Not Found{% endblock %}
{% block content %}
<h1>Not Found</h1>
<p>What you were looking for is just not there. <a href="{{ url_for('main.index') }}">Go back home</a>.</p>
{% endblock %}
```

Add the templates above to the iris app templates folder.

## Define and register the error handlers on the app

The first method is to define the error handlers as routes. You can do this for a particular blueprint, or you can do it for the whole app.

To define them for the whole app, add them to the create_app() function:

```python
from flask import Flask, render_template


def internal_server_error(e):
    return render_template("500.html"), 500


def page_not_found(e):
    return render_template("404.html"), 404

def create_app():
    app = Flask(__name__)
    # Register error handlers
    app.register_error_handler(500, internal_server_error)
    app.register_error_handler(404, page_not_found)

    return app
```

To define them for a route add them to the routes module after the blueprint is defined.

```python
main_bp = Blueprint("main", __name__)


@main_bp.errorhandler(404)
def page_not_found(error):
    return render_template("404.html"), 404
```

Unless you have completed the Blueprint activity and applied it to the iris app, then add the 404 and 500 error handlers to the `__init__.py` and `create_app()`.

Run the app and request a page that does not exist e.g. <http://127.0.0.1:5000/display_event/99>
