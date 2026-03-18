import socket
import threading
import os

# -------------------------------
# CONFIG
# -------------------------------
# listen on all interfaces
HOST = "0.0.0.0"
# use Render's PORT if it exists, otherwise default to 5555 for local testing
PORT = int(os.environ.get("PORT", 5555))

# -------------------------------
# SERVER SETUP
# -------------------------------
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((HOST, PORT))
server.listen()

clients = []
usernames = []

print(f"Server running on {HOST}:{PORT}")

# -------------------------------
# BROADCAST FUNCTION
# -------------------------------
def broadcast(message):
    for client in clients:
        try:
            client.send(message)
        except:
            # remove client if sending fails
            if client in clients:
                index = clients.index(client)
                clients.remove(client)
                usernames.pop(index)

# -------------------------------
# HANDLE SINGLE CLIENT
# -------------------------------
def handle(client):
    while True:
        try:
            msg = client.recv(1024)
            broadcast(msg)
        except:
            if client in clients:
                index = clients.index(client)
                username = usernames[index]
                clients.remove(client)
                usernames.pop(index)
                broadcast(f"{username} has left the chat.".encode())
            client.close()
            break

# -------------------------------
# ACCEPT CONNECTIONS
# -------------------------------
def receive_connections():
    while True:
        client, addr = server.accept()
        print(f"{addr} connected")

        # request username from client
        client.send("USERNAME".encode())
        username = client.recv(1024).decode()

        usernames.append(username)
        clients.append(client)

        broadcast(f"{username} joined the chat!".encode())
        client.send("Connected to the server!".encode())

        # start thread to handle this client
        thread = threading.Thread(target=handle, args=(client,))
        thread.start()

# -------------------------------
# START SERVER
# -------------------------------
receive_connections()
