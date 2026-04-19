#include <stdio.h>
#include <mpi.h>

int main(int argc, char *argv[]) {
    int rank, size, name_len;
    char processor_name[MPI_MAX_PROCESSOR_NAME];

    // Initialize the MPI environment
    MPI_Init(&argc, &argv);

    // Get the total number of processes
    MPI_Comm_size(MPI_COMM_WORLD, &size);

    // Get the rank (ID) of the current process
    MPI_Comm_rank(MPI_COMM_WORLD, &rank);

    // Get the name of the processor
    MPI_Get_processor_name(processor_name, &name_len);

    printf("Hello from process %d of %d on %s\n", rank, size, processor_name);

    // Finalize the MPI environment
    MPI_Finalize();

    return 0;
}