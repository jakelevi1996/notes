# Notes on "CUDA by Example" by Jason Sanders and Edward Kandrot

"CUDA by Example" is a book by Jason Sanders and Edward Kandrot which explains the fundamentals of programming NVidia GPUs using CUDA. The homepage for the book is [here](https://developer.nvidia.com/cuda-example), from which all of the source code from the book can be downloaded (I found that for some reason I couldn't download the source code using the Google Chrome web browser, but I was able to download the source code using the Microsoft Edge web broswer). All of the code from the book can be compiled and run on a GPU such as a [Jetson Nano Developer Kit](https://developer.nvidia.com/embedded/jetson-nano-developer-kit) (although note that some examples require additional compiler flags, EG `-lGL -lGLU -lglut` for the Julia Set examples from chapter 4 of the book).

Before starting, make sure that `nvcc` is present on your system path. On a freshly set up Jetson Nano Developer Kit, this involves appending `PATH=$PATH:/usr/local/cuda-10.2/bin/` to the end of `~/.bashrc`, but apart from this, a freshly set up Jetson Nano Developer Kit supports everything required for `nvcc`, `ssh`, `rsync`, and X11 forwarding to view graphical interfaces over `ssh`, although it may be necessary to run the command `export DISPLAY=localhost:0.0` on a local WSL machine connecting to a Jetson Nano over `ssh`.

The CUDA language features (keywords, function names, etc) specified below are all built-in to CUDA (IE don't require including a specific header file), unless otherwise specified.

- To write a CUDA source file, use the filename suffix `.cu`
- A C-style function in a CUDA source file will run on the CPU unless otherwise specified
- The `main` function should run on the CPU
- A CUDA kernel is a function that can run on GPU hardware
- To define a kernel that can be called from both the CPU and GPU, prepend the function definition with the keyword `__global__`, EG `__global__ void add( int *a, int *b, int *c ) {...`
- To define a kernel that can only be called from functions running on the GPU, prepend the function definition with the keyword `__device__` 
- To call a global kernel from a CPU function, use triple angle brackets, EG `add<<<N,1>>>( dev_a, dev_b, dev_c );`
  - The first number in the angle brackets refers to the number of blocks, and the second number refers to the number of threads
  - Threads can use memory which is shared between threads, but not between blocks, by declaring the memory using the `__shared__` keyword, EG `__shared__ float cache[threadsPerBlock];`
  - Threads can wait for other threads within the same block to finish processing using the `__syncthreads()` function, which is useful for example for performing reductions (such as dot products)
- ...
