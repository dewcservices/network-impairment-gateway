import asyncio
import json

import psutil
from fastapi import WebSocket, WebSocketDisconnect

# async def websocket_endpoint(websocket: WebSocket):
#     await websocket.accept()
#     previous_stats = psutil.net_io_counters()
#     skip = True

#     while True:
#         await asyncio.sleep(1)
#         current_stats = psutil.net_io_counters()
#         rx_per_sec = current_stats.bytes_recv - previous_stats.bytes_recv
#         tx_per_sec = current_stats.bytes_sent - previous_stats.bytes_sent

#         previous_stats = current_stats

#         data = {"rx": rx_per_sec, "tx": tx_per_sec}

#         if skip:
#             skip = False
#             continue

#         await websocket.send_json(data=data)


async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    previous_stats = psutil.net_io_counters(pernic=True).get("eth0", None)

    # Check if 'eth0' exists
    if previous_stats is None:
        await websocket.send_json({"error": "eth0 interface not found"})
        await websocket.close()
        return

    monitoring_interval = 1  # Monitor every 1 second

    try:
        while True:
            await asyncio.sleep(monitoring_interval)
            current_stats = psutil.net_io_counters(pernic=True).get("eth0", None)

            if current_stats:
                # Calculate per-second changes
                data = {
                    "bytes_recv_per_sec": current_stats.bytes_recv
                    - previous_stats.bytes_recv,
                    "bytes_sent_per_sec": current_stats.bytes_sent
                    - previous_stats.bytes_sent,
                    "packets_recv_per_sec": current_stats.packets_recv
                    - previous_stats.packets_recv,
                    "packets_sent_per_sec": current_stats.packets_sent
                    - previous_stats.packets_sent,
                    "errors_rx_per_sec": current_stats.errin - previous_stats.errin,
                    "errors_tx_per_sec": current_stats.errout - previous_stats.errout,
                    "dropped_rx_per_sec": current_stats.dropin - previous_stats.dropin,
                    "dropped_tx_per_sec": current_stats.dropout
                    - previous_stats.dropout,
                }

                # Update previous stats
                previous_stats = current_stats

                # Send data to WebSocket client
                await websocket.send_json(data=data)

    except WebSocketDisconnect:
        print("Client disconnected from WebSocket")
    except Exception as e:
        print(f"An error occurred: {e}")


async def stats_websocket(websocket):
    while True:
        stats = await get_interface_stats()
        await websocket.send_json(json.dumps(stats))
        await asyncio.sleep(1)  # Adjust the frequency as needed


async def get_interface_stats():
    # Gather stats for eth0 and eth1
    net_io = psutil.net_io_counters(pernic=True)
    eth0_stats = net_io.get("eth0", None)
    eth1_stats = net_io.get("eth1", None)

    if eth0_stats and eth1_stats:
        # Prepare stats in a JSON-friendly format
        return {
            "eth0": {
                "bytes_sent": eth0_stats.bytes_sent,
                "bytes_recv": eth0_stats.bytes_recv,
                "packets_sent": eth0_stats.packets_sent,
                "packets_recv": eth0_stats.packets_recv,
            },
            "eth1": {
                "bytes_sent": eth1_stats.bytes_sent,
                "bytes_recv": eth1_stats.bytes_recv,
                "packets_sent": eth1_stats.packets_sent,
                "packets_recv": eth1_stats.packets_recv,
            },
        }
    else:
        return {"error": "Interfaces eth0 or eth1 not found"}
