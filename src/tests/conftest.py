import pytest
from fastapi.testclient import TestClient
from src.my_app.main import app
from src.database import get_db_connection


@pytest.fixture()
def client():
    return TestClient(app)
