#include <mpi.h>
#include <iostream>

using namespace std;

int main(int argc, char **argv)
{
    MPI_Init(&argc, &argv);

    int rank;
    MPI_Comm_rank(MPI_COMM_WORLD, &rank);

    int order_amount;
    MPI_Status status;

    if (rank == 0)
    {
        order_amount = 1000;
        cout << "Manager: Sending order amount = " << order_amount << endl;
        MPI_Send(&order_amount, 1, MPI_INT, 1, 0, MPI_COMM_WORLD);

        MPI_Recv(&order_amount, 1, MPI_INT, 1, 1, MPI_COMM_WORLD, &status);
        cout << "Manager: Received final bill after discount = " << order_amount << endl;
    }
    else if (rank == 1)
    {
        MPI_Recv(&order_amount, 1, MPI_INT, 0, 0, MPI_COMM_WORLD, &status);
        cout << "Worker: Received order amount = " << order_amount << endl;

        int discount = order_amount * 10 / 100;
        int final_bill = order_amount - discount;

        cout << "Worker: Final bill after 10% discount = " << final_bill << endl;
        MPI_Send(&final_bill, 1, MPI_INT, 0, 1, MPI_COMM_WORLD);
    }

    MPI_Finalize();
    return 0;
}
