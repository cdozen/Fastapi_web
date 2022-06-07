# Tracker DCS Web Server 

Input from outside, e.g. LabView

## Developer instructions

Local installation: 

```
conda create -n web_server python=3.9
conda activate web_server
pip install --upgrade pip
pip install -r requirements/local.txt
pip install -e .  
```

## Environment variables 

These secrets will be printed out by the server. 
They are not used for authentication, so set them to whatever you want. 

* `APP_USER`: app user
* `APP_PASSWORD`: app password

This shows how we can use environment variables in the configuration 
of the web server. 

## Running locally

```
python web_server/app.py

```

## Running locally with mqtt

```
python web_server/app_mqtt.py

```

Visit the API docs page to try the endpoints:
[http://localhost:5000/docs](http://localhost:5000/docs)

The root endpoint will print the secrets you have set. 

You can also try the other endpoints. 

## Running in docker

See the docker-compose stack, the web_server is already integrated. 

```
docker compose -f docker-compose.yml -f docker-compose.dev.yml -f up -d

```

Check the running services: 

```
docker compose ps 

```

This should give something like:

``` 
NAME                       COMMAND                  SERVICE             STATUS              PORTS
fastapi_web-mosquitto-1    "/docker-entrypoint.…"   mosquitto           running             0.0.0.0:1883->1883/tcp
fastapi_web-web_server-1   "uvicorn web_server.…"   web_server          running             0.0.0.0:8001->8000/tcp

``` 

To make a request to the root path: 

```commandline
curl localhost:8001/
```

To make a basic POST request using curl, type the following command on your command-line:

```
curl -X 'POST' 'http://localhost:8001/data' -H 'accept: application/json' -H 'Content-Type: application/json' -d '{"data":[0,1,2,5]}'

```

## Communicating with the MQTT service

To listen to all mqtt messages, run this command: 

```
docker exec fastapi_web-mosquitto-1  mosquitto_sub -t /# -v

```

```
/test_mqtt/ ~ Hello from Fastapi ~ Sensordata = [0.0, 1.0, 2.0, 3.0]
/test_mqtt/ ~ Hello from Fastapi ~ Sensordata = [0.0, 1.0, 2.0, 5.0]
```



