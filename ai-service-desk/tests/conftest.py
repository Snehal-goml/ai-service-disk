import httpx
import pytest


BASE_URL = "http://127.0.0.1:8000"


@pytest.fixture
def client():
    """Returns an httpx Client pointed at the running dev server."""
    with httpx.Client(base_url=BASE_URL) as c:
        yield c