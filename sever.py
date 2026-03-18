import socket
import threading
import os

# use Render’s port if it exists, otherwise default
HOST = "0.0.0.0"  # listens on all interfaces
PORT = int(os.environ.get("PORT", 5555))  # 5555 for local testing

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((HOST, PORT))
server.listen()

print(f"Server running on {HOST}:{PORT}")
