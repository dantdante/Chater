import socket
import threading
import customtkinter as ctk

# ---- Default Server Info ----
HOST = "127.0.0.1"
PORT = 5555
USERNAME = "User"

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# ---- Networking ----
def receive():
    while True:
        try:
            msg = client.recv(1024).decode()
            if msg.startswith("USERNAME"):
                client.send(USERNAME.encode())
            else:
                chat_box.configure(state="normal")
                chat_box.insert("end", msg + "\n")
                chat_box.configure(state="disabled")
                chat_box.yview("end")
        except OSError:
            break

def send():
    if client.fileno() == -1:
        chat_box.configure(state="normal")
        chat_box.insert("end", "[Error] Not connected to server.\n")
        chat_box.configure(state="disabled")
        return

    msg = input_box.get()
    if msg.strip() != "":
        try:
            client.send(f"{USERNAME}: {msg}".encode())
            input_box.delete(0, "end")
        except OSError:
            chat_box.configure(state="normal")
            chat_box.insert("end", "[Error] Failed to send message.\n")
            chat_box.configure(state="disabled")

def connect_to_server():
    global HOST, PORT
    HOST = server_ip_entry.get()
    PORT = int(server_port_entry.get())
    try:
        client.connect((HOST, PORT))
        threading.Thread(target=receive, daemon=True).start()
        settings_window.destroy()
        # Enable input after connecting
        input_box.configure(state="normal")
        send_button.configure(state="normal")
        chat_box.configure(state="normal")
        chat_box.insert("end", f"[Connected to {HOST}:{PORT} as {USERNAME}]\n")
        chat_box.configure(state="disabled")
    except Exception as e:
        chat_box.configure(state="normal")
        chat_box.insert("end", f"[Error] Could not connect: {e}\n")
        chat_box.configure(state="disabled")

# ---- GUI ----
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("dark-blue")

root = ctk.CTk()
root.geometry("450x600")
root.title("Chater v3")

# Chat display
chat_box = ctk.CTkTextbox(root, width=420, height=500, corner_radius=10)
chat_box.pack(pady=10)
chat_box.configure(state="disabled")

# Input + Send (disabled until connected)
input_frame = ctk.CTkFrame(root, width=420, height=40, corner_radius=10)
input_frame.pack(pady=(0,10))

input_box = ctk.CTkEntry(input_frame, width=320, placeholder_text="Type a message...")
input_box.pack(side="left", padx=(10,5))
input_box.configure(state="disabled")

send_button = ctk.CTkButton(input_frame, text="Send", width=80, command=send)
send_button.pack(side="left", padx=5)
send_button.configure(state="disabled")

# Settings menu
def open_settings():
    global settings_window, server_ip_entry, server_port_entry, username_entry
    settings_window = ctk.CTkToplevel(root)
    settings_window.geometry("300x250")
    settings_window.title("Settings")

    ctk.CTkLabel(settings_window, text="Username:").pack(pady=(10,0))
    username_entry = ctk.CTkEntry(settings_window)
    username_entry.insert(0, USERNAME)
    username_entry.pack(pady=5)

    ctk.CTkLabel(settings_window, text="Server IP:").pack(pady=(10,0))
    server_ip_entry = ctk.CTkEntry(settings_window)
    server_ip_entry.insert(0, HOST)
    server_ip_entry.pack(pady=5)

    ctk.CTkLabel(settings_window, text="Server Port:").pack(pady=(10,0))
    server_port_entry = ctk.CTkEntry(settings_window)
    server_port_entry.insert(0, str(PORT))
    server_port_entry.pack(pady=5)

    ctk.CTkButton(settings_window, text="Connect", command=lambda: [set_settings(), connect_to_server()]).pack(pady=15)

def set_settings():
    global USERNAME
    USERNAME = username_entry.get()

ctk.CTkButton(root, text="Settings", command=open_settings).pack()

root.mainloop()
