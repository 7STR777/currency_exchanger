import pytest
from fastapi.testclient import TestClient
from src.my_app.main import app


@pytest.fixture()
def client():
    return TestClient(app)