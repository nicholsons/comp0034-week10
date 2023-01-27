import pytest
import multiprocessing


@pytest.fixture(scope="session")
def init_multiprocessing():
    """Sets multiprocessing to fork once per session

    Needed in Python 3.8 and later
    """
    # get the current start method
    method = multiprocessing.get_start_method()
    if method != "fork":
        multiprocessing.set_start_method("fork")
