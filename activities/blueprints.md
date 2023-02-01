# Apply a Blueprint to a Flask app

This activity covers another pattern used in Flask apps, [Blueprints](https://flask.palletsprojects.com/en/2.2.x/blueprints/)

## What is a Blueprint?

> "Flask uses a concept of blueprints for making application components and supporting common patterns within an application or across applications. Blueprints can greatly simplify how large applications work and provide a central means for Flask extensions to register operations on applications. A Blueprint object works similarly to a Flask application object, but it is not actually an application. Rather it is a blueprint of how to construct or extend an application."

A Flask blueprint is a way to organize a flask application into smaller and re-usable components.

A blueprint defines a collection of views, templates and static assets.

If you write your blueprint in a separate Python package, then you have a component that encapsulates the elements related to a specific feature of the application.

Unlike a Flask application, a Blueprint cannot be run on its own, it can only be registered on an app.

For example, imagine you wanted to create your app, and also expose the data in the database as an API for others. Both components could re-use an authentication package. You could create a blueprint for each of these components (main app, API, authentication) within your app.

To use a Blueprint within the example application, you will carry out the following:

1. Use the flask Blueprint class to create the blueprint
2. Import and register the blueprint in the application factory
3. Define routes to associate views with the Blueprint

In practice, you are likely to have several modules that together form your Flask app.

As well as the threee steps above, you could also restructure the code to gives better separation of the code in case of re-use, an example is suggested below.

```
/yourapplication
    /my_app
        __init__.py
        app.py
        /api
            __init__.py
        /main
            __init__.py
        /static
        /templates
```

If you are likely to have several modules that each have different templates, you may also want to add sub-directories to the templates folder for each module. Another structure you may encounter is to define the [templates and static folders within each module](https://blog.miguelgrinberg.com/post/the-flask-mega-tutorial-part-xv-a-better-application-structure). You may need to consider one of these for coursework 2, however for this practice example we will keep all the templates in the same directory.

## Blueprint applied to the paralympic app

This example creates a Blueprint for the routes that are not part of the REST API; and another for the REST API routes.

There are 2 routes, the home page and a route that displays information about each event.

The Blueprint for the REST API routes will be called `api` and the other `main` (as I can't think of an appropriate name!).

Changes have been made to the python code files so that functions that are used by the main and REST API routes are in a separate module called `utilities.py` and the routes for the main and api Blueprints have been separated into api_routes.py and main_routes.py.

### 1. Use the flask Blueprint class to create the blueprint

The [Blueprint API documentation](https://flask.palletsprojects.com/en/1.1.x/api/#flask.Blueprint) lists all the parameters you can define.

A simple way to define a blueprint for the 'main' application might look like the following:

```python
from flask import Blueprint

main_bp = Blueprint('main', __name__)
```

and for the REST API:

```python
from flask import Blueprint

api_bp = Blueprint('api', __name__, url_prefix='/api')
```

The first example creates a blueprint called `main_bp` and defines one route (or view) called `index` within that Blueprint.

`url_prefix` is optional. This provides a path to prepend to all of the blueprint’s URLs, to make them distinct from the rest of the app’s routes.

Add code to the two routes modules in the paralympic app.

### 2. Import and register the blueprints in the application factory

Return to the `flask_app/__init__.py` file and the `create_app()` method.

After creating the Flask app, you need to register the blueprint before you return the Flask app object. You need to add the import within `create_app` to avoid circular imports. The code will look like something like this e.g.:

```python
def create_app(config_class_name):
    app = Flask(__name__)

    # Include the routes from api_routes.py and main_routes.py
    from paralympic_app.api_routes import api_bp
    from paralympic_app.main_routes import main_bp

    app.register_blueprint(main_bp)
    app.register_blueprint(api_bp)

```

Note: if you are using a linter you will have to ignore the warnings that will suggest you move the import to the top of the file.

You also need to delete the earlier code that registered the routes:

```python
# Include the routes from api_routes.py and main_routes.py
    with app.app_context():
        from paralympic_app import api_routes, main_routes
```

### 3. Associate routes with the Blueprints

You wil need to modify the routes to assiociate them with the Blueprint.

You will no longer need `import current_app as app`.

You then change the @route from `app.route` to `bp_main.route` or `bp_api.route` accordingly.

```python
from flask import Blueprint, render_template

main_bp = Blueprint('main', __name__)


@main_bp.route('/')
def index():
    return render_template('index.html')
```

Stop and restart the app and then navigate to: <http://127.0.0.1:5000/>

###  4. Modify references that use Flask `url_for`

If you have any references to routes in your Flask app using url_for you will now need to change these to [include the blueprint name](https://flask.palletsprojects.com/en/2.2.x/blueprints/#building-urls).

The `navbar.html` code in templates uses url_for in lines 4 and 12.

Change these to:

```jinja
<a class="navbar-brand" href="{{ url_for('main.index')}}">Paralympics</a>
<a class="nav-link active" aria-current="page" href="{{ url_for('main.index')}}" id="nav-home">Home</a>
```

You also need to change line 9 in `index.html` e.g.

```jinja
<li><a id="{{ event['event_id'] }}" href="{{ url_for('main.display_event', event_id=event
```

## Further examples

- [Flask documentation on blueprints](https://flask.palletsprojects.com/en/2.2.x/blueprints/#modular-applications-with-blueprints)
- [Miguel Gringerg: Using Blueprints as part of a better application structure](https://blog.miguelgrinberg.com/post/the-flask-mega-tutorial-part-xv-a-better-application-structure)
