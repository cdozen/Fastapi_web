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

Visit the API docs page to try the endpoints:
[http://localhost:5000/docs](http://localhost:5000/docs)

The root endpoint will print the secrets you have set. 

You can also try the other endpoints. 

## Running in docker

See the docker-compose stack, the web_server is already integrated. 

To make a request to the root path: 

```commandline
curl localhost:8001/
```





