# Lab 3 Assignment: Distributed P2P Chat Application

## Overview
A fully decentralized peer-to-peer chat system where each node acts as both a client and a server. Two terminals communicate directly without any centralized server.

## Architecture

Each node runs **3 components** concurrently:

```text
  Node A                                         Node B
  ------                                         ------
  [User Input]                                      
      |                                             
      v                                             
  [Client Module]                                   
      |  (sends to own relay)                       
      v                                             
  [Relay Server :7001]                              
      |  (forwards to peer)                         
      v                                             
                    ----(network)---->               
                                                    
                                         [External Server :6002]
                                              |
                                              v
                                         [Display Message]
```

### Port Layout

| Node   | External Server | Relay Server | Peer Target |
|--------|-----------------|--------------|-------------|
| Node A | 6001            | 7001         | 6002        |
| Node B | 6002            | 7002         | 6001        |

---

## How to Run

### Step 1: Start Node A

Open **Terminal 1** and run:
```bash
python node.py A 6001 6002
```

### Step 2: Start Node B

Open **Terminal 2** and run:
```bash
python node.py B 6002 6001
```

Node A will wait for Node B to come online. Once both are running, you can type messages in either terminal.

### Step 3: Chat!

```
[A] > Hello Node B!
  [Relay] Forwarded to peer on port 6002
```

On Node B's terminal:
```
  >> [A]: Hello Node B!
[B] > Hey! Got your message!
```

Type `quit` to exit.

---

## Files

| File         | Description                                      |
|--------------|--------------------------------------------------|
| `node.py`    | Complete P2P chat node (client + server + relay)  |
| `report.tex` | LaTeX documentation with code and terminal output |
| `README.md`  | This file                                         |

---

## Generate PDF Report

```bash
cd "LAB 3/Assignment"
pdflatex report.tex
pdflatex report.tex
```
