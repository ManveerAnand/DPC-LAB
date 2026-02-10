<div align="center">

# 🌐 Distributed & Parallel Computing Lab Archive

**Making computers talk to each other (without screaming errors)**

[![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)](https://www.python.org/)
[![Status](https://img.shields.io/badge/Status-Active-success.svg)]()
[![Lab](https://img.shields.io/badge/Current_Lab-3-orange.svg)]()
[![License](https://img.shields.io/badge/License-MIT-purple.svg)]()

*Journey through socket programming, threading, P2P architectures, and distributed systems*

</div>

---

## 📊 Current Status

| Metric | Status |
|--------|--------|
| **Progress Level** | Lab 3 ✅ |
| **System State** | Fully Operational 🚀 |
| **Bugs Squashed** | Too many to count 🐛 |
| **Coffee Consumed** | Infinite ☕ |

---

## 🗂️ Lab Timeline

### 🔥 Lab 3: Peer-to-Peer Chat System
> **Achievement Unlocked: True Decentralization** 🏆

**The Revolution:** I killed the central server. Now every node is a rebel—acting as both client and server simultaneously. Two terminals chat directly without asking permission from any middleman.

#### 🎯 Key Features
- **Three-Component Architecture**: External Server + Relay Server + Client Module
- **Message Routing**: Messages flow through sender's own server before reaching peer
- **No Single Point of Failure**: Nodes only depend on their peers, not a central authority
- **Concurrent Operations**: Multithreading enables real-time bidirectional chat

#### 🛠️ Tech Stack
```
Python Socket Programming | Threading | TCP/IP | P2P Architecture
```

#### 📂 Directory Structure
```
LAB 3/Assignment/
├── node.py          # Complete P2P chat node implementation
├── report.tex       # Detailed LaTeX documentation
└── README.md        # Setup and usage instructions
```

[📖 View Lab 3 Details →](./LAB%203/Assignment/)

---

### ⚡ Lab 2: Concurrency & Load Balancing
> **Achievement Unlocked: Multitasking Mastery** 🎖️

**The Realization:** A single-threaded server handling multiple clients is like using a screen door on a submarine—technically possible, but spectacularly ineffective.

#### 🎯 What I Built

**1. Multi-Client Server** 🧵
- Threading-based concurrent client handling
- Each connection gets its own worker thread
- No more waiting in line for service

**2. Multi-Server Architecture with Load Balancer** ⚖️
- Custom TCP Layer 4 Load Balancer
- Round Robin distribution strategy
- Transparent proxy forwarding
- Horizontal scalability achieved

**3. Assignment: Distributed Request Processing** 🔢
- Three backend servers (ports 5001-5003)
- Arithmetic operations server
- String analysis server
- Real-world multi-server coordination

#### 🛠️ Tech Stack
```
Python Sockets | Threading | TCP Load Balancing | Concurrent Programming
```

#### 📂 Directory Structure
```
LAB 2/
├── MultiClient/          # Multi-threaded server demo
│   ├── server.py
│   ├── client.py
│   └── README.md
├── MultiServer/          # Load balancer implementation
│   ├── load_balancer.py
│   ├── backend.py
│   ├── client.py
│   └── README.md
└── Assignment/           # Multi-server request processor
    ├── server.py
    ├── client.py
    ├── report.tex
    └── README.md
```

[📖 View Lab 2 Details →](./LAB%202/)

---

### 🌱 Lab 1: Foundations & Remote Procedure Calls
> **Achievement Unlocked: Hello World (Remotely)** 🎓

**The Beginning:** Where I learned that `localhost` and `127.0.0.1` are both home, but in different languages.

#### 🎯 What I Learned

**Basic Socket Programming** 🔌
- TCP connection establishment (the sacred handshake)
- Client-server communication patterns
- Data serialization and deserialization
- Port binding and listening

**Remote Procedure Calls (RPC)** 📞
- Making functions run on remote machines
- Request-response patterns
- Function parameter marshalling
- The illusion of local execution for remote code

#### 🛠️ Tech Stack
```
Python Socket API | TCP/IP | RPC Concepts | Client-Server Architecture
```

#### 📂 Directory Structure
```
LAB 1/
├── CLIENT_SERVER/        # Basic socket examples
│   ├── server.py
│   └── client.py
└── RPC/                  # Remote procedure call implementation
    ├── rpc_server.py
    └── rpc_client.py
```

[📖 View Lab 1 Details →](./LAB%201/)

---

## 🚀 Quick Start

### Prerequisites
```bash
Python 3.8+
```

### Clone & Run
```bash
# Clone the repository
git clone https://github.com/YourUsername/DPC.git
cd DPC

# Navigate to any lab
cd "LAB 3/Assignment"

# Run the implementation
python node.py A 6001 6002  # Terminal 1
python node.py B 6002 6001  # Terminal 2
```

---

## 📚 Learning Outcomes

| Concept | Lab | Status |
|---------|-----|--------|
| Socket Programming Basics | Lab 1 | ✅ Mastered |
| Remote Procedure Calls | Lab 1 | ✅ Implemented |
| Multi-threading | Lab 2 | ✅ Deployed |
| Load Balancing | Lab 2 | ✅ Engineered |
| P2P Architecture | Lab 3 | ✅ Revolutionized |
| Distributed Systems Design | All Labs | 🔄 Ongoing |

---

## 🎓 Course Information

**Course:** CS302 - Distributed and Parallel Computing  
**Institution:** [Your Institution]  
**Instructor:** Dr. Sanjay Saxena  
**Session:** Winter 2026-27  
**Student:** Manveer Anand (202351080)

---

## 🛠️ Technology Stack

<div align="center">

![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)
![Sockets](https://img.shields.io/badge/Socket_Programming-FF6B6B?style=for-the-badge)
![TCP/IP](https://img.shields.io/badge/TCP%2FIP-4A90E2?style=for-the-badge)
![Threading](https://img.shields.io/badge/Threading-50C878?style=for-the-badge)
![LaTeX](https://img.shields.io/badge/LaTeX-008080?style=for-the-badge&logo=latex&logoColor=white)

</div>

---

## 📈 Repository Stats

```
Total Labs Completed: 3
Total Lines of Code: 2000+
Bugs Fixed: ∞
Hours of Debugging: Don't ask
```

---

## 🔮 What's Next?

The journey continues. More labs, more complex architectures, and inevitably, more distributed bugs to squash. Each lab builds on the last, creating a foundation in distributed systems that goes from "Hello World" to "Hello Distributed World."

**Upcoming Topics:**
- Distributed consensus algorithms
- Fault tolerance mechanisms
- Advanced synchronization primitives
- Message queuing systems

---

## 📝 License

This project is licensed under the MIT License - see what you want, it's all learning material.

---

<div align="center">

**Made with ☕ and lots of debugging**

*Repository Maintained by [Manveer Anand](https://github.com/YourUsername)*

⭐ Star this repo if you found it helpful!

</div>

