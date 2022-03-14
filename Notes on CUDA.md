# Notes on Cuda

This Gist contains notes and useful links about programming in Cuda, a language based on C/C++ for general purpose programming on Nvidia GPUs. Much of these notes are based on the book ["CUDA by Example"](https://developer.nvidia.com/cuda-example) by Jason Sanders and Edward Kandrot. There is also an example Cuda program, notes on [Thrust](https://docs.nvidia.com/cuda/thrust/index.html) ("the CUDA C++ template library"), and miscellaneous topics.

## Contents

- [Notes on Cuda](#notes-on-cuda)
  - [Contents](#contents)
  - [General tips about CUDA](#general-tips-about-cuda)
  - [Example Cuda progrm](#example-cuda-progrm)
  - [Useful links](#useful-links)
  - [Notes on "CUDA by Example" by Jason Sanders and Edward Kandrot](#notes-on-cuda-by-example-by-jason-sanders-and-edward-kandrot)
    - [Introduction](#introduction)
    - [General tips about CUDA (specifically from "CUDA by Example")](#general-tips-about-cuda-specifically-from-cuda-by-example)
    - [Functions and kernels (chapter 3)](#functions-and-kernels-chapter-3)
    - [Allocating, copying and releasing memory (chapter 3)](#allocating-copying-and-releasing-memory-chapter-3)
    - [Blocks and threads (chapters 4 and 5)](#blocks-and-threads-chapters-4-and-5)
    - [Reductions (chapter 5)](#reductions-chapter-5)
    - [Profiling (chapter 6)](#profiling-chapter-6)
    - [Constant memory (chapter 6)](#constant-memory-chapter-6)
    - [Atomics (chapter 9)](#atomics-chapter-9)
    - [Streams (chapter 10)](#streams-chapter-10)
    - [Multiple GPUs (chapter 11)](#multiple-gpus-chapter-11)
    - [...](#)
  - [Error checking](#error-checking)
  - [Thrust](#thrust)
    - [General notes about Thrust](#general-notes-about-thrust)
    - [Calculating mean and variance using Thrust](#calculating-mean-and-variance-using-thrust)

## General tips about CUDA

- To write a CUDA source file, use the filename suffix `.cu`
- Use `nvcc` to compile a CUDA source file, EG `nvcc main.cu -o main`
- A program compiled using `nvcc` is run exactly the same as a normal program, EG `./main`
- Cuda kernels are prefixed with the keyword `__global__` and must always return `void`
- Any pointer which is passed to a Cuda kernel should point to device (GPU) memory; otherwise the program may fail silently, and parts of the program may simply not execute

## Example Cuda progrm

Below is an example Cuda program, which calculates the square of each element in a vector of doubles. This example demonstrates some major, commonly used components, such as defining a Cuda kernel, launching a Cuda kernel, device (GPU) memory allocation, copying memory between the device and the host (CPU), freeing GPU memory, and profiling. If the code is saved in a file called `square_vector.cu`, it can be compiled and run with the command `nvcc square_vector.cu -o square_vector && square_vector`. For an input vector size of `N = 10000` on a Jetson Nano dev board this took 0.168 ms vs 0.192 ms for an equivalent program using the CPU, whereas for an input vector size of `N = 100000` this took 0.597 ms on the GPU vs 1.72 ms on the CPU.

```c
#include "stdio.h"

#define N (10000)
#define THREADS_PER_BLOCK (256)
#define CEIL_DIV(a, b) (((a) + (b) - 1) / (b))

/* Define profiling macros */
#define PROFILING_INIT                                              \
    cudaEvent_t start, stop;                                        \
    float elapsedTime;

#define PROFILING_START                                             \
    cudaEventCreate(&start);                                        \
    cudaEventCreate(&stop);                                         \
    cudaEventRecord(start, 0);

#define PROFILING_STOP                                              \
    cudaEventRecord(stop, 0);                                       \
    cudaEventSynchronize(stop);                                     \
    cudaEventElapsedTime(&elapsedTime, start, stop);                \
    printf("Time elapsed:  %.3g ms\n", elapsedTime);

/* Define the Cuda kernel */
__global__ void square_vector(double* data_in, double* data_out, int n) {
    int thread_start_idx = threadIdx.x + blockIdx.x * blockDim.x;
    int stride = blockDim.x * gridDim.x;
    for (
        int i = thread_start_idx;
        i < n;
        i += stride
    ) {
        data_out[i] = data_in[i] * data_in[i];
    }
}

/* Allocate host (CPU) inputs and outputs */
double data_in[N];
double data_out[N];

int main() {
    /* Initialise inputs */
    for (int i = 0; i < N; i++) {
        data_in[i] = (double) i;
    }

    /* Allocate device memory for inputs and outputs, and copy input data from
    host to device memory */
    double *dev_data_in;
    cudaMalloc((void**) &dev_data_in, N * sizeof(double));
    cudaMemcpy(dev_data_in, data_in, N * sizeof(double), cudaMemcpyHostToDevice);

    double *dev_data_out;
    cudaMalloc((void**) &dev_data_out, N * sizeof(double));

    /* Initialise profiling */
    PROFILING_INIT;
    PROFILING_START;

    /* Call the Cuda kernel */
    square_vector<<<CEIL_DIV(N, THREADS_PER_BLOCK), THREADS_PER_BLOCK>>>(
        dev_data_in,
        dev_data_out,
        N
    );

    /* Stop profiling and print the running time */
    PROFILING_STOP;

    /* Copy output data from device back to host memory */
    cudaMemcpy(data_out, dev_data_out, N * sizeof(double), cudaMemcpyDeviceToHost);

    /* Compare actual output with expected output */
    for (int i = 0; i < N; i++) {
        if (data_out[i] != (data_in[i] * data_in[i])) {
            printf(
                "Fail: element %i was %.1f, expected %.1f\n",
                i,
                data_out[i],
                data_in[i] * data_in[i]
            );
        }
    }

    /* Free allocated device memory */
    cudaFree(dev_data_in);
    cudaFree(dev_data_out);

}
```

## Useful links

- [Unified Memory for CUDA Beginners](https://developer.nvidia.com/blog/unified-memory-cuda-beginners/)
- [An Even Easier Introduction to CUDA](https://developer.nvidia.com/blog/even-easier-introduction-cuda/) (including profiling with [`nvprof`](https://docs.nvidia.com/cuda/profiler-users-guide/index.html))
- NVidia official [CUDA Samples](https://github.com/nvidia/cuda-samples)
- [Homepage for "CUDA by Example"](https://developer.nvidia.com/cuda-example)
- Thrust
  - [API reference guide](https://docs.nvidia.com/cuda/thrust/index.html)
  - [Full API documentation](https://nvidia.github.io/thrust/api.html)

## Notes on "CUDA by Example" by Jason Sanders and Edward Kandrot

### Introduction

"CUDA by Example" is a book by Jason Sanders and Edward Kandrot which explains the fundamentals of programming NVidia GPUs using CUDA. The homepage for the book is [here](https://developer.nvidia.com/cuda-example), from which all of the source code from the book can be downloaded (I found that for some reason I couldn't download the source code using the Google Chrome web browser, but I was able to download the source code using the Microsoft Edge web broswer). All of the code from the book can be compiled and run on a GPU such as a [Jetson Nano Developer Kit](https://developer.nvidia.com/embedded/jetson-nano-developer-kit) (although note that some examples require additional compiler flags, EG `-lGL -lGLU -lglut` for the Julia Set examples from chapter 4 of the book).

Before starting, make sure that `nvcc` is present on your system path. On a freshly set up Jetson Nano Developer Kit, this involves appending `PATH=$PATH:/usr/local/cuda-10.2/bin/` to the end of `~/.bashrc`, but apart from this, a freshly set up Jetson Nano Developer Kit supports everything required for `nvcc`, `ssh`, `rsync`, and X11 forwarding to view graphical interfaces over `ssh` (although it may be necessary to run the command `export DISPLAY=localhost:0.0` on a local WSL machine connecting to a Jetson Nano over `ssh` with X11 forwarding).

The CUDA language features (keywords, function names, etc) specified below are all built-in to CUDA (IE don't require including a specific header file), unless otherwise specified. Filenames are assumed to refer to the source code for the book, which can be downloaded from the above link to the book's website.

### General tips about CUDA (specifically from "CUDA by Example")

- To get information about all GPU devices currently available on a given machine, compile and run `cuda_by_example/chapter03/enum_gpu.cu`, which prints information to `stdout` such as device name, compute capability, clock rate, total global and constant memory, the maximum number of threads per block, the maximum thread dimensions, and the maximum grid size
- Error checking is important for calls to built-in Cuda functions
  - Many built-in Cuda functions (EG for GPU memory allocation) return a variable of type `cudaError_t`, indicating if they were successful or not
  - If the return code is not equal to `cudaSuccess`, then this indicates that an error occured
  - If an error occured, an error string can be acquired by passing the return code to `cudaGetErrorString(code)`
  - For example, within a Cuda error-checking function, this error code might be printed to `stderr`, along with the filename and line of the function call, after which the error-checking function could call `exit( EXIT_FAILURE )` or `exit(code)`
  - The filename and line number of the error can be passed to the error-checking function by wrapping it in a macro function, accepts the error code and calls the error-checking function with the error code as well as `__FILE__` and `__LINE__`

### Functions and kernels (chapter 3)

- A normal C-style function in a CUDA source file will run on the CPU unless otherwise specified
- The `main` function should run on the CPU
- A CUDA kernel is a function that can run on GPU hardware
- To define a kernel that can be called from both the CPU and GPU, prepend the function definition with the keyword `__global__`, EG `__global__ void add( int *a, int *b, int *c ) {...}`
- To define a kernel that can only be called from functions running on the GPU, prepend the function definition with the keyword `__device__` (this keyword can also be used for functions defined within a `struct`, as demonstrated in section 4.2.2 of the book)
- To call a global kernel from a CPU function, use triple angle brackets, EG `add<<<N,1>>>( dev_a, dev_b, dev_c );`

### Allocating, copying and releasing memory (chapter 3)

- To allocate memory on the GPU, use the `cudaMalloc` function, which accepts the address of a pointer (a pointer to a pointer) for the memory, and the number of bytes to by allocated, EG `int *dev_a; cudaMalloc( (void**)&dev_a, N * sizeof(int) )`
  - After calling `cudaMalloc`, `dev_a` will now point to a correctly sized buffer on the GPU
- To copy memory from an array on the CPU to an array on the GPU, use the `cudaMemcpy` function with the `cudaMemcpyHostToDevice` keyword, EG `int a[N]; cudaMemcpy( dev_a, a, N * sizeof(int), cudaMemcpyHostToDevice );` (assuming that `dev_a` has been declared and allocated as described in the previous example)
- To copy memory from an array on the GPU to an array on the CPU, use the `cudaMemcpy` function with the `cudaMemcpyDeviceToHost` keyword, EG `cudaMemcpy( c, dev_c, N * sizeof(int), cudaMemcpyDeviceToHost )`
- To free allocated GPU memory, use the `cudaFree` function, EG `cudaFree( dev_a )`

### Blocks and threads (chapters 4 and 5)

- When calling a CUDA kernel using angle bracket notation, the first number in the angle brackets refers to the number of blocks, and the second number refers to the number of threads
- Often it is useful at the start of a kernel to calculate an index which is specific to each thread, and is used to decide which element of the inputs/outputs to process in the thread which is currently executing
  - This is achieved using:
    - The index of the thread within the block, EG `threadIdx.x`
    - The index of the block within the grid, EG `blockIdx.x`
    - The dimensions of each block of threads, EG `blockDim.x`
    - The dimensions of the grid of blocks, EG `gridDim.x`
  - With 1D arrays of blocks and threads, it is possible to get a unique index for each thread in the program using the expression `int tid = threadIdx.x + blockIdx.x * blockDim.x;`
    - In this example, if there are more elements to be processed than there are threads and blocks, the thread index can be incremented in a loop (EG while `tid` is less than the total number of elements to be processed) using the expression `tid += blockDim.x * gridDim.x;`
  - If there is only 1 thread per block and a 1D array of blocks, we can simply use `int tid = blockIdx.x;`, and increment `tid` in a loop while it is less than the number of elements to be processed using the expression `tid += gridDim.x;`
    - Note that using only 1 thread per block is likely to perform more slowly than using many threads per block (EG 256)
- Threads can use memory which is shared between threads, but not between blocks, by declaring the memory using the `__shared__` keyword, EG `__shared__ float cache[threadsPerBlock];`
- Threads can wait for other threads within the same block to finish processing using the `__syncthreads()` function, which is useful for example for performing reductions (see section [Reductions](#reductions) below)
- It is possible to define higher dimensional arrays of blocks and threads, by declaring a `dim3` variable (which represents a 3D tuple) and passing it to the kernel call, for example `dim3 blocks(DIM/16,DIM/16); dim3 threads(16,16); kernel<<<blocks,threads>>>( d->dev_bitmap, ticks );`
  - This might be useful for example if processing all pixels of an image in parallel
  - In this case, the offset for each thread can be calculated as follows: `int x = threadIdx.x + blockIdx.x * blockDim.x; int y = threadIdx.y + blockIdx.y * blockDim.y; int offset = x + y * blockDim.x * gridDim.x;`
- There is a limit to the number of blocks and threads that can be launched
  - The maximum number of blocks is 65,535 (according to section 4.2.1 of the book, this is a hardware-imposed limit)
  - The maximum number of threads per block is platform-specific (the maximum number of threads on the Jetson Nano is 1024, whereas section 5.2.1 of the book states that "For many of the graphics processors currently available, this limit is 512 threads per block")

### Reductions (chapter 5)

- When the number of outputs is proportional to the number of inputs (EG when adding two vectors together element-wise, or evaluating a function at every point in an array), a GPU can hypothetically calculate the answer in constant time, independent of the number of inputs, if it has enough internal parallel processing units, by assigning one thread/processing unit to each element of the input/output data
- Summing over all the values in an array to produce a scalar output is a fundamentally different type of operation that cannot be performed in constant time, even with an infinite number of internal parallel processing units
- This type of computation which takes an input array and operates on all the elements to produce a smaller array is called a reduction
- Naively, a reduction such as summing an array could be performed by a single thread and a single processing unit by adding up each element one by one, in time which is proportional to the length of the input array
- Such a reduction can be performed more efficiently in time that is proportional to the logarithm of the length of the input array, using shared memory and thread synchronisation (using the `__shared__` keyword and the `__syncthreads()` function mentioned above)
- An example of a kernel which calculates the dot-product of 2 arrays can be found in `cuda_by_example/chapter05/dot.cu`, which demonstrates how to implement a reduction efficiently

### Profiling (chapter 6)

- To initialise GPU profiling (which can be used to profile kernel calls, copying memory between the CPU and GPU, etc):

Instruction | Code
--- | ---
Declare the following variables | `cudaEvent_t start, stop; float elapsedTime;`
Initialise the Cuda event variables | `cudaEventCreate( &start ); cudaEventCreate( &stop );`
Record the start of the profiling | `cudaEventRecord( start, 0 );`
Perform code which is to be profiled |
Record the end of the profiling | `cudaEventRecord( stop, 0 );`
Synchronise the CPU with the GPU | `cudaEventSynchronize( stop );`
Calculate the elapsed time | `cudaEventElapsedTime( &elapsedTime, start, stop )`
Free the memory created by `cudaEventCreate` | `cudaEventDestroy( start ); cudaEventDestroy( stop )`
Print the elapsed time | `printf( "Time elapsed: %3.1f ms\n", elapsedTime );`

This set of commands can be followed up into 3 macros as follows:

```c
/* *** PROFILING MACROS *** */
/* Initialise profiling: use this macro once per function before calling
PROFILING_START and PROFILING_STOP */
#define PROFILING_INIT                                              \
    cudaEvent_t start, stop;                                        \
    float elapsedTime;

/* Record the start time for profiling: use this macro immediately before any
call(s) that are to be profiled */
#define PROFILING_START                                             \
    cudaEventCreate(&start);                                        \
    cudaEventCreate(&stop);                                         \
    cudaEventRecord(start, 0);

/* Record the stop time for profiling: use this macro immediately after any
call(s) that are to be profiled */
#define PROFILING_STOP                                              \
    cudaEventRecord(stop, 0);                                       \
    cudaEventSynchronize(stop);                                     \
    cudaEventElapsedTime(&elapsedTime, start, stop);                \
    printf("Time elapsed:  %.3g ms\n", elapsedTime);
```

These macros can be used as follows:

```c
int main() {
    PROFILING_INIT;

    PROFILING_START;
    my_kernel<<<4096, 256>>>();
    PROFILING_STOP;

    PROFILING_START;
    my_kernel<<<2048, 512>>>();
    PROFILING_STOP;
}
```

### Constant memory (chapter 6)

### Atomics (chapter 9)

### Streams (chapter 10)

### Multiple GPUs (chapter 11)

### ...

## Error checking

In addition to the notes on error checking mentioned above in the context of the "CUDA By Example" book, [this Stack Overflow answer](https://stackoverflow.com/a/6420012/8477566) provides a useful method for checking if an error occured during a kernel call:

```c
kernel<<<blocks, threads>>>(params);
cudaError_t err = cudaGetLastError();
if (err != cudaSuccess)
    printf("Error: %s\n", cudaGetErrorString(err));
```

Cuda memory errors can be investigated using [CUDA-MEMCHECK](https://docs.nvidia.com/cuda/cuda-memcheck/index.html), which in the simplest case can be used by just calling `cuda-memcheck` along with the name of the executable:

```
nvcc app_name.cu -o app_name
cuda-memcheck app_name
```

## Thrust

As stated in the documentation, "Thrust is a C++ template library for CUDA based on the Standard Template Library (STL). Thrust allows you to implement high performance parallel applications with minimal programming effort through a high-level interface that is fully interoperable with CUDA C. Thrust provides a rich collection of data parallel primitives such as scan, sort, and reduce, which can be composed together to implement complex algorithms with concise, readable source code."

The API reference guide for Thrust can be found [here](https://docs.nvidia.com/cuda/thrust/index.html), and the full API documentation can be found [here](https://nvidia.github.io/thrust/api.html).

### General notes about Thrust

- Thrust functions can't be called from inside a Cuda kernel, they can only be called from host (CPU) functions ([source](https://stackoverflow.com/a/17814466/8477566))
- Thrust is based on the Standard Template Library (STL), and many Thrust functions correspond to an analogous STL function, EG [`thrust::transform`](https://nvidia.github.io/thrust/api/groups/group__transformations.html#function-transform) and [`std::transform`](https://www.cplusplus.com/reference/algorithm/transform/)
- Many Thrust functions accept instances of [functors](https://stackoverflow.com/a/356993/8477566), which are essentially classes which define `operator()` (IE are callable, see example below)
- Generalised reductions, transformed reductions, and inner products can be performed using [`thrust::reduce`](https://nvidia.github.io/thrust/api/groups/group__reductions.html#function-reduce), [`thrust::transform_reduce`](https://nvidia.github.io/thrust/api/groups/group__transformed__reductions.html#function-transform-reduce), and [`thrust::inner_product`](https://nvidia.github.io/thrust/api/groups/group__transformed__reductions.html#function-inner-product), which might be useful EG if generalising existing Thrust functions to complex numbers
- Stream Compaction is an established solved problem which refers to removing all elements from an array which don't satisfy a certain condition, and can be achieved using [`thrust::copy_if`](https://nvidia.github.io/thrust/api/groups/group__stream__compaction.html#function-copy-if), which is found in the [Thrust API documentation](https://nvidia.github.io/thrust/) at API/Algorithms/Reordering/Stream Compaction
- If a Thrust vector is initialised (EG with `thrust::device_vector<double> dev_data_in(N);`), sometimes it can be useful to cast this vector to a raw pointer (EG for compatibility with other inputs to a template function), which can be performed with an expression such as `(double*) thrust::raw_pointer_cast(&dev_data_in[0])`, or the vector can be cast to a `thrust::device_ptr<double>` with the expression `thrust::device_pointer_cast(&dev_data_in[0])`
- Many Thrust functions are template functions, and can accept many combinations of different input types, including iterators of Thrust vectors and/or raw pointers (as long as they point to the correct location in host or device memory), however often it can be be easier to simply use raw pointers instead of Thrust vectors, as this can alleviate the need to appropriately cast Thrust vectors (EG using `raw_pointer_cast` or `device_pointer_cast` as described above), and also avoids having to debug complicated compiler errors (EG that are >500 lines long and overflow the terminal buffer) due to incompatibility between different template types and overloaded functions
- Thrust defines a set of [Predefined Function Objects](https://nvidia.github.io/thrust/api/groups/group__predefined__function__objects.html) (including [Arithmetic Operations](https://nvidia.github.io/thrust/api/groups/group__arithmetic__operations.html), [Comparison Operations](https://nvidia.github.io/thrust/api/groups/group__comparison__operations.html), and [Logical Operations](https://nvidia.github.io/thrust/api/groups/group__logical__operations.html)), which can be useful for implementing generalised transformations, reductions, etc

### Calculating mean and variance using Thrust

Below is an example of calculating mean and variance using Thrust:

```c++
struct square_double {
    __host__ __device__ double operator()(const double& x) const {
        return x * x;
    }
};

void mean_and_var(double* a, int n, double* p_mean, double* p_var) {
    double sum = thrust::reduce(a, &a[n], 0.0, thrust::plus<double>());
    double sum_square = thrust::transform_reduce(
        a,
        &a[n],
        square_double(),
        0.0,
        thrust::plus<double>()
    );
    double mean = sum / n;
    *p_mean = mean;
    *p_var = (sum_square / n) - mean*mean;
}
```

Here is that solution in a self-contained source file along with some profiling calculations, comparing CPU versus GPU, and device memory versus host memory in Thrust function calls:

```c++
#include "stdio.h"
#include <thrust/reduce.h>
#include <thrust/device_vector.h>

#define PROFILING_INIT                                              \
    cudaEvent_t start, stop;                                        \
    float elapsedTime;

#define PROFILING_START                                             \
    cudaEventCreate(&start);                                        \
    cudaEventCreate(&stop);                                         \
    cudaEventRecord(start, 0);

#define PROFILING_STOP                                              \
    cudaEventRecord(stop, 0);                                       \
    cudaEventSynchronize(stop);                                     \
    cudaEventElapsedTime(&elapsedTime, start, stop);                \
    printf("Time elapsed:  %.3g ms\n", elapsedTime);

#define N (6*8000)
// #define N (6*8000*10)
// #define N (6*8000*100)
double a[N];

template <typename T> struct square {
    __host__ __device__ T operator()(const T& x) const {
        return x * x;
    }
};

void mean_and_var_cpu(double* a, int n, double* p_mean, double* p_var) {
    double sum = 0, sum_square = 0, mean;
    for (int i = 0; i < n; i++) {
        sum += a[i];
        sum_square += (a[i] * a[i]);
    }
    mean = sum / n;
    *p_mean = mean;
    *p_var = (sum_square / n) - mean*mean;
}

template <typename T> void mean_and_var(T a, int n, double* p_mean, double* p_var) {
    double sum = thrust::reduce(a, &a[n], 0.0, thrust::plus<double>());
    double sum_square = thrust::transform_reduce(a, &a[n], square<double>(), 0.0, thrust::plus<double>());
    double mean = sum / n;
    *p_mean = mean;
    *p_var = (sum_square / n) - mean*mean;
}

int main() {
    for (int i = 0; i < N; i++) {
        a[i] = i;
    }

    double mean, var;

    PROFILING_INIT;

    printf("With thrust:\n");
    PROFILING_START;
    mean_and_var<double*>(a, N, &mean, &var);
    PROFILING_STOP;
    printf("Mean = %f, var = %f\n", mean, var);

    printf("With thrust, using device memory:\n");
    thrust::device_vector<double> a_dev(N);
    thrust::copy(a, &a[N], a_dev.begin());
    PROFILING_START;
    mean_and_var<thrust::device_ptr<double>>(&a_dev[0], N, &mean, &var);
    PROFILING_STOP;
    printf("Mean = %f, var = %f\n", mean, var);

    printf("On CPU:\n");
    PROFILING_START;
    mean_and_var_cpu(a, N, &mean, &var);
    PROFILING_STOP;
    printf("Mean = %f, var = %f\n", mean, var);

}
```

In all cases, the answers agree with the mean and population variance calculated using the Python `statistics` module:

```python
import statistics
x = 8000*6
print(statistics.mean(list(range(x))))
# print(statistics.variance(list(range(x))))
print(statistics.pvariance(list(range(x))))
```

Here is some profiling information, all of which was performed on a Jetson Nano development board:

N | Time taken for Thrust (ms) | Time taken for Thrust using device memory (ms) | Time taken for naive CPU implementation (ms)
--- | --- | --- | ---
6*8000 | 11.2 | 2.38 | 1.11
6\*8000\*10 | 108 | 7.62 | 11.7
6\*8000\*100 | 1.12e+03 | 41.7 | 109

Conclusions from profiling:
- If you're going to use Thrust, make sure you use device memory!
- For a large enough input size, the GPU is faster than the CPU
- For smaller input sizes, depending on the platform, it might be faster using the CPU than the GPU
