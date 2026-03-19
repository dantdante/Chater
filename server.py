# server.py
import os
import websockets
import asyncio

clients = set()

async def handler(websocket, path):
    clients.add(websocket)
    try:
        async for message in websocket:
            for client in clients.copy():
                if client != websocket:
                    try:
                        await client.send(message)
                    except:
                        clients.remove(client)
    finally:
        clients.remove(websocket)

port = int(os.environ.get("PORT", 5555))
print(f"Chater WebSocket Server running on port {port}")

# expose a "main" coroutine for uvicorn instead of asyncio.run()
async def main():
    return await websockets.serve(handler, "0.0.0.0", port)
