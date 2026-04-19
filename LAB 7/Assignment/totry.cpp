/*
 * Operation Staff-WiFi
 * Distributed & Parallel Computing Lab Assignment
 * * Student 1 ID: 20231114 -> A = 1114 (My ID)
 * Student 2 ID: 202351080 -> B = 1080 (Friend's ID)
 */

#include <iostream>
#include <mpi.h>

using namespace std;

// The computationally expensive Grinder function
long long grinder(long long seed, long long m, long long a, long long mod_val) {
    long long r = seed;
    // N = 2,000,000,000 as specified. 
    // Using long long (LL) to avoid 32-bit integer overflow issues.
    long long N = 2000000000LL; 
    
    for (long long i = 0; i < N; ++i) {
        r = (r * m + a) % mod_val;
    }
    return r;
}

int main(int argc, char** argv) {
    // Initialize the MPI environment
    MPI_Init(&argc, &argv);

    int rank, size;
    MPI_Comm_rank(MPI_COMM_WORLD, &rank);
    MPI_Comm_size(MPI_COMM_WORLD, &size);

    // The assignment requires exactly two students (processes)
    if (size != 2) {
        if (rank == 0) {
            cout << "Error: This simulation requires exactly 2 MPI processes." << endl;
            cout << "Run using: mpirun --oversubscribe -np 2 ./wifi_cipher" << endl;
        }
        MPI_Finalize();
        return 0;
    }

    // Keys extracted from the last 4 digits of the provided student IDs
    long long A = 1121; // Student 1 (You)
    long long B = 1120; // Student 2 (Friend)

    // Start measuring total computation time
    double start_time = MPI_Wtime();

    if (rank == 0) {
        // ================= STUDENT 1 =================
        
        // Step 1a & 1b: Compute alpha values
        long long alpha_prime = grinder(A, 31, 17, 9973);
        long long alpha_double_prime = grinder(alpha_prime, 37, 11, 9973);
        
        // Step 1c: Compute final alpha
        long long alpha = (alpha_prime + alpha_double_prime) % 9973;

        // Transmit alpha to Student 2
        MPI_Send(&alpha, 1, MPI_LONG_LONG, 1, 0, MPI_COMM_WORLD);

        // Receive beta from Student 2
        long long beta;
        MPI_Recv(&beta, 1, MPI_LONG_LONG, 1, 0, MPI_COMM_WORLD, MPI_STATUS_IGNORE);

        // Step 3: Verify (Both compute this)
        long long verify = grinder(alpha + beta, 7, 3, 101);
        cout << "[Student 1] Verification Value: " << verify << endl;

        // Step 4: Compute R
        long long R = grinder(alpha * beta + A + B, 13, 7, 9973);
        
        // Step 5: Compute final Password
        long long password = R % 10000;

        cout << "\n>>> Operation Staff-WiFi Success! <<<" << endl;
        // Formatting to ensure it prints as exactly 4 digits (e.g., 0042)
        printf(">>> The Password is: %04lld <<<\n\n", password);

    } else if (rank == 1) {
        // ================= STUDENT 2 =================
        
        long long alpha;
        // Receive alpha from Student 1
        MPI_Recv(&alpha, 1, MPI_LONG_LONG, 0, 0, MPI_COMM_WORLD, MPI_STATUS_IGNORE);

        // Step 2a & 2b: Compute beta values
        long long beta_prime = grinder(alpha, B, 13, 9973);
        long long beta_double_prime = grinder(beta_prime, 41, 19, 9973);
        
        // Step 2c: Compute final beta
        long long beta = (beta_prime + beta_double_prime) % 9973;

        // Transmit beta to Student 1
        MPI_Send(&beta, 1, MPI_LONG_LONG, 0, 0, MPI_COMM_WORLD);

        // Step 3: Verify (Both compute this)
        long long verify = grinder(alpha + beta, 7, 3, 101);
        cout << "[Student 2] Verification Value: " << verify << endl;
    }

    // Synchronize before ending the timer
    MPI_Barrier(MPI_COMM_WORLD);
    double end_time = MPI_Wtime();

    if (rank == 0) {
        cout << "Total Computation Time: " << (end_time - start_time) << " seconds." << endl;
    }

    // Clean up and exit
    MPI_Finalize();
    return 0;
}