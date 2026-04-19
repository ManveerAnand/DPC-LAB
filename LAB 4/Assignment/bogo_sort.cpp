/**
 * =============================================================
 *  Parallel BOGO Sort Performance Study using OpenMP
 *  CS637 - Distributed and Parallel Computing | Lab 4
 * =============================================================
 *
 *  Each thread independently shuffles its own copy of the array.
 *  The first thread to find a sorted permutation signals all
 *  others to stop via a shared atomic flag.
 *
 *  Compile:
 *    g++ -fopenmp -O2 -o bogo_sort bogo_sort.cpp
 *
 *  Run:
 *    ./bogo_sort
 * =============================================================
 */

#include <iostream>
#include <iomanip>
#include <vector>
#include <algorithm>
#include <random>
#include <ctime>
#include <cstring>
#include <omp.h>

using namespace std;

// ─── Configuration ───────────────────────────────────────────
const int N = 14;       // Array size (kept small; BOGO is O(n!))
const int VAL_MIN = 1;  // Minimum value in array
const int VAL_MAX = 50; // M


// ─── Utility: Check if array is sorted ───────────────────────
bool isSorted(const int arr[], int n)
{
    for (int i = 0; i < n - 1; i++)
    {
        if (arr[i] > arr[i + 1])
            return false;
    }
    return true;
}

// ─── Utility: Print array ────────────────────────────────────
void printArray(const int arr[], int n)
{
    for (int i = 0; i < n; i++)
    {
        cout << arr[i];
        if (i < n - 1)
            cout << " ";
    }
    cout << endl;
}

// ─── Sequential BOGO Sort ───────────────────────────────────
long long sequentialBogoSort(int arr[], int n)
{
    long long shuffles = 0;
    mt19937 rng(42); // fixed seed for reproducibility

    while (!isSorted(arr, n))
    {
        // Fisher-Yates shuffle
        for (int i = n - 1; i > 0; i--)
        {
            uniform_int_distribution<int> dist(0, i);
            int j = dist(rng);
            swap(arr[i], arr[j]);
        }
        shuffles++;
    }
    return shuffles;
}

// ─── Parallel BOGO Sort ─────────────────────────────────────
/**
 *  Each thread gets its own copy of the array and shuffles
 *  independently.  A shared `found` flag (atomic) lets the
 *  winning thread signal all others to stop.
 */
struct ParallelResult
{
    long long totalShuffles;
    int winnerThread;
    int sortedArray[N];
};

ParallelResult parallelBogoSort(const int original[], int n, int numThreads)
{
    // Shared termination flag
    volatile int found = 0;

    long long totalShuffles = 0;
    int winnerThread = -1;
    int result[N];

    omp_set_num_threads(numThreads);

#pragma omp parallel
    {
        int tid = omp_get_thread_num();

        // Each thread gets its own copy of the array
        int localArr[N];
        memcpy(localArr, original, n * sizeof(int));

        // Each thread gets a unique RNG seeded differently
        mt19937 rng(42 + tid * 1000 + (unsigned)time(NULL));

        long long localShuffles = 0;

        while (!found)
        {
            // Fisher-Yates shuffle on local copy
            for (int i = n - 1; i > 0; i--)
            {
                uniform_int_distribution<int> dist(0, i);
                int j = dist(rng);
                swap(localArr[i], localArr[j]);
            }
            localShuffles++;

            // Check if this shuffle produced a sorted array
            if (isSorted(localArr, n))
            {
#pragma omp critical
                {
                    if (!found)
                    {
                        found = 1;
                        winnerThread = tid;
                        memcpy(result, localArr, n * sizeof(int));
                    }
                }
            }
        }

// Accumulate total shuffles from all threads
#pragma omp atomic
        totalShuffles += localShuffles;
    }

    ParallelResult pr;
    pr.totalShuffles = totalShuffles;
    pr.winnerThread = winnerThread;
    memcpy(pr.sortedArray, result, n * sizeof(int));
    return pr;
}

