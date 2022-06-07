import pytest
from fastapi.testclient import TestClient
from fastapi import status

user = "candan"
password = "cms"

@pytest.fixture
def app_client(monkeypatch):
    monkeypatch.setenv("APP_USER", user)
    monkeypatch.setenv("APP_PASSWORD", password)
    from web_server.app import app
    client = TestClient(app)
    yield client


def test_root(app_client):
    """Test root endpoint"""
    response = app_client.get("/")
    assert response.status_code == status.HTTP_200_OK
    json = response.json()
    assert json["message"] == "Hello World"
    # assert json["user"] == os.environ["APP_USER"]
    assert json["user"] == user
    assert json["password"] == password

def test_data(app_client):
    the_data = [27., 51, 18.1, 40.]
    response = app_client.post("/data", json={"data": the_data})
    assert response.status_code == status.HTTP_201_CREATED
    assert response.json() == the_data


def test_wrong_data(app_client):
    the_data = [27., 51, 18.1]
    response = app_client.post("/data", json={"data": the_data})
    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY

