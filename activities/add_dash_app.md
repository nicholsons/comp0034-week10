# Adding a Dash app to a route in Flask

## Overview

The [Dash app documentation](https://dash.plotly.com/integrating-dash) offers two solutions for running a Dash app inside other apps, neither of which is suitable for the COMP0034 coursework. The first requires Dash Enterpise (you don't have access to this), and the second requires a live hosted Dash app that you access in an iframe. Iframes are generally discouraged and further you are not permitted to host a version of your app that could be accessed by others (not allowed under the current UCL CS ethics approvals for data sets in this course).

The following solution is based on a combination of the solutions offered by:

- [How to embed a Dash app into an existing Flask app](https://medium.com/@olegkomarov_77860/how-to-embed-a-dash-app-into-an-existing-flask-app-ea05d7a2210b)
with the code in [GitHub okomarov](https://github.com/okomarov/dash_on_flask).
- [Video](https://youtu.be/Jr_vfH_XRCI) with code in [GitHub pepgar](https://github.com/pepegar/flask-video-series/)

Both authors suggest placing the dash app code folder inside the Flask app code folder.

The general steps to integrate the dashboard as a route in a Flask app are:

1. Create a function that includes the code to create the Dash app;  add the layout and register the callbacks. The function takes a Flask app as a parameter.
2. Call the new create dash app function in the Flask app `create_app()` function.
3. Add a link to the Dashboard to the navbar in the Flask app.

This activity can be applied to the paralympic app which has the paralympic dash app folder already within it.

### 1. Create a function that creates the Dash app, layout and callbacks

The Dash app is no longer run as a separate server, it needs to be run taking the Flask server as a parameter and then creating the Dash app as a route on this.

Look in [/paralympic_app/paralympic_dash_app/paralympic_dash_app.py](/paralympic_app/paralympic_dash_app/paralympic_dash_app.py) and you should see that the code to create the app; add the layout and the callbacks has been added to a function `def create_dash_app(flask_app):` that takes as a parameter a runnning Flask app.

You will now run the Dash app from within your Flask code which is in the `paralympic_app/__init__.py` file in the `create_app()` function.

### 2. Call the new create dash app function in the Flask app `create_app()` function

Adapt the `create_app()` function in `__init__.py` to call the code that creates the dash app.

```python
create_dash_app(app)
```

Note that the example in: [Dash on flask with flask_login](https://github.com/okomarov/dash_on_flask) separates the `create_app()` code into functions for different aspects (`register_dash_apps(app)`, `register_extensions(app)`,`register_blueprints(app)`). This improves code readability.

```python
def create_app(config_classname):
    app = Flask(__name__)
    app.config.from_object(config_classname)

    register_dash_apps(app)
    register_extensions(app)
    register_blueprints(app)

    return app
```

The `register_extensions` function registers flask_login, sqlalchemy, csrf and also creates the initial database.

### 3. Add the dashboard to the navbar for the Flask app

In the navigation bar html template add the route for the Dash app e.g.:

```jinja
<li class="nav-item dropdown">
    <a class="nav-link dropdown-toggle" href="#" id="navbarDropdown" role="button"
       data-bs-toggle="dropdown" aria-expanded="false">Dash apps</a>
    <ul class="dropdown-menu" aria-labelledby="navbarDropdown">
        <li><a class="dropdown-item" href="/dashboard/">Dashboard</a></li>
    </ul>
</li>
```

## Using CSRFProtect() and Flask-Login

1. If you are using CSRFProtect in your Flask app then you need to add a line of code to exempt Dash views. We have not been adding CSRFProtect in the teaching materials so you may not have it in your code in which case you can skip it. The code you need to add would look like this:

```python
csrf = CSRFProtect()
csrf._exempt_views.add('dash.dash.dispatch')
```

2. If you are using Flask-Login and want to make login required for the Dash app then you need to add an extra function.

```python
from flask_login.utils import login_required

def _protect_dash_views(dash_app):
    """ Allow Dash to be protected by Flask-Login when Dash is integrated with Flask"""
    for view_func in dash_app.server.view_functions:
        if view_func.startswith(dash_app.config.routes_pathname_prefix):
            dash_app.server.view_functions[view_func] = login_required(dash_app.server.view_functions[view_func])

```

You then call this function from the `create_dash_app()` function before you return the app. e.g.

```python
    # ... other code here
   
    _protect_dash_views(dash_app)

    return dash_app
```

The code from Okmarov and Pepe include guidance on protecting a Dash view with Flask-Login.

## Further information

Useful information can be found in the following posts:

- <https://github.com/plotly/dash/issues/214>
- <https://stackoverflow.com/questions/57873247/how-to-combine-dash-and-flask-login-without-using-iframe>
- <https://github.com/plotly/dash/pull/138>
- <https://github.com/okomarov/dash_on_flask>
- <https://youtu.be/Jr_vfH_XRCI> with code in <https://github.com/pepegar/flask-video-series/>

For students with a multi-page Dash app:

The purpose of a multi-page Dash app is to support URL routing in Dash ( see URL routing and multiple apps). Flask handles URL routing differently.

Rather than try to fit a multi-page Dash app into Flask, consider adding each Dash app into Flask and let Flask handle the routing.
