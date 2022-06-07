import pytest
import string
import time
import json
from fastapi.testclient import TestClient
from fastapi import status
import paho.mqtt.client as mqtt

user = "candan"
password = "cms"


class device(object):
    name: string
    status: string = "0"


mydevice = device()
mydevice.name = "web_server"
mydevice.status = "0"


def on_connect(client, userdata, flags, rc):
    # Subscribing in on_connect() means that if we lose the connection and
    # reconnect then subscriptions will be renewed.
    client.subscribe(f"/{mydevice.name}/cmd/#")


def on_message(client, userdata, msg):
    print("recv", msg.topic, msg.payload)
    client.device.command(msg.topic, msg.payload)


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
    # assert json["user"] == user
    # assert json["password"] == password
    mqtt_host = "localhost"
    print(mqtt_host)
    client = mqtt.Client()
    client.on_connect = on_connect
    client.connect(mqtt_host, 1883, 60)
    client.loop_start()
    client.publish(
        "/{}/".format(mydevice.name)
        # json.dumps(mydevice.status)
    )
    time.sleep(2)
    client.loop_stop()
    client.disconnect()
    return {
        "message": "Hello World",
        "status": mydevice.status,
        # "user": os.environ["APP_USER"],
        # "password": os.environ["APP_PASSWORD"],
    }


def test_data(app_client):
    the_data = [27.0, 51, 18.1, 40.0]
    response = app_client.post("/data", json={"data": the_data})
    try:
        assert response.status_code == status.HTTP_201_CREATED
        assert response.json() == the_data
        # json = response.json()
        #assert json["message"] == "Hello World"
    except AssertionError as msg:
        print(msg)

    mqtt_host = "localhost"
    print(mqtt_host)
    client = mqtt.Client()
    client.connect(mqtt_host, 1883, 60)
    # mystring = str(data.data)
    mystring = "Hello from FastAPI web_server " + str(the_data)
    client.publish("/mqtt/", mystring)  # publishing mqtt topic
    client.publish("/mqtt", "Hello from Fastapi")  # publishing mqtt topic
    return the_data


def test_wrong_data(app_client):
    the_data = [27.0, 51, 18.1]
    response = app_client.post("/data", json={"data": the_data})
    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
