# Single Server, Many Clients (Threaded)

### 🧠 The Conceptual Problem (The "DMV" Problem)
In Lab 1, our server had a fatal flaw: **It was single-threaded.**
It handled one client at a time. If Client A connected and took 10 seconds to say "Hello", Client B was stuck waiting effectively "on hold" until Client A hung up.

**The Solution: Multithreading**
Just like a bank with multiple tellers. The bank (Server) has a main door. When you walk in, the manager assigns you a specific teller (Thread). That teller talks **only to you**, while the manager goes back to the door to greet the next person.

---

### 🔍 Deep Dive: The Code & Syntax

#### 1. The Mysterious `setsockopt`
You will see this line in `server.py`:
```python
s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
```
**Why do we need this?**
When you stop a server (Ctrl+C), the Operating System doesn't close the port immediately. It puts it in a `TIME_WAIT` state for a few minutes to ensure all lingering data packets are finished.
If you try to restart your server immediately, you'll get an error: `Address already in use`.
*   **`SOL_SOCKET`**: We are configuring the Socket layer itself.
*   **`SO_REUSEADDR`**: "Socket Option: Reuse Address".
*   **`1` (True)**: "Yes, please allow me to re-bind to this port even if it's technically still in timeout."

#### 2. The Threading Logic
This is the magic loop in `main()`:

```python
while True:
    conn, addr = s.accept()  # 1. Wait for a new connection
    
    # 2. Create a shiny new Thread
    t = threading.Thread(target=handle_client, args=(conn, addr), daemon=True)
    
    # 3. Launch it!
    t.start()
```

*   **`target=handle_client`**: This is the function the new thread will run.
*   **`args=(conn, addr)`**: We pass the *specific* connection socket to the thread. The thread owns this connection now.
*   **`daemon=True`**: This is a cleanup trick.
    *   **Normal Thread:** Keeps the program running even if Main crashes.
    *   **Daemon Thread:** "Background helper". If the Main program exits, all Daemon threads are instantly killed. This ensures that when you Ctrl+C the server, the threads don't keep running like headless chickens.

#### 3. Context Managers (`with socket...`)
```python
with socket.socket(...) as s:
    s.connect(...)
    # do stuff
```
The `with` keyword is a safety net. It guarantees that `s.close()` is called **even if your code crashes**. Without this, your program might leave "ghost" connections open, consuming system resources (file descriptors).

---

### 🛡️ Stress Testing
We wrote `stress_client.py` to prove the concept.
It creates **20 threads** on the client side.
Each thread acts like a unique user.
They all hit the "Connect" button at the same millisecond.
*   **Without Threading on the Server:** The 20th client would wait a long time.
*   **With Threading:** All 20 get an immediate "Hello" from a dedicated server thread.

---

## How to Run

### Option 1: Interactive Client

**Terminal 1 - Start Server:**
```bash
python "LAB 2/MultiClient/server.py"
```

**Terminal 2 - Run Client:**
```bash
python "LAB 2/MultiClient/client.py"
```
Type messages and press Enter. Open multiple terminals to run multiple clients simultaneously.

### Option 2: Stress Test (20 Clients Automatically)

**Terminal 1 - Start Server:**
```bash
python "LAB 2/MultiClient/server.py"
```

**Terminal 2 - Run Stress Test:**
```bash
python "LAB 2/MultiClient/stress_client.py"
```
Watch as 20 simultaneous clients connect and get responses.
