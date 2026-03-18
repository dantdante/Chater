# server.py
import os
from fastapi import FastAPI, WebSocket, WebSocketDisconnect
import uvicorn

app = FastAPI()
clients = []

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    clients.append(websocket)
    try:
        while True:
            msg = await websocket.receive_text()
            for client in clients:
                if client != websocket:
                    await client.send_text(msg)
    except WebSocketDisconnect:
        clients.remove(websocket)

@app.get("/")
async def root():
    return {"status": "Chater WebSocket Server Running"}

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5555))  # Render sets $PORT, fallback to 5555 for local
    uvicorn.run("server:app", host="0.0.0.0", port=port, log_level="info")