// ═════════════════════════════════════════════════════════════
//  MAIN
// ═════════════════════════════════════════════════════════════
int main()
{
    // ─── Generate unique random array ────────────────────────
    int original[N];
    vector<int> pool;
    for (int v = VAL_MIN; v <= VAL_MAX; v++)
        pool.push_back(v);
    mt19937 genRng(time(NULL));
    shuffle(pool.begin(), pool.end(), genRng);
    for (int i = 0; i < N; i++)
    {
        original[i] = pool[i];
    }

    cout << "============================================================" << endl;
    cout << "  Parallel BOGO Sort — OpenMP Performance Study" << endl;
    cout << "  Array Size: " << N << "  |  Value Range: [" << VAL_MIN << ", " << VAL_MAX << "]" << endl;
    cout << "============================================================" << endl;
    cout << endl;

    // ─── Print original array ────────────────────────────────
    cout << "Sample Array: ";
    printArray(original, N);
    cout << endl;

    // ═══════════════════════════════════════════════════════
    //  SEQUENTIAL RUN
    // ═══════════════════════════════════════════════════════
    cout << "------------------------------------------------------------" << endl;
    cout << "  Sequential BOGO Sort (Baseline)" << endl;
    cout << "------------------------------------------------------------" << endl;

    int seqArr[N];
    memcpy(seqArr, original, N * sizeof(int));

    double seqStart = omp_get_wtime();
    long long seqShuffles = sequentialBogoSort(seqArr, N);
    double seqEnd = omp_get_wtime();
    double seqTime = seqEnd - seqStart;

    cout << "Sorted Array: ";
    printArray(seqArr, N);
    cout << "Time Taken:    " << fixed << setprecision(3) << seqTime << " sec" << endl;
    cout << "Total Shuffles: " << seqShuffles << endl;
    cout << endl;

    // ═══════════════════════════════════════════════════════
    //  PARALLEL RUNS (2, 4, 8 threads)
    // ═══════════════════════════════════════════════════════
    int threadCounts[] = {2, 4, 8};
    int numRuns = 3;

    // Storage for summary table
    double parTimes[3];
    long long parShuffles[3];
    double speedups[3];

    for (int r = 0; r < numRuns; r++)
    {
        int T = threadCounts[r];

        cout << "------------------------------------------------------------" << endl;
        cout << "  Parallel Run (Threads = " << T << ")" << endl;
        cout << "------------------------------------------------------------" << endl;

        double parStart = omp_get_wtime();
        ParallelResult pr = parallelBogoSort(original, N, T);
        double parEnd = omp_get_wtime();
        double parTime = parEnd - parStart;

        parTimes[r] = parTime;
        parShuffles[r] = pr.totalShuffles;
        speedups[r] = seqTime / parTime;

        cout << "Thread " << pr.winnerThread << " found the sorted array!" << endl;
        cout << "Sorted Array:  ";
        printArray(pr.sortedArray, N);
        cout << "Time Taken:    " << fixed << setprecision(3) << parTime << " sec" << endl;
        cout << "Total Shuffles: " << pr.totalShuffles << endl;
        cout << "Speedup:       " << fixed << setprecision(2) << speedups[r] << "x" << endl;
        cout << endl;
    }

    // ═══════════════════════════════════════════════════════
    //  SUMMARY TABLE
    // ═══════════════════════════════════════════════════════
    cout << "============================================================" << endl;
    cout << "  Summary Table" << endl;
    cout << "============================================================" << endl;
    cout << left
         << setw(12) << "Threads"
         << setw(15) << "Time(sec)"
         << setw(15) << "Shuffles"
         << setw(12) << "Speedup"
         << endl;
    cout << "------------------------------------------------------------" << endl;

    // Sequential baseline row
    cout << left
         << setw(12) << "1 (seq)"
         << setw(15) << fixed << setprecision(3) << seqTime
         << setw(15) << seqShuffles
         << setw(12) << "1.00x"
         << endl;

    // Parallel rows
    for (int r = 0; r < numRuns; r++)
    {
        cout << left
             << setw(12) << threadCounts[r]
             << setw(15) << fixed << setprecision(3) << parTimes[r]
             << setw(15) << parShuffles[r]
             << fixed << setprecision(2) << speedups[r] << "x"
             << endl;
    }

    cout << "============================================================" << endl;
    cout << endl;

    return 0;
}
