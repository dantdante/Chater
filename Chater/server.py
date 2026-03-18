import socket, threading

HOST = "0.0.0.0"  # Accept connections from anywhere
PORT = 5555

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((HOST, PORT))
server.listen()

clients = []
usernames = []

print(f"Server running on IP: {socket.gethostbyname(socket.gethostname())}, Port: {PORT}")

def broadcast(message):
    for client in clients:
        client.send(message)

def handle(client):
    while True:
        try:
            msg = client.recv(1024)
            broadcast(msg)
        except:
            index = clients.index(client)
            clients.remove(client)
            client.close()
            left_user = usernames[index]
            broadcast(f"{left_user} has left the chat.".encode())
            usernames.pop(index)
            break

def receive_connections():
    while True:
        client, addr = server.accept()
        print(f"{addr} connected")
        
        client.send("USERNAME".encode())
        username = client.recv(1024).decode()
        usernames.append(username)
        clients.append(client)
        
        broadcast(f"{username} joined the chat.".encode())
        threading.Thread(target=handle, args=(client,)).start()

receive_connections()