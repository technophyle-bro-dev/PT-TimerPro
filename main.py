import os

import uvicorn
from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware

from TimerPro.routers import time_track


app = FastAPI()

# Configure CORS
origins = [
    "*",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


app.include_router(time_track.router)


if __name__ == "__main__":
    uvicorn.run("main:app", host=os.environ.get('FASTAPI_HOST'), port=int(os.environ.get('FASTAPI_PORT')), lifespan="on", reload=True)
