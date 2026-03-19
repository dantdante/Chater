from fastapi import FastAPI, WebSocket, WebSocketDisconnect
import os

app = FastAPI()

clients = []

@app.get("/")
def home():
    return {"status": "chater server running 🔥"}

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    clients.append(websocket)
    print("client connected")

    try:
        while True:
            data = await websocket.receive_text()
            print("message:", data)

            for client in clients:
                try:
                    await client.send_text(data)
                except:
                    pass

    except WebSocketDisconnect:
        clients.remove(websocket)
        print("client disconnected")
