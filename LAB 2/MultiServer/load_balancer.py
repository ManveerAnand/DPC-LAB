import socket
import threading
import select

# Configuration
LB_HOST = "127.0.0.1"
LB_PORT = 5000

# List of backend servers (IP, Port)
BACKEND_SERVERS = [
    ("127.0.0.1", 5001),
    ("127.0.0.1", 5002)
]


class LoadBalancer:
    def __init__(self):
        self.current_server_index = 0
        self.lock = threading.Lock()

    def get_next_server(self):
        """Round Robin selection of backend server"""
        with self.lock:
            server = BACKEND_SERVERS[self.current_server_index]
            self.current_server_index = (
                self.current_server_index + 1) % len(BACKEND_SERVERS)
        return server

    def bridge(self, source, target, name):
        """Forward data between sockets"""
        try:
            while True:
                data = source.recv(4096)
                if not data:
                    break
                target.sendall(data)
        except Exception:
            pass
        finally:
            try:
                source.close()
            except:
                pass
            try:
                target.close()
            except:
                pass

    def handle_client(self, client_sock, client_addr):
        backend_addr = self.get_next_server()
        print(f"[LB] Forwarding {client_addr} to Backend {backend_addr}")

        try:
            backend_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            backend_sock.connect(backend_addr)

            # Start threads to forward traffic in both directions
            t1 = threading.Thread(target=self.bridge, args=(
                client_sock, backend_sock, "C->S"))
            t2 = threading.Thread(target=self.bridge, args=(
                backend_sock, client_sock, "S->C"))

            t1.daemon = True 
            t2.daemon = True
            t1.start()
            t2.start()

            # We don't join here because bridge closes sockets when done,
            # and we want to return to accept more clients immediately.
            # The threads will die when connection closes.

        except Exception as e:
            print(f"[LB] Failed to connect to backend {backend_addr}: {e}")
            client_sock.close()

    def start(self):
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        s.bind((LB_HOST, LB_PORT))
        s.listen()
        print(f"Load Balancer running on {LB_HOST}:{LB_PORT}")
        print(f"Balancing traffic to: {BACKEND_SERVERS}")

        while True:
            conn, addr = s.accept()
            threading.Thread(target=self.handle_client,
                             args=(conn, addr), daemon=True).start()


if __name__ == "__main__":
    lb = LoadBalancer()
    lb.start()
