import socket
import threading
import sys
import time

HOST = "127.0.0.1"


class ChatNode:
    """
    A peer-to-peer chat node that acts as BOTH client and server.

    Communication Flow (Node A -> Node B):
        1. User types a message in Node A's client module
        2. Client sends it to Node A's OWN relay server (server_port + 1000)
        3. Node A's relay server forwards it to Node B's external server (peer_port)
        4. Node B's external server receives and displays the message

    Each node runs THREE components:
        - External Server (server_port): Receives messages FROM the peer
        - Relay Server (server_port + 1000): Receives from local client, forwards to peer
        - Client Module: Takes user input and sends to own relay server
    """

    def __init__(self, name, server_port, peer_port):
        self.name = name
        self.server_port = server_port          # External: peer connects here
        self.relay_port = server_port + 1000    # Internal: local client connects here
        self.peer_port = peer_port              # Peer's external server port
        self.peer_conn = None                   # Persistent connection to peer's server

    # ─────────────────────────────────────────────────────────
    # COMPONENT 1: External Server (receives messages from peer)
    # ─────────────────────────────────────────────────────────
    def external_server(self):
        """Listens for incoming messages from the peer node."""
        srv = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        srv.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        srv.bind((HOST, self.server_port))
        srv.listen(5)
        print(f"[{self.name}] External server listening on port {self.server_port}")

        while True:
            conn, addr = srv.accept()
            threading.Thread(
                target=self.handle_peer_message,
                args=(conn,),
                daemon=True
            ).start()

    def handle_peer_message(self, conn):
        """Display messages received from peer node."""
        try:
            while True:
                data = conn.recv(1024)
                if not data:
                    break
                msg = data.decode("utf-8", errors="ignore")
                print(f"\n  >> {msg}")
                print(f"[{self.name}] > ", end="", flush=True)
        except Exception:
            pass

    # ─────────────────────────────────────────────────────────
    # COMPONENT 2: Relay Server (local client -> forward to peer)
    # ─────────────────────────────────────────────────────────
    def relay_server(self):
        """Internal server that receives from local client and forwards to peer."""
        srv = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        srv.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        srv.bind((HOST, self.relay_port))
        srv.listen(1)
        print(f"[{self.name}] Relay server listening on port {self.relay_port}")

        while True:
            conn, addr = srv.accept()
            threading.Thread(
                target=self.forward_to_peer,
                args=(conn,),
                daemon=True
            ).start()

    def forward_to_peer(self, conn):
        """Forward messages from local client to peer's external server."""
        try:
            while True:
                data = conn.recv(1024)
                if not data:
                    break
                # Forward the message to the peer's external server
                if self.peer_conn:
                    self.peer_conn.sendall(data)
                    print(
                        f"  [Relay] Forwarded to peer on port {self.peer_port}")
                    print(f"[{self.name}] > ", end="", flush=True)
        except Exception:
            pass

    # ─────────────────────────────────────────────────────────
    # COMPONENT 3: Client Module (user input)
    # ─────────────────────────────────────────────────────────
    def connect_to_peer(self):
        """Establish persistent connection to peer's external server."""
        while True:
            try:
                self.peer_conn = socket.socket(
                    socket.AF_INET, socket.SOCK_STREAM)
                self.peer_conn.connect((HOST, self.peer_port))
                print(
                    f"[{self.name}] Connected to peer's server on port {self.peer_port}")
                return
            except ConnectionRefusedError:
                print(f"[{self.name}] Waiting for peer to come online...")
                time.sleep(2)

    def client_module(self):
        """Client: reads user input and sends to OWN relay server for forwarding."""
        # Connect to own relay server (NOT directly to peer)
        time.sleep(0.5)
        client_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client_sock.connect((HOST, self.relay_port))
        print(
            f"[{self.name}] Client connected to own relay server on port {self.relay_port}")
        print(f"\n{'=' * 50}")
        print(f"  Chat started! Type messages and press Enter.")
        print(f"  Type 'quit' to exit.")
        print(f"{'=' * 50}\n")

        while True:
            try:
                msg = input(f"[{self.name}] > ")
                if not msg:
                    continue
                if msg.lower() == "quit":
                    print("Exiting chat...")
                    break
                # Tag the message with sender name and send to OWN relay server
                tagged_msg = f"[{self.name}]: {msg}"
                client_sock.sendall(tagged_msg.encode("utf-8"))
            except (KeyboardInterrupt, EOFError):
                print("\nExiting chat...")
                break

        client_sock.close()

    # ─────────────────────────────────────────────────────────
    # STARTUP
    # ─────────────────────────────────────────────────────────
    def start(self):
        """Launch all three components of the node."""
        print(f"\n{'=' * 50}")
        print(f"  Starting Chat Node: {self.name}")
        print(f"  External Server Port: {self.server_port}")
        print(f"  Relay Server Port:    {self.relay_port}")
        print(f"  Peer Server Port:     {self.peer_port}")
        print(f"{'=' * 50}\n")

        # 1. Start external server (receives from peer)
        threading.Thread(target=self.external_server, daemon=True).start()

        # 2. Start relay server (receives from local client, forwards to peer)
        threading.Thread(target=self.relay_server, daemon=True).start()

        time.sleep(0.5)

        # 3. Connect to peer's external server
        self.connect_to_peer()

        # 4. Run client module on main thread
        self.client_module()


def main():
    if len(sys.argv) != 4:
        print("Usage: python node.py <node_name> <own_port> <peer_port>")
        print()
        print("Example (run in two separate terminals):")
        print("  Terminal 1: python node.py A 6001 6002")
        print("  Terminal 2: python node.py B 6002 6001")
        sys.exit(1)

    name = sys.argv[1]
    own_port = int(sys.argv[2])
    peer_port = int(sys.argv[3])

    node = ChatNode(name, own_port, peer_port)
    node.start()


if __name__ == "__main__":
    main()
