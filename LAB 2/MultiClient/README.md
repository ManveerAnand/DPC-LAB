# Single Server, Many Clients (Threaded)

### The Concept
In a basic client-server model, if a server operates in a single loop, it can only talk to one client at a time. To handle multiple users simultaneously (like a chat room or web server), we use **Threading**.

*   **The Server** sits in an infinite loop listening for connections.
*   When a **Client** connects, the Server spawns a new **Thread** just for that client.
*   The main server loop goes back to listening for the next person immediately.

### The Implementation

#### 1. Server (`server.py`)
The server uses `threading.Thread` to give each client its own independent `handle_client` function.

```python
import socket
import threading
from datetime import datetime

HOST = "127.0.0.1"
PORT = 5000

def handle_client(conn, addr):
    # This runs in its own thread
    print(f"[+] Connected: {addr}")
    with conn:
        while True:
            data = conn.recv(1024)
            if not data: break
            # Process message and reply
            msg = data.decode("utf-8").strip()
            reply = f"[{datetime.now()}] Server got '{msg}'\n"
            conn.sendall(reply.encode("utf-8"))
    print(f"[-] Disconnected: {addr}")

def main():
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind((HOST, PORT))
    s.listen()
    print(f"Server listening on {HOST}:{PORT}")
    
    while True:
        conn, addr = s.accept()
        # SPAWN A NEW THREAD HERE
        threading.Thread(target=handle_client, args=(conn, addr), daemon=True).start()

if __name__ == "__main__":
    main()
```

#### 2. Stress Test Client (`stress_client.py`)
This script simulates heavy load by creating 20 threads, each pretending to be a different client connecting at roughly the same time.

```python
# ... (imports)
def one_client(cid: int):
    # Connect, send "Hello", print reply, disconnect
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((HOST, PORT))
        # ... send and receive logic ...

def main():
    N = 20
    threads = []
    for i in range(N):
        t = threading.Thread(target=one_client, args=(i,))
        t.start()
        threads.append(t)
    
    # ... join threads ...
```

### How to Run

1.  **Start the Server:**
    ```bash
    python server.py
    ```

2.  **Run clients:**
    *   **Manual:** `python client.py`
    *   **Stress Test:** `python stress_client.py`
