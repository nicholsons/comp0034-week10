from paralympic_app import db
from paralympic_app.models import Event
from paralympic_app.schemas import EventSchema


# Marshmallow Schemas
events_schema = EventSchema(many=True)
event_schema = EventSchema()


def get_events():
    """Function to get all events from the database as objects and convert to json.

    NB: This was extracted to a separate function as it is used in multiple places
    """
    all_events = db.session.execute(db.select(Event)).scalars()
    event_json = events_schema.dump(all_events)
    return event_json


def get_event(event_id):
    """Function to get a single event as a json structure"""
    event = db.session.execute(
        db.select(Event).filter_by(event_id=event_id)
    ).one()
    result = events_schema.dump(event)
    return result
