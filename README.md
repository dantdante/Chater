Chater is a minimal real-time chat app built in Python. it’s got a sleek, tuff GUI, lets you connect to custom servers, and works both locally on your mac or online with a cloud server. perfect for learning python GUI or just chatting with friends.

Features

Minimal, tuff GUI with CustomTkinter

Real-time messaging with custom server connections

Settings menu to set username, server IP, and port

Works locally or online (with websockets / render)

Lightweight and easy to run

Getting started
Prerequisites
    python 3.x installed
    customtkinter library (install with pip install customtkinter)

Running locally
1. Start the server: python3 server.py

2. Start the client: python3 chat.py

3. Open settings in the client to set your username and connect to a server

4. Start chatting! 🗨️

Deployment (online server)

To make chater always online, deploy the server to a cloud platform like Render using a websocket server. Then point your client to the public address of the deployed server.
