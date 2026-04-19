#include <stdio.h>
#include <cuda_runtime.h>
#include <device_launch_parameters.h>

#define N 8

__global__ void prefixSumKernel(const int *input, int *output)
{
    __shared__ int temp[N];

    int tid = threadIdx.x;
    temp[tid] = input[tid];

    __syncthreads();

    for (int stride = 1; stride < N; stride *= 2)
    {
        int val = 0;
        if (tid >= stride)
        {
            val = temp[tid - stride];
        }

        __syncthreads();
        temp[tid] += val;
        __syncthreads();
    }

    output[tid] = temp[tid];
}

int main()
{
    int arr[N] = {1, 2, 3, 4, 5, 6, 7, 8};
    int result[N] = {0};

    int *d_arr = nullptr;
    int *d_result = nullptr;

    cudaMalloc((void **)&d_arr, N * sizeof(int));
    cudaMalloc((void **)&d_result, N * sizeof(int));

    cudaMemcpy(d_arr, arr, N * sizeof(int), cudaMemcpyHostToDevice);

    prefixSumKernel<<<1, N>>>(d_arr, d_result);
    cudaDeviceSynchronize();

    cudaMemcpy(result, d_result, N * sizeof(int), cudaMemcpyDeviceToHost);

    printf("Input:\n");
    for (int i = 0; i < N; i++)
    {
        printf("%d ", arr[i]);
    }
    printf("\n");

    printf("Prefix Sum:\n");
    for (int i = 0; i < N; i++)
    {
        printf("%d ", result[i]);
    }
    printf("\n");

    cudaFree(d_arr);
    cudaFree(d_result);

    return 0;
}
