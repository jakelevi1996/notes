# Notes on "CUDA by Example" by Jason Sanders and Edward Kandrot

## Contents

- [Notes on "CUDA by Example" by Jason Sanders and Edward Kandrot](#notes-on-cuda-by-example-by-jason-sanders-and-edward-kandrot)
  - [Contents](#contents)
  - [Introduction](#introduction)
  - [General tips about CUDA](#general-tips-about-cuda)
  - [Functions and kernels](#functions-and-kernels)
  - [Blocks and threads](#blocks-and-threads)
  - [Allocating, copying and releasing memory](#allocating-copying-and-releasing-memory)
  - [Reductions](#reductions)
  - [Profiling](#profiling)
  - [Constant memory](#constant-memory)
  - [Atomics](#atomics)
  - [Streams](#streams)
  - [...](#)

## Introduction

"CUDA by Example" is a book by Jason Sanders and Edward Kandrot which explains the fundamentals of programming NVidia GPUs using CUDA. The homepage for the book is [here](https://developer.nvidia.com/cuda-example), from which all of the source code from the book can be downloaded (I found that for some reason I couldn't download the source code using the Google Chrome web browser, but I was able to download the source code using the Microsoft Edge web broswer). All of the code from the book can be compiled and run on a GPU such as a [Jetson Nano Developer Kit](https://developer.nvidia.com/embedded/jetson-nano-developer-kit) (although note that some examples require additional compiler flags, EG `-lGL -lGLU -lglut` for the Julia Set examples from chapter 4 of the book).

Before starting, make sure that `nvcc` is present on your system path. On a freshly set up Jetson Nano Developer Kit, this involves appending `PATH=$PATH:/usr/local/cuda-10.2/bin/` to the end of `~/.bashrc`, but apart from this, a freshly set up Jetson Nano Developer Kit supports everything required for `nvcc`, `ssh`, `rsync`, and X11 forwarding to view graphical interfaces over `ssh`, although it may be necessary to run the command `export DISPLAY=localhost:0.0` on a local WSL machine connecting to a Jetson Nano over `ssh`.

The CUDA language features (keywords, function names, etc) specified below are all built-in to CUDA (IE don't require including a specific header file), unless otherwise specified. Filenames are assumed to refer to the source code for the book, which can be downloaded from the above link to the book's website.

## General tips about CUDA

- To write a CUDA source file, use the filename suffix `.cu`
- Use `nvcc` to compile a CUDA source file, EG `nvcc main.cu -o main`
- A program compiled using `nvcc` is run exactly the same as a normal program, EG `./main`
- To get information about all GPU devices currently available on a given machine, compile and run `cuda_by_example/chapter03/enum_gpu.cu`, which prints information to `stdout` such as device name, compute capability, clock rate, total global and constant memory, the maximum number of threads per block, the maximum thread dimensions, and the maximum grid size

## Functions and kernels

- A normal C-style function in a CUDA source file will run on the CPU unless otherwise specified
- The `main` function should run on the CPU
- A CUDA kernel is a function that can run on GPU hardware
- To define a kernel that can be called from both the CPU and GPU, prepend the function definition with the keyword `__global__`, EG `__global__ void add( int *a, int *b, int *c ) {...`
- To define a kernel that can only be called from functions running on the GPU, prepend the function definition with the keyword `__device__` (this keyword can also be used for functions defined within a `struct`)
- To call a global kernel from a CPU function, use triple angle brackets, EG `add<<<N,1>>>( dev_a, dev_b, dev_c );`

## Blocks and threads

- When calling a CUDA kernel using angle bracket notation, the first number in the angle brackets refers to the number of blocks, and the second number refers to the number of threads
- Often it is useful at the start of a kernel to calculate an index which is specific to each thread, and is used to decide which element of the inputs/outputs to process
  - This is achieved using:
    - The index of the thread within the block, EG `threadIdx.x`
    - The index of the block within the grid, EG `blockIdx.x`
    - The dimensions of each block of threads, EG `blockDim.x`
    - The dimensions of the grid of blocks, EG `gridDim.x`
  - With 1D arrays of blocks and threads, it is possible to get a unique index for each thread in the program using the expression `int tid = threadIdx.x + blockIdx.x * blockDim.x;`
    - In this example, if there are more elements to be processed than there are threads and blocks, the thread index can be incremented in a loop (EG while `tid` is less than the total number of elements to be processed) using the expression `tid += blockDim.x * gridDim.x;`
  - If there is only 1 thread per block and a 1D array of blocks, we can simply use `int tid = blockIdx.x;`, and increment `tid` in a loop while it is less than the number of elements to be processed using the expression `tid += gridDim.x;`
- Threads can use memory which is shared between threads, but not between blocks, by declaring the memory using the `__shared__` keyword, EG `__shared__ float cache[threadsPerBlock];`
- Threads can wait for other threads within the same block to finish processing using the `__syncthreads()` function, which is useful for example for performing reductions (such as dot products)
- It is possible to define higher dimensional arrays of blocks and threads, by declaring a `dim3` variable (which represents a 3D tuple) and passing it to the kernel call, for example `dim3 blocks(DIM/16,DIM/16); dim3 threads(16,16); kernel<<<blocks,threads>>>( d->dev_bitmap, ticks );`
  - This might be useful for example if processing all pixels of an image in parallel
  - In this case, the offset for each thread can be calculated as follows: `int x = threadIdx.x + blockIdx.x * blockDim.x; int y = threadIdx.y + blockIdx.y * blockDim.y; int offset = x + y * blockDim.x * gridDim.x;`


## Allocating, copying and releasing memory

- To allocate memory on the GPU, use the `cudaMalloc` function, which accepts the address of a pointer (a pointer to a pointer) for the memory, and the number of bytes to by allocated, EG `int *dev_a; cudaMalloc( (void**)&dev_a, N * sizeof(int) )`
- To copy memory from an array on the CPU to an array on the GPU, use the `cudaMemcpy` function with the `cudaMemcpyHostToDevice` keyword, EG `int a[N]; cudaMemcpy( dev_a, a, N * sizeof(int), cudaMemcpyHostToDevice ) );` (assuming that `dev_a` has been declared and allocated as described in the previous example)
- To copy memory from an array on the GPU to an array on the CPU, use the `cudaMemcpy` function with the `cudaMemcpyDeviceToHost` keyword, EG `cudaMemcpy( c, dev_c, N * sizeof(int), cudaMemcpyDeviceToHost ) )`
- To free allocated GPU memory, use the `cudaFree` function, EG `cudaFree( dev_a )`

## Reductions

- When the number of outputs is proportional to the number of inputs (EG when adding two vectors together element-wise, or evaluating a function at every point in an array), a GPU can hypothetically calculate the answer in constant time, independent of the number of inputs, if it has enough internal parallel processing units, by assigning one thread/processing unit to each element of the input/output data
- Summing over all the values in an array to produce a scalar output is a fundamentally different type of operation that cannot be performed in constant time, even with an infinite number of internal parallel processing units
- This type of computation which takes an input array and operates on all the elements to produce a smaller array is called a reduction
- Naively, a reduction such as summing an array could be performed by a single thread and a single processing unit by adding up each element one by one, in time which is proportional to the length of the input array
- Such a reduction can be performed more efficiently in time that is proportional to the logarithm of the length of the input array
- An example implementation of a dot-product can be found in `cuda_by_example/chapter05/dot.cu`, which demonstrates how to implement a reduction efficiently

## Profiling

## Constant memory

## Atomics

## Streams

## ...
