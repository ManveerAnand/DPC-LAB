# DPC Labs Master README (Exam-Oriented)

This file summarizes what was done in each lab, what happened/what you should remember for exams, the language(s) used, and how to run each lab.

## How to Use This Guide

- Run commands from the repository root: `d:\Dev 2.0\DPC`
- Use separate terminals where noted (server/client or multi-process runs)
- For labs with reports/notebooks, code files are the fastest way to reproduce outputs

## Global Prerequisites

- Python 3.8+ (recommended for Labs 1, 2, 3, 8, 9)
- C/C++ compiler with OpenMP support (Labs 4, 5)
- CUDA Toolkit (`nvcc`) + NVIDIA GPU (Lab 6)
- MPI runtime/toolchain (MS-MPI/OpenMPI + `mpiexec`) for Labs 7 and 9
- Python package for MPI (Lab 9):

```bash
pip install mpi4py
```

---

## Lab 1 - Foundations: Socket Programming and RPC

**Languages:** Python

### What we did
- Implemented basic socket client-server communication (`CLIENT_SERVER/`)
- Added an improved command-based socket server (`ADD:x:y`, `SQUARE:x`) in `server_pro.py`
- Implemented XML-RPC service for palindrome/Armstrong checks (`RPC/`)
- Assignment version: matrix multiplication over both sockets and RPC (`Assignment/`)

### What happened (exam perspective)
- Socket server blocks on `accept()` until a client connects
- Data is sent/received as bytes and decoded/encoded manually
- RPC hides raw socket-level serialization and exposes function calls (`proxy.check(...)`, `proxy.multiply(...)`)
- Matrix multiplication logic stayed same in both socket and RPC variants; only communication model changed

### How to run

#### Basic socket demo
```bash
python "LAB 1/CLIENT_SERVER/server.py"
python "LAB 1/CLIENT_SERVER/client.py"
```

#### Command-based socket demo
```bash
python "LAB 1/CLIENT_SERVER/server_pro.py"
python "LAB 1/CLIENT_SERVER/client_pro.py"
```

#### RPC palindrome/Armstrong demo
```bash
python "LAB 1/RPC/rpc_server.py"
python "LAB 1/RPC/rpc_client.py"
```

#### Assignment matrix multiplication (socket)
```bash
python "LAB 1/Assignment/server.py"
python "LAB 1/Assignment/client.py"
```

#### Assignment matrix multiplication (RPC)
```bash
python "LAB 1/Assignment/rpc_server.py"
python "LAB 1/Assignment/rpc_client.py"
```

---

## Lab 2 - Scaling Client-Server Architectures

**Languages:** Python

### What we did
- Built multi-client threaded server (`MultiClient/`)
- Built load-balanced multi-server architecture (`MultiServer/`) using round-robin LB
- Assignment: 3 server instances (`5001`, `5002`, `5003`) supporting arithmetic + text analysis

### What happened (exam perspective)
- Thread-per-client design removed single-client bottleneck
- `SO_REUSEADDR` allowed fast server restart after stop
- Load balancer forwarded traffic to backend servers in round-robin order
- Assignment server handled invalid commands and divide-by-zero robustly

### How to run

#### MultiClient (threaded single server)
```bash
python "LAB 2/MultiClient/server.py"
python "LAB 2/MultiClient/client.py"
python "LAB 2/MultiClient/stress_client.py"
```

#### MultiServer (2 backends + load balancer)
```bash
python "LAB 2/MultiServer/backend.py" 5001 1
python "LAB 2/MultiServer/backend.py" 5002 2
python "LAB 2/MultiServer/load_balancer.py"
python "LAB 2/MultiServer/client.py"
```

#### Assignment (3 logical servers in one process)
```bash
python "LAB 2/Assignment/server.py"
python "LAB 2/Assignment/client.py"
python "LAB 2/Assignment/client.py" --demo
```

---

## Lab 3 - Decentralized Peer-to-Peer Chat

**Languages:** Python

### What we did
- Built a P2P chat node (`node.py`) where each node is both client and server
- Each node runs 3 components: external server, relay server, and input client module

