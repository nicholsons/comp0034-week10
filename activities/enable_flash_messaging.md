# Providing user feedback using flash messaging and form errors

## Flash messaging

Flask provides a way to pass messages from one request to the next (and only the next)
using [message flashing](https://flask.palletsprojects.com/en/1.1.x/quickstart/#message-flashing).

This can be useful for highlighting errors or giving other feedback to the user.

This activity adds flash messaging to the Iris app.

### Display flashed messages

Since you may want to do this for any page in an application, you may prefer to enable this in the base template.

Add the following to the `layout.html` jinja template for the Iris app between the navbar and the main content:

```jinja2
    <!-- Flashed messages see https://flask.palletsprojects.com/en/2.2.x/patterns/flashing/ -->
    {% with messages = get_flashed_messages() %}
    {% if messages %}
    <ul class="alert alert-warning">
        {% for message in messages %}
        <li>{{ message }}</li>
        {% endfor %}
    </ul>
    {% endif %}
    {% endwith %}
```

Change the `register` route so that rather than printing `text = f"<p>You are registered! {repr(new_user)}</p>"`, instead you flash a message and then redirect to the `index`:

```python
from flask import flash, redirect, url_for

@app.route("/register", methods=["GET", "POST"])
def register():
    form = UserForm()
    if form.validate_on_submit():
        email = request.form.get("email")
        password = request.form.get("password")
        new_user = User(email=email, password=password)
        db.session.add(new_user)
        db.session.commit()
        # Remove two lines and replace with Flash message code
        # text = f"<p>You are registered! {repr(new_user)}</p>"
        # return text
        text = f"You are registered! {repr(new_user)}"
        flash(text)
        return redirect(url_for("index"))
```

To test it, run the app `python -m flask --app 'iris_app:create_app()' --debug run`, click on Register in the navbar then compete and submit the form.

![homepage screenshot with flash message](/activities/flash-screenshot.png)

## Using the form object's errors attribute

Currently, the registration form returns if it doesn't pass the validation, however if you don't use the `_formhelpers.html` Jinja macro then you probably are not giving any feedback to the user about the errors.

You can access the validation errors of a Flask-WTF form object using `form.errors`.

An example of adding errors:

```jinja2
{# Display the form validation errors #}
    {% for field, errors in form.errors.items() %}
        <div class="alert alert-error">
            {{ form[field].label }}: {{ ', '.join(errors) }}
        </div>
    {% endfor %}
```

This has already been added to the code in [register.html](/iris_app/templates/register.html), have a look to see the syntax.

Note: The Jinja2 template macro `_formhelpers.html` is used to generate forms automatically from fields and add styling. Read the [documentation here](https://flask.palletsprojects.com/en/2.0.x/patterns/wtforms/#forms-in-templates) which contains the necessary code.

You could try and apply this to the register.html code! (not included in the completed code example).
