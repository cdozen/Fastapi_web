import time
from web_server.data import SensorData
from fastapi import FastAPI, status
import paho.mqtt.client as mqtt

app = FastAPI()

def on_connect(client, userdata, flags, rc):
    # Subscribing in on_connect() means that if we lose the connection and
    # reconnect then subscriptions will be renewed.
    client.subscribe(f'/test/#')
    client.connected = True

def on_message(client, userdata, msg):
    #print(msg.topic + " " + str(msg.payload))
    client = mqtt.Client()
    client.on_connect = on_connect
    client.on_message = on_message
    ret = client.connect("localhost", 1883, 60)
    assert ret == 0

@app.get("/")
async def root():  
    return {
    "message": "Hello World",
    #"user": os.environ["APP_USER"],
    #"password": os.environ["APP_PASSWORD"],
    }

@app.post("/data", status_code=status.HTTP_201_CREATED)
async def upload_data(data: SensorData):
    client = mqtt.Client()
    client.on_connect = on_connect
    client.on_message = on_message
    client.connected = False
    client.connect("localhost", 1883, 60)
    print('MQTT connected! Starting loop...')
    client.loop_start()
    while not client.connected:
        time.sleep(0.001)
    topic = '/test_mqtt/'
    client.subscribe(topic)
    messages = "~ Hello from Fastapi ~ Sensordata = " +  str(data.data)
    client.publish(topic, messages)
    time.sleep(1)
    print(f'publish the data: {data.data}')
    client.loop_stop()
    print('End of the loop...')
    client.disconnect()
    return data.data #response body


#@app.get("/data", status_code=status.HTTP_200_OK)
#async def read_data(data:SensorData):
#    return data.data


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=500, access_log=False, timeout_keep_alive=60)