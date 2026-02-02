# Lab 1: The Foundations of Distributed Computing

Welcome to the engine room. Before we can build massive distributed systems, we need to understand the nuts and bolts of how two programs on different computers (or the same one) talk to each other.

This Lab covers two fundamental communication patterns:
1.  **Sockets (Client-Server)**: The raw, byte-level conversation.
2.  **RPC (Remote Procedure Call)**: The polite, "please run this function for me" conversation.

---

## Part 1: Sockets (The "Hello World" of Networking)

### 🧠 The Concept
Imagine you want to talk to your friend.
1.  You need a phone (**Socket**).
2.  Your friend needs a phone number (**IP Address**) and an extension number (**Port**) so you don't accidentally call their FAX machine.
3.  Your friend needs to be sitting by the phone, waiting for it to ring (**Bind & Listen**).
4.  You dial the number (**Connect**).
5.  Your friend picks up (**Accept**).
6.  You talk (**Send/Recv**).

### 🔍 Decoding the Syntax (The "Magical Incantations")

You will see this line everywhere. Let's rip it apart:

```python
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
```

*   **`socket.socket(...)`**: "Hey, Operating System! Give me a network endpoint."
*   **`socket.AF_INET`**: This stands for **Address Family: Internet** (IPv4). It means we are identifying computers using IP addresses like `127.0.0.1`.
    *   *Alternative:* `AF_UNIX` (for local files) or `AF_INET6` (for IPv6).
*   **`socket.SOCK_STREAM`**: This means we want a **TCP** connection.
    *   **TCP (Transmission Control Protocol)** is reliable. It guarantees that if you send "Hello", it arrives as "Hello", not "Hlole" or "Hell". It creates a continuous "stream" of data.
    *   *Alternative:* `SOCK_DGRAM` (UDP) - fast, fire-and-forget, but messages might get lost.

#### The Server Setup Ritual
1.  **`s.bind((HOST, PORT))`**: "Operating System, reserve Port 5000 for me. If anyone knocks on door 5000, send them to me."
2.  **`s.listen()`**: "I am open for business. Put incoming calls in a queue."
3.  **`conn, addr = s.accept()`**: **CRITICAL STEP.**
    *   This command **blocks** (pauses) your program. It sits there and waits.
    *   When a client connects, it wakes up and returns **two** things:
        *   `conn`: A *new* socket object dedicated specifically to *this* client.
        *   `addr`: The IP address of the client.

#### The Client Setup Ritual
1.  **`s.connect((HOST, PORT))`**: "Dial this number." If nobody is listening, this crashes with `ConnectionRefusedError`.

---

## Part 2: RPC (Remote Procedure Calls)

### 🧠 The Concept
Sockets are great, but they are "dumb". They only send bytes (text). Coping with "Send `15`, multiply it by `2`, and send back `30`" using raw sockets is annoying because you have to parse strings manually.

**RPC** abstracts this away. It lets you call a function on another computer as if it were on your own computer.

*   You: `result = server.check("palindrome", 12321)`
*   RPC Library: *Magic happens (serializes arguments, sends over network, runs function on server, sends result back).*
*   You: `print(result)` -> `True`

### 🔍 Decoding the Syntax (`xmlrpc`)

```python
server = SimpleXMLRPCServer(("0.0.0.0", 6000))
server.register_function(check, "check")
```
*   **`SimpleXMLRPCServer`**: A built-in Python class that handles all the socket mess for you. It listens for XML messages.
*   **`register_function(func, name)`**: This exposes your local Python function to the world.
    *   `func`: The actual code to run.
    *   `name`: The string name clients will use to ask for it.

**Why XML?**
It's an old standard. The data is wrapped in XML tags (e.g., `<param><value><int>123</int></value></param>`) so that any language (Java, C++, Python) can understand the request.
