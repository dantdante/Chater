import os
from fastapi import FastAPI, WebSocket, WebSocketDisconnect
import uvicorn

app = FastAPI()
clients = set()

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    clients.add(websocket)
    try:
        while True:
            msg = await websocket.receive_text()
            # broadcast to everyone except sender
            for client in clients.copy():
                if client != websocket:
                    try:
                        await client.send_text(msg)
                    except:
                        clients.remove(client)
    except WebSocketDisconnect:
        clients.remove(websocket)

@app.get("/")
async def root():
    return {"status": "Chater WebSocket Server Running"}

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5555))  # Render $PORT or local fallback
    uvicorn.run("server:app", host="0.0.0.0", port=port, log_level="info")
