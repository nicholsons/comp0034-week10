# Further information for students with a multi-page Dash app

The purpose of a multi-page Dash app is to support URL routing in Dash ( see URL routing and multiple apps). Flask
handles URL routing differently.

Rather than try to fit a multi-page Dash app into Flask, consider adding each Dash app into Flask and let Flask handle
the routing.

The Dash documentation recommends using iFrames (see Embed your Dash app in other websites), however this assumes you
have a live server (which you don't) and are using the Dash enterprise middleware (which you aren't).

A further complexity for the coursework may arise if you wish to protect a Dash app using Flask-Login.

The following attempts to outline one solution to both of the above i.e. to running a number of Dash apps from within
Flask and protecting the routes using Flask-Login.

Note: There will be other solutions for integrating Dash apps in Flask, however you will need to research to find these
yourself.

Useful information can be found here:

- https://github.com/plotly/dash/issues/214
- https://stackoverflow.com/questions/57873247/how-to-combine-dash-and-flask-login-without-using-iframe
- https://github.com/plotly/dash/pull/138
- https://github.com/okomarov/dash_on_flask

## Changes to the Dash apps

The following suggested structure turns a Dash app into a class, though you could just create functions if that is your
preferred style of coding.

The general structure of each class is:

```python
class DashAppName:
    def __init__(self, flask_server):
        self.app = Dash(name=self.__class__.__name__, routes_pathname_prefix='/dash_app_name/',
                        suppress_callback_exceptions=True, server=flask_server, external_stylesheets=[dbc.themes.LUX],
                        meta_tags=[{
                            'name': 'viewport',
                            'content': 'width=device-width, initial-scale=1.0'
                        }])

        def setup(self):
            self.setup_layout()
            self.setup_callbacks()

        def setup_layout(self):
            self.app.layout = html.Div([
                # layout code
            ])

        def setup_callbacks(self):
            @self.app.callback(Output('some_id', 'children'), [Input('some_id', 'value')])
            def display_value(value):
                return '{}'.format(value)

```

### Changes to the Flask app code

Consider adapting factory functions in `__init__.py` using the
example: [Dash on flask with flask_login](https://github.com/okomarov/dash_on_flask). This improves code readability.

```python
def create_app(config_classname):
    app = Flask(__name__)
    app.config.from_object(config_classname)

    register_dash_apps(app)
    register_extensions(app)
    register_blueprints(app)

    return app
```

The `register_extensions` function registers flask_login, sqlalchemy, csrf and configure uploads and also creates the
initial database.

The `register_blueprints` function contains the code to register the blueprints.

The example below of `register_dash_apps` which creates and registers two dash apps. There is then a further
method `_protect_dash_views(dash_app)` which protects the Dash app using Flask Login.

```python
def register_dash_apps(app):
    with app.app_context():
        from dash_apps.app1 import DashApp1
        from dash_apps.app2 import DashApp2

        dash_app1 = DashApp1(app)
        dash_app1.setup()
        _protect_dash_views(dash_app1.app)

        dash_app2 = DashApp2(app)
        dash_app2.setup()


def _protect_dash_views(dash_app):
    for view_func in dash_app.server.view_functions:
        if view_func.startswith(dash_app.config.routes_pathname_prefix):
            dash_app.server.view_functions[view_func] = login_required(dash_app.server.view_functions[view_func])
```

In `routes.py` added routes for the dash apps so that you could use the `url_for` in the nav bar. If you use the urls in
the nav e.g. /dash_app2/ then you don't need to have any route definitions in routes.py since the
routes_pathname_prefix='...', defines the URL.

In this version there are routes for the dash apps that redirects to the dash URL that is defined in the constructor for
the app class, e.g.

```python
@main_bp.route('/dash_app1')
def dash_app1():
    return redirect('/dash_app1/')


@main_bp.route('/dash_app2')
def dash_app2():
    return redirect('/dash_app2/')
```

In the navigation bar html template add the routes for the Dash apps e.g.:

```jinja
<li class="nav-item dropdown">
    <a class="nav-link dropdown-toggle" href="#" id="navbarDropdown" role="button"
       data-bs-toggle="dropdown" aria-expanded="false">Dash apps</a>
    <ul class="dropdown-menu" aria-labelledby="navbarDropdown">
        <li><a class="dropdown-item" href="{{ url_for(" main.dash_app1") }}">Dash app 1</a></li>
        <li><a class="dropdown-item" href="{{ url_for(" main.dash_app2") }}">Dash app 2</a></li>
    </ul>
</li>
```
