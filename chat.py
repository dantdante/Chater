import customtkinter as ctk
import threading
import websocket
import time
import certifi

# -------------------------------
# CONFIG
# -------------------------------
ctk.set_appearance_mode("Dark")
ctk.set_default_color_theme("dark-blue")

RENDER_URL = "wss://chater-bfsl.onrender.com/ws"
LOCAL_URL = "ws://127.0.0.1:5555"
USERNAME = input("Enter your username: ")

# -------------------------------
# GLOBALS
# -------------------------------
ws = None
connected = False
current_url = None

# -------------------------------
# GUI SETUP
# -------------------------------
root = ctk.CTk()
root.title("Chater 💬")
root.geometry("450x550")
root.resizable(False, False)

messages_frame = ctk.CTkFrame(root)
messages_frame.pack(pady=10, padx=10, fill="both", expand=True)

msg_list = ctk.CTkTextbox(messages_frame, width=400, height=400, corner_radius=10)
msg_list.pack(padx=5, pady=5, fill="both", expand=True)
msg_list.configure(state="disabled")

entry_field = ctk.CTkEntry(root, width=300, placeholder_text="Type your message...")
entry_field.pack(side="left", padx=(10, 0), pady=(0, 10))

send_button = ctk.CTkButton(root, text="Send")
send_button.pack(side="left", padx=(5, 10), pady=(0, 10))

settings_button = ctk.CTkButton(root, text="Settings")
settings_button.pack(side="bottom", pady=(0, 10))

# -------------------------------
# FUNCTIONS
# -------------------------------
def add_message(msg):
    msg_list.configure(state="normal")
    msg_list.insert("end", msg + "\n")
    msg_list.see("end")
    msg_list.configure(state="disabled")

def connect_to_server(urls=(RENDER_URL, LOCAL_URL)):
    global ws, connected, current_url
    for url in urls:
        try:
            if url.startswith("wss"):
                ws = websocket.WebSocket(sslopt={"cert_reqs": 2, "ca_certs": certifi.where()})
            else:
                ws = websocket.WebSocket()
            ws.connect(url)
            ws.send(USERNAME)
            connected = True
            current_url = url
            add_message(f"Connected to server: {url}")
            threading.Thread(target=receive_messages, daemon=True).start()
            return
        except Exception as e:
            add_message(f"Failed to connect to {url}: {e}")
    connected = False
    add_message("Could not connect to any server.")

def receive_messages():
    global ws, connected
    while connected:
        try:
            msg = ws.recv()
            if msg:
                add_message(msg)
        except:
            connected = False
            add_message("Disconnected. Reconnecting in 5s...")
            time.sleep(5)
            connect_to_server()
            break

def send_message():
    global ws, connected
    msg = entry_field.get()
    if msg and connected:
        try:
            ws.send(f"{USERNAME}: {msg}")
            entry_field.delete(0, "end")
        except:
            add_message("Message failed. Reconnecting...")
            connect_to_server()
    else:
        add_message("Not connected or message empty.")

def open_settings():
    global USERNAME, RENDER_URL, LOCAL_URL, connected, ws
    url = ctk.simpledialog.askstring("Settings", "Render Server URL:", initialvalue=RENDER_URL)
    local = ctk.simpledialog.askstring("Settings", "Local Server URL:", initialvalue=LOCAL_URL)
    name = ctk.simpledialog.askstring("Settings", "Username:", initialvalue=USERNAME)
    if url: RENDER_URL = url
    if local: LOCAL_URL = local
    if name: USERNAME = name
    if connected:
        ws.close()
        connected = False
    connect_to_server((RENDER_URL, LOCAL_URL))

# -------------------------------
# BUTTON EVENTS
# -------------------------------
send_button.configure(command=send_message)
entry_field.bind("<Return>", lambda event: send_message())
settings_button.configure(command=open_settings)

# -------------------------------
# START CLIENT
# -------------------------------
connect_to_server((RENDER_URL, LOCAL_URL))
root.mainloop()
