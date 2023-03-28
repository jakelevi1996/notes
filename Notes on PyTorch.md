# Notes on PyTorch

## Contents

- [Notes on PyTorch](#notes-on-pytorch)
  - [Contents](#contents)
  - [Installing PyTorch](#installing-pytorch)
  - [Using a DataLoader with a custom dataset](#using-a-dataloader-with-a-custom-dataset)

## Installing PyTorch

- Instructions for installing PyTorch can be found [here](https://pytorch.org/get-started/locally/)
- In particular, PyTorch can be downloaded using `pip`
- PyTorch has different versions depending on if the installation is to have both GPU and CPU support or only CPU support, and if the installation is to have GPU support, there are further different versions of PyTorch depending on the version of CUDA
- At the time of writing, the most recent version of CUDA which is supported by a version of PyTorch is CUDA 11.7
- The different versions of CUDA are available to download [here](https://developer.nvidia.com/cuda-toolkit-archive)
- In particular, I downloaded CUDA 11.7.1 (available for download [here](https://developer.nvidia.com/cuda-11-7-1-download-archive))
- During the installation process, the installer states that Visual Studio is required, but doesn't specify which packages within Visual Studio are required
- [This post on the Nvidia developer forum](https://forums.developer.nvidia.com/t/visual-studio-2019-minimal-components-needed-for-cuda-10-installation/81899) suggests that the C++ development workload ("Desktop Development with C++") is "the only one required", however this workload alone requires about 8 GB of storage space
- In the end, I assumed Visual Studio would only be required for CUDA compilation with `nvcc`, but that PyTorch would come with pre-compiled binaries for GPU integration and would only require access to CUDA runtimes and not CUDA compilation, and therefore `nvcc` and by extension Visual Studio wouldn't be required, so I didn't install Visual Studio
- I then installed PyTorch (version `1.13.0+cu117`) with the following commands:

```
python -m pip install -U pip
python -m pip install torch torchvision torchaudio --extra-index-url https://download.pytorch.org/whl/cu117
```

This installation appears to work fine, and commands such as `torch.cuda.is_available()` and `torch.tensor([2.,3,4], requires_grad=True).cuda()` return results suggesting that GPU support is working successfully.

## Using a DataLoader with a custom dataset

To use a `DataLoader` with a custom dataset, define a class for the dataset which is a subclass of `torch.utils.data.Dataset` ([source](https://pytorch.org/tutorials/beginner/basics/data_tutorial.html#creating-a-custom-dataset-for-your-files)), and implement the following methods:

Method name | Purpose | When it is called
--- | --- | ---
`__init__` | Initialise the dataset, including any necessary attributes used by `__len__` and `__getitem__` | When the dataset is initialised
`__len__` | Return the total number of datapoints in the dataset | Called by a `DataLoader`, with frequency that depends on if the `DataLoader` is initialised with `shuffle` equal to  `True` or `False`. If `shuffle` is `False`, `__len__` is called once at the start of each epoch. If `shuffle` is `True`, `__len__` is called twice when the `DataLoader` is initialised, and 3 times per epoch (twice at the start of the epoch, and once before or after the final batch, depending on if the number of data points is a multiple of the batch size)
`__getitem__` | Return a single data point (input and target) with the given index | Called by a `DataLoader` once for every datapoint in every batch (IE `batch_size` number of times per batch)

Below is a toy example:

```python
import torch
import numpy as np

class MockData(torch.utils.data.Dataset):
    def __init__(self, n=8):
        self._n = n
        self._x = np.arange(n)
        self._y = self._x + 100

    def __len__(self):
        print("Called len(MockData)")
        return self._n

    def __getitem__(self, index):
        print("Called MockData[%i]" % index)
        return self._x[index], self._y[index]

dataset = MockData()
data_loader = torch.utils.data.DataLoader(
    dataset=dataset,
    batch_size=3,
    shuffle=True,
)
for epoch in range(2):
    print("Epoch = %i" % epoch)
    for x, y in data_loader:
        print("Received batch x = %s, y = %s" % (x, y))
```

Output:

```
Called len(MockData)
Called len(MockData)
Epoch = 0
Called len(MockData)
Called len(MockData)
Called MockData[6]
Called MockData[1]
Called MockData[0]
Received batch x = tensor([6, 1, 0], dtype=torch.int32), y = tensor([106, 101, 100], dtype=torch.int32)
Called MockData[7]
Called MockData[5]
Called MockData[2]
Received batch x = tensor([7, 5, 2], dtype=torch.int32), y = tensor([107, 105, 102], dtype=torch.int32)
Called len(MockData)
Called MockData[4]
Called MockData[3]
Received batch x = tensor([4, 3], dtype=torch.int32), y = tensor([104, 103], dtype=torch.int32)
Epoch = 1
Called len(MockData)
Called len(MockData)
Called MockData[7]
Called MockData[1]
Called MockData[3]
Received batch x = tensor([7, 1, 3], dtype=torch.int32), y = tensor([107, 101, 103], dtype=torch.int32)
Called MockData[0]
Called MockData[2]
Called MockData[5]
Received batch x = tensor([0, 2, 5], dtype=torch.int32), y = tensor([100, 102, 105], dtype=torch.int32)
Called len(MockData)
Called MockData[6]
Called MockData[4]
Received batch x = tensor([6, 4], dtype=torch.int32), y = tensor([106, 104], dtype=torch.int32)
```