### What happened (exam perspective)
- No central server: both nodes are symmetric peers
- Relay module forwards local input to peer external server
- If peer is offline, node retries connection until peer comes online
- Demonstrates distributed design with local forwarding + remote delivery

### How to run
(Use two terminals)

```bash
python "LAB 3/Assignment/node.py" A 6001 6002
python "LAB 3/Assignment/node.py" B 6002 6001
```

Type `quit` in a terminal to exit that node.

---

## Lab 4 - OpenMP Parallelism and BOGO Study

**Languages:** C++ (OpenMP)

### What we did
- Assignment: sequential vs parallel BOGO sort with multiple thread counts (`Assignment/bogo_sort.cpp`)
- Additional OpenMP practice files: `codes.cpp`, `pu1.cpp`

### What happened (exam perspective)
- Parallel BOGO used independent per-thread shuffling and shared completion flag
- The first winning thread terminated overall search; others stopped when flag set
- Speedup behavior can be non-linear/super-linear due to randomized search space
- `codes.cpp` demonstrates OpenMP `sections`; `pu1.cpp` shows simple loop parallelization idea

### How to run

#### Assignment BOGO study
```bash
g++ -fopenmp -O2 "LAB 4/Assignment/bogo_sort.cpp" -o bogo_sort.exe
./bogo_sort.exe
```

#### Additional practice programs
```bash
g++ -fopenmp "LAB 4/codes.cpp" -o codes.exe
./codes.exe

g++ -fopenmp "LAB 4/pu1.cpp" -o pu1.exe
./pu1.exe
```

---

## Lab 5 - OpenMP: Sorting, Matrix Multiply, N-Queens

**Languages:** C++ (OpenMP)

### What we did
- Implemented odd-even transposition sort (`bubble_sort.cpp`)
- Implemented parallel matrix multiplication (`MM.cpp`)
- Assignment: parallel 8-Queens solver (`Assignement/n_queens.cpp`)

### What happened (exam perspective)
- Odd-even sort is parallelizable because compared pairs in each phase are disjoint
- Matrix multiplication used nested-loop parallelization (`collapse(2)`)
- N-Queens used parallel first-row branching with reduction for total solution count
- For N=8, expected total solutions are 92 (core correctness checkpoint)

### How to run
```bash
g++ -fopenmp "LAB 5/bubble_sort.cpp" -o bubble_sort.exe
./bubble_sort.exe

g++ -fopenmp "LAB 5/MM.cpp" -o mm.exe
./mm.exe

g++ -fopenmp -O2 "LAB 5/Assignement/n_queens.cpp" -o n_queens.exe
./n_queens.exe
```

---

## Lab 6 - CUDA Programming

**Languages:** CUDA C++, Python (notebook driver)

### What we did
- Built CUDA histogram kernel with `atomicAdd` (`hist_freq.cu`)
- Built shared-memory prefix sum kernel (`prefix_sum_shared.cu`)
- Assignment notebook (`Assignment/lab6_assignment_202351080.ipynb`) generated and ran a CUDA program to search candidate keys and compute guest metrics

### What happened (exam perspective)
- Histogram race conditions were handled using atomic operations
- Prefix sum used `__shared__` memory + synchronization per stride
- Assignment used GPU reductions over very large input (`2^22` guests) and batched candidate key evaluation
- Demonstrates kernel design, block/thread indexing, and host-device memory transfer flow

### How to run

#### Standalone CUDA files
```bash
nvcc -O2 "LAB 6/hist_freq.cu" -o hist_freq.exe
./hist_freq.exe

nvcc -O2 "LAB 6/prefix_sum_shared.cu" -o prefix_sum_shared.exe
./prefix_sum_shared.exe
```

#### Assignment notebook
- Open `LAB 6/Assignment/lab6_assignment_202351080.ipynb`
- Run cells in order (GPU check -> write CUDA file -> compile -> execute)
- In Colab/local Jupyter, the key compile/run commands are:

```bash
nvcc -O2 king_nala_lab6.cu -o king_nala_lab6
./king_nala_lab6
```

---

## Lab 7 - MPI Basics and Distributed Computation

**Languages:** C, C++, PowerShell, Python utility script

