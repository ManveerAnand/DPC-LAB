#include <iostream>
#include <omp.h>

using namespace std;

int main()
{
    int n;

    cout << "Enter number of elements: ";
    cin >> n;

    int arr[n];

    cout << "Enter array elements:" << endl;
    for (int i = 0; i < n; i++)
        cin >> arr[i];

    // Odd-Even Transposition Sort
    for (int i = 0; i < n; i++)
    {
        if (i % 2 == 0)
        {
#pragma omp parallel for
            for (int j = 0; j < n - 1; j += 2)
            {
                if (arr[j] > arr[j + 1])
                    swap(arr[j], arr[j + 1]);
            }
        }
        else
        {
#pragma omp parallel for
            for (int j = 1; j < n - 1; j += 2)
            {
                if (arr[j] > arr[j + 1])
                    swap(arr[j], arr[j + 1]);
            }
        }
    }

    cout << "Sorted array:" << endl;
    for (int i = 0; i < n; i++)
        cout << arr[i] << " ";
    cout << endl;

    return 0;
}

/*
 * HOW ODD-EVEN TRANSPOSITION SORT WORKS
 * ======================================
 *
 * Classic bubble sort compares adjacent pairs sequentially (left to right),
 * so each swap depends on the previous one — it CANNOT be parallelized.
 *
 * Odd-Even Transposition splits each pass into two independent phases:
 *
 *   EVEN phase (i=0,2,4,...): compare pairs at indices (0,1), (2,3), (4,5), ...
 *   ODD  phase (i=1,3,5,...): compare pairs at indices (1,2), (3,4), (5,6), ...
 *
 * Example with arr = [5, 2, 9, 1, 6]:
 *
 *   Pass 0 (EVEN): compare (0,1)(2,3)(4,-)  → [2,5, 1,9, 6]
 *   Pass 1 (ODD):  compare (1,2)(3,4)       → [2,1, 5,6, 9]
 *   Pass 2 (EVEN): compare (0,1)(2,3)(4,-)  → [1,2, 5,6, 9]
 *   Pass 3 (ODD):  compare (1,2)(3,4)       → [1,2, 5,6, 9]  (no swaps)
 *   Pass 4 (EVEN): compare (0,1)(2,3)(4,-)  → [1,2, 5,6, 9]  (sorted!)
 *
 * Why it's parallelizable:
 *   Within each phase, the pairs DON'T overlap — (0,1) and (2,3) share no
 *   indices, so multiple threads can compare & swap them simultaneously.
 *   This is why #pragma omp parallel for works here but not on classic bubble sort.
 *
 * Guaranteed to sort in exactly N passes (N = number of elements).
 */