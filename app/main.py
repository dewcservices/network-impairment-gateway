import asyncio

import psutil
import uvicorn
from fastapi import FastAPI, WebSocket
from fastapi.middleware.cors import CORSMiddleware

from app.controllers import (
    bearer_controller,
    environment_controller,
    settings_controller,
)

app = FastAPI()

app.include_router(environment_controller.router)
app.include_router(bearer_controller.router)
app.include_router(settings_controller.router)

origins = ["http://localhost:4200"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.websocket("/ws/network")


async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    previous_stats = psutil.net_io_counters()

    while True:
        await asyncio.sleep(1)
        current_stats = psutil.net_io_counters()
        rx_per_sec = current_stats.bytes_recv - previous_stats.bytes_recv
        tx_per_sec = current_stats.bytes_sent - previous_stats.bytes_sent

        previous_stats = current_stats

        data = {"rx": rx_per_sec, "tx": tx_per_sec}

        await websocket.send_json(data=data)


if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
