import asyncio

import psutil
from fastapi import WebSocket

from app.main import app


@app.websocket("/ws/network")
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
