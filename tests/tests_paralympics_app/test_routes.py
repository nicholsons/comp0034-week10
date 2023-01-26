import json
from flask import jsonify
from paralympic_app.models import Region
from paralympic_app.schemas import RegionSchema


# -------
# Schemas
# -------

regions_schema = RegionSchema(many=True)
region_schema = RegionSchema()


def test_get_all_regions(client):
    """
    GIVEN a running Flask app
    WHEN an HTTP GET request is made to '/noc'
    THEN the status code should be 200
    """
    response = client.get("/noc")
    print(response)
    assert response.status_code == 200


def test_add_region(new_region, client):
    """
    GIVEN a Region model
    WHEN the HTTP POST request is made to /noc
    THEN a new region should be inserted in the database and the response returned with the new region in JSON format
    """
    response = client.post(
        "/noc",
        data=region_schema.jsonify(new_region),
        content_type="application/json",
    )
    data = json.loads(response.data.decode())
    assert response.status_code == 201
    assert "NEW" in data["NOC"]


def test_delete_region(new_region):
    """
    GIVEN a Region model AND the Region is in the database
    WHEN the
    THEN check the fields are defined correctly
    """
    pass


def test_delete_region(client):
    """
    GIVEN
    WHEN
    THEN
    """
    pass
