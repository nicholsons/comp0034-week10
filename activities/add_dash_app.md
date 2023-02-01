# Adding a Dash app to a route in Flask

The [Dash app documentation](https://dash.plotly.com/integrating-dash) offers two solutions for running a Dash app
inside other apps, neither of which is suitable for the COMP0034 coursework. The first requires Dash Enterpise (you
don't have access to this), and the second requires a live hosted Dash app that you access in an iframe. Iframes are
generally discouraged and further you are not permitted to host a version of your app that could be accessed by others (
not allowed under the current UCL CS ethics approvals for data sets in this course).

The following solution is based on the Dash in Flask with Flask-Login solution offered
by[How to embed a Dash app into an existing Flask app](https://medium.com/@olegkomarov_77860/how-to-embed-a-dash-app-into-an-existing-flask-app-ea05d7a2210b)
with the code in [GitHub okomarov](https://github.com/okomarov/dash_on_flask). Feel free to implement any other solution you may find.

He suggests moving the dash directory to within the flask directory. 

```text
/my_project
├── /my_flask_app
│   ├── __init__.py
│   ├── app.py
│   ├── /static
│   ├── /templates
│   └── /my_dash_app
│       └── callbacks.py
│       └── layout.py
├── /data
├── README.md
├── config.py
├── requirements.txt
```

Move the `paralympic_app` package into `my_flask_app`.

## Modify the way the Dash app is created and the layout and callbacks applied

The Dash app callbacks needs to be modified so that the code is created through a functions.
The code to create the dash app object and run the server are moved to the `__init__.py` and `create_app`

The code in `paralympic_app.py` has been split into two files, [layout.py](../example_app/paralympic_app/layout.py) and [callbacks.py](../example_app/paralympic_app/callbacks.py).

New functions have been added to [__init__.py](../example_app/__init__.py) and the `create_app` function:

1. To make sure your Dash callbacks work, if you are using CSRFProtect you need to add a line of code to exempt Dash views:
```python
csrf = CSRFProtect()
csrf._exempt_views.add('dash.dash.dispatch')
```

2. Add two new functions at the end of __init__.py, e.g.
```python
def register_dashapp(app):
    from example_app.paralympic_app import layout
    from example_app.paralympic_app.callbacks import register_callbacks

    meta_viewport = {"name": "viewport", "content": "width=device-width, initial-scale=1, shrink-to-fit=no"}

    dashapp = dash.Dash(__name__,
                         server=app,
                         url_base_pathname='/dashboard/',
                         assets_folder=get_root_path(__name__) + '/dashboard/assets/',
                         meta_tags=[meta_viewport],
                         external_stylesheets=[dbc.themes.SKETCHY])

    with app.app_context():
        dashapp.title = 'Dashboard'
        dashapp.layout = layout.layout
        register_callbacks(dashapp)

    _protect_dash_views(dashapp)


def _protect_dash_views(dash_app):
    for view_func in dash_app.server.view_functions:
        if view_func.startswith(dash_app.config.routes_pathname_prefix):
            dash_app.server.view_functions[view_func] = login_required(dash_app.server.view_functions[view_func])

```

3. Modify the create_app function to register the dash app after the Flask app is configured and before the extensions are initialised, e.g.
```python
def create_app(config_class_name):
    app = Flask(__name__)
    app.config.from_object(config_class_name)

    register_dashapp(app)
```

## Add the Dash route to the navbar
Add the Dash route to the navbar in navbar.html e.g.

```html

<li class="nav-item">
    <a class="nav-link" href="/dashboard/">Dashboard</a>
</li>
```

Run the app with app.py and click on the Dashboard link in the menu to check that it runs.