# Lab 4: Parallel BOGO Sort using OpenMP

## Overview
A performance study of BOGO Sort implemented in both sequential and parallel forms using **OpenMP**. Multiple threads independently shuffle their own copy of the array, and the first thread to find a sorted permutation terminates the entire computation.

## Architecture

```
                    ┌──────────────────────┐
                    │     Main Thread      │
                    │  Generate Array      │
                    │  Run Sequential      │
                    └──────────┬───────────┘
                               │
              ┌────────────────┼────────────────┐
              ▼                ▼                ▼
       ┌─────────────┐ ┌─────────────┐ ┌─────────────┐
       │  Thread 0   │ │  Thread 1   │ │  Thread T-1 │
       │  Local Copy │ │  Local Copy │ │  Local Copy │
       │  Own RNG    │ │  Own RNG    │ │  Own RNG    │
       │  Shuffle    │ │  Shuffle ✓  │ │  Shuffle    │
       └──────┬──────┘ └──────┬──────┘ └──────┬──────┘
              │               │                │
              │         found = 1              │
              │        (critical)              │
              └───────────────┼────────────────┘
                              │
                    ┌─────────▼──────────┐
                    │   Collect Results  │
                    │   Print Summary    │
                    └────────────────────┘
```

## OpenMP Concepts Used

| Construct | Directive | Purpose |
|-----------|-----------|---------|
| Parallel Region | `#pragma omp parallel` | Spawns T independent threads |
| Critical Section | `#pragma omp critical` | Protects shared result & flag |
| Atomic Operation | `#pragma omp atomic` | Accumulates shuffle counts |
| Thread Control | `omp_set_num_threads()` | Sets thread count per run |
| Timing | `omp_get_wtime()` | High-resolution wall clock |

## Quick Start

### Prerequisites
- **GCC** with OpenMP support (MinGW-w64 / MSYS2 on Windows)
- C++11 or later

### Compile & Run
```bash
# Compile with OpenMP
g++ -fopenmp -O2 -o bogo_sort.exe bogo_sort.cpp

# Run
./bogo_sort.exe
```

## Sample Output
```
============================================================
  Parallel BOGO Sort — OpenMP Performance Study
  Array Size: 10  |  Value Range: [1, 50]
============================================================

Sample Array: 11 41 43 8 37 36 38 49 46 30

Sequential BOGO Sort (Baseline):
  Time: 0.283 sec  |  Shuffles: 5,595,031

Parallel Run (2 threads):  0.214 sec  |  Speedup: 1.32x
Parallel Run (4 threads):  0.096 sec  |  Speedup: 2.95x
Parallel Run (8 threads):  0.022 sec  |  Speedup: 12.86x
```

## Results Summary

| Threads | Time (sec) | Shuffles | Speedup |
|---------|-----------|----------|---------|
| 1 (seq) | 0.283 | 5,595,031 | 1.00x |
| 2 | 0.214 | 6,788,361 | 1.32x |
| 4 | 0.096 | 5,089,005 | 2.95x |
| 8 | 0.022 | 1,565,129 | 12.86x |

> **Note:** Super-linear speedup (12.86x with 8 threads) is expected for trial-based parallel algorithms—more threads explore the permutation space faster, and the minimum discovery time across threads decreases faster than linearly.

## File Structure
```
LAB 4/Assignment/
├── bogo_sort.cpp    # Complete implementation
├── report.tex       # Detailed LaTeX documentation
└── README.md        # This file
```

## Key Design Decisions

1. **N = 10**: BOGO Sort is O(N!); N=10 gives ~3.6M expected shuffles—enough for measurable timing without waiting hours
2. **Unique Values**: Array values are unique integers from [1, 50], generated via Fisher-Yates shuffle on the value pool
3. **Independent RNGs**: Each thread has its own Mersenne Twister with a unique seed to avoid contention
4. **Volatile Flag**: The `found` flag uses `volatile` to prevent compiler optimization of the read in the while-loop
