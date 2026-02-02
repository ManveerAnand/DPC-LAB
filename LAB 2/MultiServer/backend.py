import socket
import threading
import sys
from datetime import datetime

HOST = "127.0.0.1"


def handle_client(conn, addr, server_id):
    print(f"[Server {server_id}] Connected: {addr}")
    with conn:
        while True:
            try:
                data = conn.recv(1024)
                if not data:
                    break
                msg = data.decode("utf-8", errors="ignore").strip()

                # Tag the response with the Server ID
                reply = f"[{datetime.now().isoformat(timespec='seconds')}][Server {server_id}] You said: '{msg}'\n"
                conn.sendall(reply.encode("utf-8"))
            except ConnectionResetError:
                break
    print(f"[Server {server_id}] Disconnected: {addr}")


def main():
    if len(sys.argv) != 3:
        print("Usage: python backend.py <port> <server_id>")
        sys.exit(1)

    PORT = int(sys.argv[1])
    SERVER_ID = sys.argv[2]

    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

    try:
        s.bind((HOST, PORT))
    except OSError as e:
        print(f"Error binding to port {PORT}: {e}")
        return

    s.listen()
    print(f"Backend Server {SERVER_ID} listening on {HOST}:{PORT}")

    while True:
        try:
            conn, addr = s.accept()
            threading.Thread(target=handle_client, args=(
                conn, addr, SERVER_ID), daemon=True).start()
        except KeyboardInterrupt:
            break


if __name__ == "__main__":
    main()
