# Lab 2: Client-Server & Distributed Architectures

This project contains two implementations demonstrating network scaling concepts.

## 1. Single Server, Many Clients (Threaded)
**Folder:** [`MultiClient/`](MultiClient/)

A classic multi-threaded server implementation designed to handle multiple concurrent client connections on a single machine.
*   [Read Guide](MultiClient/README.md)

## 2. Multi-Server Architecture (Load Balanced)
**Folder:** [`MultiServer/`](MultiServer/)

A distributed system simulation featuring a Load Balancer implementing a Round-Robin algorithm to distribute traffic across multiple backend servers (Horizontal Scaling).
*   [Read Guide](MultiServer/README.md)
