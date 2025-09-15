import socket
import threading
import socks
from stem import Signal
from stem.control import Controller
from colorama import Fore, Style

# Tor configs
TOR_SOCKS_PORT = 9050
SERVER_HOST = "127.0.0.1"
SERVER_PORT = 24456

# Predefined users (3 users with keys)
USERS = {
    "Udit": "woif1fw2f7", "color": Fore.BLUE,
    "Sanjeev": "letmein", "color": Fore.GREEN,
    "Muthu": "df98s7df98", "color": Fore.RED
}

clients = {}  # {socket: username}

def renew_tor_ip():
    with Controller.from_port(port=9051) as controller:
        controller.authenticate()
        controller.signal(Signal.NEWNYM)

# ---------------- SERVER ---------------- #
def broadcast(message, sender_socket=None):
    """Send message to all clients except the sender."""
    for client, user in clients.items():
        if client != sender_socket:
            try:
                client.sendall(message.encode("utf-8"))
            except:
                client.close()
                del clients[client]

def handle_client(client_socket):
    try:
        # Step 1: Get authentication key
        key = client_socket.recv(1024).decode("utf-8").strip()
        username = None
        for user, ukey in USERS.items():
            if key == ukey:
                username = user
                break

        if not username:
            client_socket.sendall("Invalid key. Connection closed.".encode("utf-8"))
            client_socket.close()
            return

        clients[client_socket] = username
        print(f"{username} joined the chat")
        broadcast(f"{username} has joined the chat.", client_socket)

        # Step 2: Chat loop
        while True:
            msg = client_socket.recv(1024).decode("utf-8")
            if not msg:
                break
            print(f"[{username}] {msg}")
            broadcast(f"[{username}] {msg}", client_socket)

    except ConnectionResetError:
        pass
    finally:
        if client_socket in clients:
            left_user = clients[client_socket]
            print(f"{left_user} left the chat")
            broadcast(f"{left_user} has left the chat.")
            del clients[client_socket]
            client_socket.close()

def start_server():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((SERVER_HOST, SERVER_PORT))
    server_socket.listen(5)
    print(f"Server started on {SERVER_HOST}:{SERVER_PORT}")

    while True:
        client_socket, addr = server_socket.accept()
        threading.Thread(target=handle_client, args=(client_socket,), daemon=True).start()

# ---------------- CLIENT ---------------- #
def receive_messages(client_socket):
    while True:
        try:
            msg = client_socket.recv(1024).decode("utf-8")
            if msg:
                print("\n" + msg)
        except:
            break

def client_mode(target_onion_address):
    client_socket = socks.socksocket()
    client_socket.set_proxy(socks.SOCKS5, "127.0.0.1", TOR_SOCKS_PORT)
    client_socket.connect((target_onion_address, SERVER_PORT))

    # Authenticate
    key = input("Enter your secret key: ").strip()
    client_socket.sendall(key.encode("utf-8"))

    # Start receiving thread
    threading.Thread(target=receive_messages, args=(client_socket,), daemon=True).start()

    # Send messages
    while True:
        msg = input()
        if msg.lower() == "/quit":
            client_socket.close()
            break
        client_socket.sendall(msg.encode("utf-8"))

# ---------------- MAIN ---------------- #
def main():
    mode = input("Start as server or client? (s/c): ").strip().lower()
    if mode == "s":
        print("Starting server mode...")
        start_server()
    elif mode == "c":
        onion_address = input("Enter the .onion address of the server: ").strip()
        print("Connecting to", onion_address)
        client_mode(onion_address)
    else:
        print("Invalid option")

if __name__ == "__main__":
    main()