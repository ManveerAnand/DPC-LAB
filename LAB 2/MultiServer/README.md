# Multi-Server Architecture (Load Balanced)

### The Concept
What if one server isn't enough? If you have 1 million users, a single machine (even with threading) will crash.
The solution is **Horizontal Scaling**: adding more servers.

To make this work transparently for the user, we introduce a **Load Balancer (LB)**.
*   **The Client** connects to the Load Balancer (thinking it's the server).
*   **The Load Balancer** picks an available **Backend Server** (using an algorithm like "Round Robin").
*   **The Load Balancer** acts as a "bridge," passing data back and forth between the Client and the chosen Backend Server.

### The Implementation

#### 1. The Backend Worker (`backend.py`)
This is a standard server, but it takes command-line arguments to decide which Port to listen on. It also knows its own "ID" so we can see which server replies to us.

```python
# Usage: python backend.py <PORT> <SERVER_ID>
# Example: python backend.py 5001 1
def handle_client(conn, addr, server_id):
    # ... receive msg ...
    # Tag response with Server ID
    reply = f"[Server {server_id}] You said: '{msg}'\n"
    conn.sendall(reply.encode("utf-8"))
```

#### 2. The Load Balancer (`load_balancer.py`)
This script listens on the main port (5000) and forwards traffic to the pool of backends (5001, 5002).

**Key Logic: Round Robin Selection**
```python
BACKEND_SERVERS = [("127.0.0.1", 5001), ("127.0.0.1", 5002)]

def get_next_server(self):
    # Cycles 0 -> 1 -> 0 -> 1 ...
    server = BACKEND_SERVERS[self.current_server_index]
    self.current_server_index = (self.current_server_index + 1) % len(BACKEND_SERVERS)
    return server
```

**Key Logic: Bridging**
When a client connects, the LB connects to a backend. It then creates **two threads** to pipe data in both directions:
1.  Client -> Server
2.  Server -> Client

```python
def bridge(source, target):
    while True:
        data = source.recv(4096)
        # If one side closes, close the other
        if not data: break
        target.sendall(data)

def handle_client(client_sock):
    backend_sock = connect_to_backend()
    threading.Thread(target=bridge, args=(client_sock, backend_sock)).start()
    threading.Thread(target=bridge, args=(backend_sock, client_sock)).start()
```

#### 3. The Client (`client.py`)
To the client, nothing has changed. It still connects to Port 5000. It doesn't know there are multiple servers behind the scenes.

---

### How to Run

You will need 4 separate terminals or command prompts.

1.  **Start Backend 1**: 
    ```bash
    python backend.py 5001 1
    ```

2.  **Start Backend 2**: 
    ```bash
    python backend.py 5002 2
    ```

3.  **Start Load Balancer** (Runs on port 5000):
    ```bash
    python load_balancer.py
    ```

4.  **Run Client** (Connects to port 5000):
    ```bash
    python client.py
    ```

_Run the client multiple times to see the response alternate between "Server 1" and "Server 2"._
