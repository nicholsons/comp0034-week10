from flask import render_template, current_app as app, abort

from paralympic_app.utilities import get_event, get_events


@app.route("/")
def index():
    """Returns the home page"""
    response = get_events()
    return render_template("index.html", event_list=response)


@app.route("/display_event/<event_id>")
def display_event(event_id):
    """Returns the event detail page"""
    ev = get_event(event_id)
    if ev:
        return render_template("event.html", event=ev)
    else:
        abort(404)
