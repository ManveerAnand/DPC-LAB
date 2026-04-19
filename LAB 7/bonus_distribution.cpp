#include <mpi.h>
#include <iostream>

using namespace std;

int main(int argc, char **argv)
{
    MPI_Init(&argc, &argv);

    int rank, size;
    MPI_Comm_rank(MPI_COMM_WORLD, &rank);
    MPI_Comm_size(MPI_COMM_WORLD, &size);

    int bonus;
    int base_salary = 20000;

    if (rank == 0)
    {
        bonus = 5000;
        cout << "HR Manager: Announcing bonus = " << bonus << endl;
    }

    MPI_Bcast(&bonus, 1, MPI_INT, 0, MPI_COMM_WORLD);

    int final_salary = base_salary + bonus + (rank * 1000);
    cout << "Employee (Process " << rank << ") received bonus = " << bonus
         << " and final salary = " << final_salary << endl;

    MPI_Finalize();
    return 0;
}
