import os
import asyncio
import websockets

# store connected clients
clients = set()

async def handler(websocket):
    # add client
    clients.add(websocket)
    try:
        async for message in websocket:
            # broadcast to everyone except sender
            for client in clients.copy():
                if client != websocket:
                    try:
                        await client.send(message)
                    except:
                        clients.remove(client)
    finally:
        clients.remove(websocket)

# pick port from Render or default to 5555
port = int(os.environ.get("PORT", 5555))
start_server = websockets.serve(handler, "0.0.0.0", port)

print(f"Chater WebSocket Server running on port {port}")
asyncio.get_event_loop().run_until_complete(start_server)
asyncio.get_event_loop().run_forever()
