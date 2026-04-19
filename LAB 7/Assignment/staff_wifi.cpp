#include <iostream>
#include <mpi.h>

using namespace std;

// The Grinder Function
// Runs 2 billion times to simulate a heavy workload
long long grinder(long long seed, long long m, long long a, long long mod_val) {
    long long r = seed;
    // 2,000,000,000 iterations
    for (long long i = 0; i < 2000000000LL; ++i) {
        r = (r * m + a) % mod_val;
    }
    return r;
}

int main(int argc, char** argv) {
    // Initialize MPI
    MPI_Init(&argc, &argv);

    int rank;
    MPI_Comm_rank(MPI_COMM_WORLD, &rank);

    // Start the timer
    double start_time = MPI_Wtime();

    // The Student IDs (Last 4 digits)
    long long A = 1080; // Your ID (202351080)
    long long B = 1114; // <--- REPLACE THIS WITH YOUR FRIEND'S LAST 4 DIGITS

    long long alpha, beta, verify;

    // ==========================================
    // RANK 0: STUDENT 1
    // ==========================================
    if (rank == 0) {
        // Step 1a, 1b, 1c
        long long alpha_prime = grinder(A, 31, 17, 9973);
        long long alpha_double_prime = grinder(alpha_prime, 37, 11, 9973);
        alpha = (alpha_prime + alpha_double_prime) % 9973;

        // Send alpha to Student 2 (Rank 1)
        MPI_Send(&alpha, 1, MPI_LONG_LONG, 1, 0, MPI_COMM_WORLD);

        // Receive beta from Student 2 (Rank 1)
        MPI_Recv(&beta, 1, MPI_LONG_LONG, 1, 0, MPI_COMM_WORLD, MPI_STATUS_IGNORE);

        // Step 3: Compute Verification
        verify = grinder(alpha + beta, 7, 3, 101);

        // Step 4 & 5: Compute Password
        long long R = grinder(alpha * beta + A + B, 13, 7, 9973);
        long long password = R % 10000;

        double end_time = MPI_Wtime();

        // Print final results
        cout << "[Student 1] Verification Code: " << verify << endl;
        cout << "[Student 1] The Staff WiFi Password is: " << password << endl;
        cout << "Total Execution Time: " << (end_time - start_time) << " seconds" << endl;

    } 
    // ==========================================
    // RANK 1: STUDENT 2
    // ==========================================
    else if (rank == 1) {
        // Receive alpha from Student 1 (Rank 0)
        MPI_Recv(&alpha, 1, MPI_LONG_LONG, 0, 0, MPI_COMM_WORLD, MPI_STATUS_IGNORE);

        // Step 2a, 2b, 2c
        long long beta_prime = grinder(alpha, B, 13, 9973);
        long long beta_double_prime = grinder(beta_prime, 41, 19, 9973);
        beta = (beta_prime + beta_double_prime) % 9973;

        // Send beta to Student 1 (Rank 0)
        MPI_Send(&beta, 1, MPI_LONG_LONG, 0, 0, MPI_COMM_WORLD);

        // Step 3: Compute Verification
        verify = grinder(alpha + beta, 7, 3, 101);

        cout << "[Student 2] Verification Code: " << verify << endl;
    }

    // Finalize MPI
    MPI_Finalize();
    return 0;
}