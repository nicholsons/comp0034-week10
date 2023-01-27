from paralympic_app.models import Region


def test_create_new_region():
    """
    GIVEN json data for a region
    WHEN a new Region object is created
    THEN check the fields are defined correctly
    """
    r = Region(
        NOC="NEW", region="New Region", notes="Some notes about the new region"
    )
    assert r.NOC == "NEW"
    assert r.region == "New Region"
    assert r.notes == "Some notes about the new region"
