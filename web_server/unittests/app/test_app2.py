import pytest
import string
import time
import json
import logging
import sys

from fastapi.testclient import TestClient
from fastapi import status
import paho.mqtt.client as mqtt

level = logging.DEBUG
log = logging.getLogger(__name__)
log.setLevel(level)
formatter = logging.Formatter(
    '%(asctime)s %(levelname)s %(module)s | %(message)s')

sh = logging.StreamHandler(sys.stdout)
sh.setFormatter(formatter)
log.addHandler(sh)

fh = logging.FileHandler('log')
fh.setFormatter(formatter)
log.addHandler(fh)


user = "candan"
password = "cms"

#values = []
def on_connect(client, userdata, flags, rc):
    # Subscribing in on_connect() means that if we lose the connection and
    # reconnect then subscriptions will be renewed.
    client.subscribe("/test/#")
    client.connected = True

def on_message(client, userdata, message):
    global messages
    #values.append(int(message.payload))
    print(message.topic + " " + str(message.payload))
    client = mqtt.Client()
    client.on_connect = on_connect
    client.on_message = on_message
    ret = client.connect("localhost", 1883, 60)
    assert ret==0

def test_wait_connect():
    def on_connect(client, userdata, flags, rc):
        # Subscribing in on_connect() means that if we lose the connection and
        # reconnect then subscriptions will be renewed.
        client.subscribe("/test/#")
        client.connected = True

    client = mqtt.Client()
    client.on_connect = on_connect
    client.connected = False
    ret = client.connect("localhost", 1883, 60)
    client.loop_start()
    while not client.connected:
        time.sleep(0.001)
    assert True
    client.disconnect()
    client.loop_stop()

@pytest.fixture
def app_client(monkeypatch):
    monkeypatch.setenv("APP_USER", user)
    monkeypatch.setenv("APP_PASSWORD", password)
    from web_server.app import app
    client = TestClient(app)
    yield client


'''def test_root(app_client):
    """Test root endpoint"""
    response = app_client.get("/")
    assert response.status_code == status.HTTP_200_OK
    json = response.json()
    assert json["message"] == "Hello World"
    #assert json["user"] == os.environ["APP_USER"]
    #assert json["user"] == user
    #assert json["password"] == password
    print('connect mqtt in app')
    client = mqtt.Client()
    client.on_connect = on_connect
    client.on_message = on_message
    client.connected = False
    client.connect("localhost", 1883, 60)
    client.loop_start()
    while not client.connected:
        time.sleep(0.001)
    topic = '/test_mqtt'
    client.subscribe(topic)
    n_messages = 5
    for i in range(n_messages):
        client.publish(topic, i)
        time.sleep(0.01)
        # leave enough time for all messages to arrive
    time.sleep(1)
    client.disconnect()
    client.loop_stop()
    assert values == list(range(n_messages))
'''

def test_data(app_client):
    the_data = [27., 51, 18.1, 40.]
    response = app_client.post("/data", json={"data": the_data})
    #try:
    assert response.status_code == status.HTTP_201_CREATED
    assert response.json() == the_data
        #json = response.json()
        #assert json["message"] == "Hello World"
    #except AssertionError as msg:
    #    print(msg)

    client = mqtt.Client()
    client.on_connect = on_connect
    client.on_message = on_message
    client.connected = False
    client.connect("localhost", 1883, 60)
    log.info('MQTT connected! Starting loop...')
    client.loop_start()
    while not client.connected:
        time.sleep(0.001)
    topic = '/test_mqtt'
    client.subscribe(topic)
    messages = "Hello from Fastapi" + str(the_data)
    client.publish(topic, messages)
    time.sleep(1)
    log.info(f'publish the data: {the_data}' )
    client.loop_stop()
    log.info('End of the loop...')
    client.disconnect()
    return the_data


def test_wrong_data(app_client):
    the_data = [27., 51, 18.1, 40.,33.]
    response = app_client.post("/data", json={"data": the_data})
    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
    client = mqtt.Client()
    client.on_connect = on_connect
    client.on_message = on_message
    client.connected = False
    client.connect("localhost", 1883, 60)
    client.loop_start()
    while not client.connected:
        time.sleep(0.001)
    topic = '/test_mqtt'
    client.subscribe(topic)
    messages = str(the_data)
    client.publish(topic, messages)
    time.sleep(1)
    client.loop_stop()
    client.disconnect()


