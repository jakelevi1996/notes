# Notes on PyTorch

## Installing PyTorch

- Instructions for installing PyTorch can be found [here](https://pytorch.org/get-started/locally/)
- In particular, PyTorch can be downloaded using `pip`
- PyTorch has different versions depending on if the installation is to have both GPU and CPU support or only CPU support, and if the installation is to have GPU support, there are further different versions of PyTorch depending on the version of CUDA
- At the time of writing, the most recent version of CUDA which is supported by a version of PyTorch is CUDA 11.7
- The different versions of CUDA are available to download [here](https://developer.nvidia.com/cuda-toolkit-archive)
- In particular, I downloaded CUDA 11.7.1 (available for download [here](https://developer.nvidia.com/cuda-11-7-1-download-archive)
- During the installation process, the installer states that Visual Studio is required, but doesn't specify which packages within Visual Studio are required
- [This post on the Nvidia developer forum](https://forums.developer.nvidia.com/t/visual-studio-2019-minimal-components-needed-for-cuda-10-installation/81899) suggests that the C++ development workload ("Desktop Development with C++") is "the only one required", however this workload alone requires about 8 GB of storage space
- In the end, I assumed Visual Studio would only be required for CUDA compilation with `nvcc`, but that PyTorch would come with pre-compiled binaries for GPU integration and would only require access to CUDA runtimes and not CUDA compilation, and therefore `nvcc` and by extension Visual Studio wouldn't be required, so I didn't install Visual Studio
- I then installed PyTorch (version `1.13.0+cu117`) with the following commands:

```
python -m pip install -U pip
python -m pip install torch torchvision torchaudio --extra-index-url https://download.pytorch.org/whl/cu117
```

This installation appears to work fine, and commands such as `torch.cuda.is_available()` and `torch.tensor([2.,3,4], requires_grad=True).cuda()` return results suggesting that GPU support is working successfully.
