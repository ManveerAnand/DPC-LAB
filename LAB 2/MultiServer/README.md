# Multi-Server Architecture (Load Balanced)

### 🧠 The Conceptual Problem (The "McDonald's" Problem)
Threading (Lab 2 Part 1) is great, but it has a limit. Eventually, your CPU runs out of power.
A single computer can only handle so many threads before it melts.

**The Solution: Horizontal Scaling**
Instead of buying a bigger computer (Vertical Scaling), we buy **more cheap computers** (Horizontal Scaling).
But we can't tell users: "Hey, try connecting to Server 1. If it's busy, try Server 2." That's bad UX.

We need a **Load Balancer (LB)**. The LB is the "Manager" at the front counter. You talk to the manager, and the manager hands your order to an available cook (Backend Server).

---

### 🔍 Deep Dive: The Code & Syntax

#### 1. The Traffic Cop (`load_balancer.py`)
This script isn't a normal server. It doesn't process data. It just moves it.

**Round Robin Logic:**
```python
def get_next_server(self):
    with self.lock:  # <--- Why Lock?
        server = BACKEND_SERVERS[self.current_server_index]
        # ... increment index ...
    return server
```
*   **The Problem:** The Round Robin index is a shared variable. If two clients connect at the *exact same nanosecond*, both might read `index=0` and send two requests to Server 1, leaving Server 2 idle.
*   **The Lock (`threading.Lock`):** This forces clients to get in a single-file line just for the split-second it takes to pick a server ID. It guarantees perfect distribution.

#### 2. The Bridge Function (The Magic)
How do we connect Client A to Server B without them knowing?

```python
def bridge(source, target):
    while True:
        data = source.recv(4096)
        if not data: break
        target.sendall(data)
```
This function is a **unidirectional pipe**. It takes bytes from left and pushes to right.
*   The LB spawns **two** of these threads for every single client:
    1.  Thread X: Reading from Client -> Writing to Backend
    2.  Thread Y: Reading from Backend -> Writing to Client
*   This creates a full-duplex transparent interaction.

#### 3. Backend Identity
In `backend.py`, we run:
```bash
python backend.py 5001 1
```
The arguments `5001` and `1` are accessed via `sys.argv`.
*   `sys.argv[0]`: script name (`backend.py`)
*   `sys.argv[1]`: port (`5001`)
*   `sys.argv[2]`: ID (`1`)

This allows us to run the **exact same code** multiple times, just behaving slightly differently (listening on different ports).

---

### 🚀 Architecture Visualization

```text
       [  Client  ]      [  Client  ]
             \                /
              \              /
           [ LOAD BALANCER (Port 5000) ]
           /              \
          / (Forwarding)   \ (Forwarding)
         /                  \
[ Backend 1 (5001) ]    [ Backend 2 (5002) ]
```

1.  Client connects to LB (5000).
2.  LB creates a specialized socket for Backend 1 (5001).
3.  LB glues the two sockets together.
4.  Client thinks it's talking to LB, but LB is just mouthing the words from Backend 1.

---

## How to Run (Requires 4 Terminals)

**Terminal 1 - Start Backend Server 1:**
```bash
python "LAB 2/MultiServer/backend.py" 5001 1
```

**Terminal 2 - Start Backend Server 2:**
```bash
python "LAB 2/MultiServer/backend.py" 5002 2
```

**Terminal 3 - Start Load Balancer:**
```bash
python "LAB 2/MultiServer/load_balancer.py"
```
The Load Balancer listens on Port 5000 and forwards traffic to backends.

**Terminal 4 - Run Client:**
```bash
python "LAB 2/MultiServer/client.py"
```
Type messages. Notice the response will show `[Server 1]` or `[Server 2]`.

**To Test Round Robin:** Open Terminal 5 and run another client. Observe how requests alternate between Server 1 and Server 2.
