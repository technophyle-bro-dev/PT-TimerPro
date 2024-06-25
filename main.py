import os

import uvicorn
from fastapi import FastAPI
from TimerPro.routers import time_track
from sockets import socket_app

app = FastAPI()

# Configure CORS
origins = [
    "*",
]
app.include_router(time_track.router)
app.mount("/", socket_app)


@app.get("/")
def read_root():
    return {"Hello": "World"}


if __name__ == "__main__":
    uvicorn.run("main:app", host=os.environ.get('FASTAPI_HOST'), port=int(os.environ.get('FASTAPI_PORT')), lifespan="on", reload=True)