### What we did
- MPI hello-world process identity demo (`hello_mpi.c`)
- Point-to-point order processing (`order_processing.cpp`)
- Broadcast bonus distribution (`bonus_distribution.cpp`)
- Assignment: heavy compute + message exchange for Staff WiFi key derivation (`Assignment/staff_wifi.cpp`, `Assignment/totry.cpp`)

### What happened (exam perspective)
- Learned rank/size model and SPMD execution style
- Verified point-to-point communication with `MPI_Send` and `MPI_Recv`
- Verified one-to-all communication with `MPI_Bcast`
- Assignment combined expensive deterministic computation (`grinder`) + 2-process exchange + consistency check

### How to run

#### Option A: compile and run directly
```bash
mpicc "LAB 7/hello_mpi.c" -o hello_mpi.exe
mpiexec -n 4 ./hello_mpi.exe

mpicxx "LAB 7/order_processing.cpp" -o order_processing.exe
mpiexec -n 2 ./order_processing.exe

mpicxx "LAB 7/bonus_distribution.cpp" -o bonus_distribution.exe
mpiexec -n 4 ./bonus_distribution.exe

mpicxx "LAB 7/Assignment/staff_wifi.cpp" -o staff_wifi.exe
mpiexec -n 2 ./staff_wifi.exe
```

#### Option B: use provided PowerShell helper for C++ sources
```powershell
powershell -ExecutionPolicy Bypass -File "LAB 7/run_mpi.ps1" -SourceFile "LAB 7/order_processing.cpp" -Processes 2
```

---

## Lab 8 - Time Synchronization and Logical Clocks

**Languages:** Python

### What we did
- Berkeley clock synchronization simulation (`berkeley.py`)
- Lamport + vector clock event simulation (`logical_clocks.py`)
- Assignment scenario (`Assignment/chronos.py` + `Assignment/seed.json`): fault-tolerant sync plus causal message processing and buffering

### What happened (exam perspective)
- Berkeley method aligned clocks to an averaged target; outliers can be ignored via threshold
- Lamport clocks preserve happened-before ordering with scalar timestamps
- Vector clocks capture causality more precisely and detect out-of-order arrivals
- Chronos assignment buffered early messages until causal constraints were satisfied, then released buffered items

### How to run
```bash
python "LAB 8/berkeley.py"
python "LAB 8/logical_clocks.py"
```

For assignment file (needs local `seed.json` in same folder):
```bash
cd "LAB 8/Assignment"
python chronos.py
```

---

## Lab 9 - MPI with Python (Distributed Bank Backend)

**Languages:** Python (mpi4py), LaTeX report

### What we did
- Implemented a 2-process MPI simulation of a joint fixed-deposit backend (`Assignment/final_mpi.py`)
- Each rank computes maturity independently, exchanges values via send/recv, then performs consensus validation via gather

### What happened (exam perspective)
- Rank 0 and Rank 1 performed parallel local computation with daily random bonus + audit delay
- Explicit message tags and receive ordering avoided deadlock
- Final phase validated that both nodes computed the same global total (consensus check)
- Demonstrates practical IPC + synchronization barriers + correctness verification in MPI

### How to run
```bash
mpiexec -n 2 py "LAB 9/Assignment/final_mpi.py"
```

(Equivalent from inside `LAB 9/Assignment`)
```bash
mpiexec -n 2 py .\final_mpi.py
```

---

## Quick Revision Checklist (Before Exam)

- Socket vs RPC differences: control, complexity, serialization model (Lab 1)
- Thread-per-client and load balancing tradeoffs (Lab 2)
- Pure P2P design and component roles (Lab 3)
- OpenMP primitives: `parallel`, `sections`, `critical`, `atomic`, `reduction`, `collapse` (Labs 4-5)
- CUDA fundamentals: kernel launch config, memory hierarchy, synchronization, atomics (Lab 6)
- MPI fundamentals: rank/size, send/recv, broadcast, barriers, gather, deadlock-safe ordering (Labs 7 and 9)
- Clock synchronization and causality: Berkeley, Lamport, vector clocks, buffering rules (Lab 8)

---

If you want, this can be extended into a one-page viva cheat sheet next (only formulas, key APIs, and expected interview-style answers).
