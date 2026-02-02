# Lab 2 Assignment: Multi-Server System

## Overview
A scalable client-server communication system featuring multiple server instances running concurrently on different ports, each handling multiple clients simultaneously using multithreading.

## System Architecture

### Components
1. **`server.py`** - Launches 3 server instances (Ports: 5001, 5002, 5003)
2. **`client.py`** - Interactive client with manual server selection
3. **`report.tex`** - Detailed LaTeX documentation

### Supported Operations

#### Arithmetic Processing
- **Addition:** `add <num1> <num2>`
- **Subtraction:** `sub <num1> <num2>`
- **Multiplication:** `mul <num1> <num2>`
- **Division:** `div <num1> <num2>`

#### String Analysis
- **Analyze:** `analyze <text>`
  - Converts text to uppercase
  - Counts characters and words

---

## How to Run

### Step 1: Start the Multi-Server System

Open a terminal and run:
```bash
python "LAB 2/Assignment/server.py"
```

**Expected Output:**
```
============================================================
Multi-Server System Starting...
============================================================
[Server A] Started on port 5001
[Server B] Started on port 5002
[Server C] Started on port 5003

All servers are running. Press Ctrl+C to stop.
```

### Step 2: Run the Client (Interactive Mode)

Open a **new terminal** and run:
```bash
python "LAB 2/Assignment/client.py"
```

**Usage:**
1. Enter a server port (5001, 5002, or 5003)
2. Enter a command (e.g., `add 10 20` or `analyze Hello World`)
3. View the response
4. Type `quit` to exit

### Step 3: Run Demo Mode (Automated Tests)

To run all test cases automatically:
```bash
python "LAB 2/Assignment/client.py" --demo
```

---

## Example Usage

### Arithmetic Operations

**Terminal 1 (Client):**
```
Select server port (5001/5002/5003): 5001
Enter command: add 10 20
Connected to server at 127.0.0.1:5001

Server Response:
Result: 30.0
```

**Terminal 1 (Client):**
```
Select server port (5001/5002/5003): 5002
Enter command: div 40 5
Connected to server at 127.0.0.1:5002

Server Response:
Result: 8.0
```

### String Analysis

**Terminal 1 (Client):**
```
Select server port (5001/5002/5003): 5003
Enter command: analyze Hello Server Programming
Connected to server at 127.0.0.1:5003

Server Response:
Uppercase: HELLO SERVER PROGRAMMING
Character Count: 25
Word Count: 3
```

### Error Handling

**Terminal 1 (Client):**
```
Select server port (5001/5002/5003): 5001
Enter command: div 10 0
Connected to server at 127.0.0.1:5001

Server Response:
Error: Division by zero
```

---

## Testing Multiple Concurrent Clients

To test concurrent client handling, open **3 client terminals** simultaneously and connect to the same server port. Each client will be handled independently by separate threads.

---

## Generate PDF Report

To compile the LaTeX report:
```bash
cd "LAB 2/Assignment"
pdflatex report.tex
pdflatex report.tex  # Run twice for table of contents
```

This generates `report.pdf` with complete documentation, code listings, and terminal outputs.

---

## Key Features Demonstrated

1. **Multi-Server Architecture:** 3 servers running in one process
2. **Concurrent Client Handling:** Each server uses threading for multiple clients
3. **Task Processing:** Arithmetic operations and string analysis
4. **Error Handling:** Division by zero, invalid commands, malformed requests
5. **Graceful Shutdown:** Ctrl+C cleanly stops all servers
6. **Logging:** Timestamped, server-tagged logs for debugging

---

## Stopping the Servers

Press **Ctrl+C** in the server terminal to gracefully shut down all servers.

```
^C
Shutting down all servers...
Goodbye!
```
