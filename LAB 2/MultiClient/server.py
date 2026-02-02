import socket
import threading
from datetime import datetime

HOST = "127.0.0.1"  # localhost (single machine)
PORT = 5000


def handle_client(conn, addr):
    print(f"[+] Connected: {addr}")
    with conn:
        while True:
            data = conn.recv(1024)
            if not data:
                break
            msg = data.decode("utf-8", errors="ignore").strip()
            reply = f"[{datetime.now().isoformat(timespec='seconds')}] Server got '{msg}' from {addr}\n"
            conn.sendall(reply.encode("utf-8"))
    print(f"[-] Disconnected: {addr}")


def main():
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM) 
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)  
    s.bind((HOST, PORT))
    s.listen()
    print(f"Server listening on {HOST}:{PORT}")
    while True:
        conn, addr = s.accept()
        threading.Thread(target=handle_client, args=(
            conn, addr), daemon=True).start()


if __name__ == "__main__":
    main()
