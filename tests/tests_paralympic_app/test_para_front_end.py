def test_app_is_running(chrome_driver, run_app):
    """Check the app is running"""
    # Change the url if you configured a different port!
    chrome_driver.get("http://127.0.0.1:5000/")
    assert chrome_driver.title == "Paralympics Home"
