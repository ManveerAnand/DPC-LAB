#include <iostream>
#include <omp.h>

using namespace std;

const int N = 8;

// Check if placing a queen at (row, col) is safe given previous placements
bool isSafe(const int board[], int row, int col)
{
    for (int i = 0; i < row; i++)
    {
        // Same column or same diagonal
        if (board[i] == col || abs(board[i] - col) == abs(i - row))
            return false;
    }
    return true;
}

// Recursive backtracking: place queens from 'row' onwards
int solveNQueens(int board[], int row)
{
    if (row == N)
        return 1; // All queens placed successfully

    int count = 0;
    for (int col = 0; col < N; col++)
    {
        if (isSafe(board, row, col))
        {
            board[row] = col;
            count += solveNQueens(board, row + 1);
        }
    }
    return count;
}

int main()
{
    cout << "========================================" << endl;
    cout << "  Parallel 8-Queens Solver (OpenMP)" << endl;
    cout << "========================================" << endl;
    cout << "Board Size: " << N << " x " << N << endl;
    cout << endl;

    int totalSolutions = 0;

    double startTime = omp_get_wtime();

    // Parallelize over first-row queen placements
    // Each thread explores trees rooted at a different column for row 0
#pragma omp parallel for schedule(dynamic) reduction(+ : totalSolutions)
    for (int col = 0; col < N; col++)
    {
        int localBoard[N];
        localBoard[0] = col;
        totalSolutions += solveNQueens(localBoard, 1);
    }

    double endTime = omp_get_wtime();
    double execTime = endTime - startTime;

    cout << "Total Valid Solutions : " << totalSolutions << endl;
    cout << "Execution Time       : " << execTime << " seconds" << endl;
    cout << endl;

    // Print one sample solution
    cout << "-- Sample Valid Configuration --" << endl;
    int sampleBoard[N];
    auto findFirst = [&](int board[], int row, auto &self) -> bool
    {
        if (row == N)
            return true;
        for (int col = 0; col < N; col++)
        {
            if (isSafe(board, row, col))
            {
                board[row] = col;
                if (self(board, row + 1, self))
                    return true;
            }
        }
        return false;
    };

    if (findFirst(sampleBoard, 0, findFirst))
    {
        for (int i = 0; i < N; i++)
        {
            for (int j = 0; j < N; j++)
            {
                if (sampleBoard[i] == j)
                    cout << " Q";
                else
                    cout << " .";
            }
            cout << endl;
        }
    }

    cout << "========================================" << endl;

    return 0;
}
