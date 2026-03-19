# server.py
import os
import asyncio
import websockets

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

# use asyncio.run instead of get_event_loop()
async def main():
    async with websockets.serve(handler, "0.0.0.0", port):
        await asyncio.Future()  # run forever

asyncio.run(main())
