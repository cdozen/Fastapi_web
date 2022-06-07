from fastapi import FastAPI, status
import os
from web_server.data import SensorData

app = FastAPI()


@app.get("/")
async def root():
    return {
        "message": "Hello World",
        "user": os.environ["APP_USER"],
        "password": os.environ["APP_PASSWORD"],
    }


@app.post("/data", status_code=status.HTTP_201_CREATED)
async def upload_data(data: SensorData):
    return data.data


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=800, access_log=False, timeout_keep_alive=60)