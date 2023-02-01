from paralympic_app.models import Region
from paralympic_app.schemas import RegionSchema
from paralympic_app import db


# -------
# Schemas
# -----
regions_schema = RegionSchema(many=True)
region_schema = RegionSchema()


def test_index(test_client):
    """
    GIVEN a running Flask app
    WHEN an HTTP GET request is made to '/'
    THEN the status code should be 200, and the page should contain the text "Barcelona 1992"
    """
    response = test_client.get("/")
    assert response.status_code == 200
    assert b"Barcelona 1992" in response.data


def test_get_all_regions(test_client):
    """
    GIVEN a running Flask app
    WHEN an HTTP GET request is made to '/noc'
    THEN the status code should be 200, the code 'AFG' should be in the response data and the content type "application/json"
    """
    response = test_client.get("/noc")
    assert response.status_code == 200
    assert b"AFG" in response.data
    assert response.content_type == "application/json"


def test_add_region(test_client, region, region_json):
    """
    GIVEN a Region model
    WHEN the HTTP POST request is made to /noc
    THEN a new region should be inserted in the database so there is 1 more row; and the response returned with the new region in JSON format
    """
    # Check if the region exists, it does then delete it
    exists = db.session.execute(
        db.select(Region).filter_by(NOC=region.NOC)
    ).scalar()
    if exists:
        db.session.execute(db.delete(Region).where(Region.NOC == region.NOC))
        db.session.commit()

    # Count() is not well explained in the documentation, try https://github.com/sqlalchemy/sqlalchemy/issues/5908
    # Count the number of regions before adding a new one
    num_regions_in_db = db.session.scalar(
        db.select(db.func.count()).select_from(Region)
    )
    # Add a new region
    response = test_client.post("/noc", json=region_json)
    # Count the number of regions after the new region is added
    num_regions_in_db_after = db.session.scalar(
        db.select(db.func.count()).select_from(Region)
    )
    data = response.json
    assert response.status_code == 201
    assert "NEW" in data["NOC"]
    assert (num_regions_in_db_after - num_regions_in_db) == 1


def test_get_specific_region(test_client):
    """
    GIVEN a running Flask app
    WHEN the "/noc/<code>" route is requested with the GBR code
    THEN the response should contain the region UK
    """
    response = test_client.get("/noc/GBR")
    assert response.status_code == 200

    noc_json = response.json
    assert noc_json["region"] == "UK"


def test_delete_region(test_client):
    """
    GIVEN a region json AND the Region is in the database
    WHEN the DELETE "/noc/<code>" route is called
    THEN check the fields are defined correctly
    """
    # Add a new region to the database if it doesn't already exist
    region = Region(NOC="ZZZ", region="ZeeeZeeeZeee", notes="Zed notes")

    # Check if the region exists, it does then delete it
    exists = db.session.execute(
        db.select(Region).filter_by(NOC=region.NOC)
    ).scalar()

    if not exists:
        db.session.add(region)
        db.session.commit()

    url = f"/noc/{region.NOC}"
    response = test_client.delete(url)
    assert b'"Successfully deleted":"ZZZ"' in response.data
