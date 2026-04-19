#include <stdio.h>
#include <cuda_runtime.h>
#include <device_launch_parameters.h>

#define N 10
#define BINS 5

__global__ void histogramKernel(const int *data, int *hist)
{
    int i = blockIdx.x * blockDim.x + threadIdx.x;
    if (i < N)
    {
        atomicAdd(&hist[data[i]], 1);
    }
}

int main()
{
    int data[N] = {1, 2, 1, 3, 2, 4, 0, 1, 3, 2};
    int hist[BINS] = {0};

    int *d_data = nullptr;
    int *d_hist = nullptr;

    cudaMalloc((void **)&d_data, N * sizeof(int));
    cudaMalloc((void **)&d_hist, BINS * sizeof(int));

    cudaMemcpy(d_data, data, N * sizeof(int), cudaMemcpyHostToDevice);
    cudaMemcpy(d_hist, hist, BINS * sizeof(int), cudaMemcpyHostToDevice);

    int threads = 256;
    int blocks = (N + threads - 1) / threads;
    histogramKernel<<<blocks, threads>>>(d_data, d_hist);
    cudaDeviceSynchronize();

    cudaMemcpy(hist, d_hist, BINS * sizeof(int), cudaMemcpyDeviceToHost);

    printf("Histogram Result:\n");
    for (int i = 0; i < BINS; i++)
    {
        printf("Value %d : %d\n", i, hist[i]);
    }

    cudaFree(d_data);
    cudaFree(d_hist);

    return 0;
}
