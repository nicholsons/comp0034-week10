def test_create_new_region(new_region):
    """
    GIVEN a Region model
    WHEN a new Region is created
    THEN check the fields are defined correctly
    """
    assert new_region.NOC == "NEW"
    assert new_region.region == "New Region"
    assert new_region.notes == "Some notes about the new region"
