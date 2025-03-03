import math
import torch
from jutility import util

torch.set_printoptions(
    precision=3,
    linewidth=10000,
    sci_mode=False,
    threshold=9000,
)

printer = util.Printer(
    "demo_torch_unfold",
    "topics/pytorch/scripts/results",
    print_to_console=False,
)

def main():
    n, c, h, w = [2, 3, 7, 10]

    nchw = [n, c, h, w]
    k = 3

    x = torch.arange(math.prod(nchw)).reshape(nchw)

    y = x.unfold(-2, k, 1).unfold(-2, k, 1)

    with util.Timer("assert shapes"):
        assert list(x.shape) == [n, c, h, w]
        assert list(y.shape) == [n, c, h-k+1, w-k+1, k, k]

    with util.Timer("assert all"):
        assert all(
            torch.all(
                x[ni, ci, hi:(hi+k), wi:(wi+k)] ==
                y[ni, ci, hi, wi, :, :]
            )
            for ni in range(y.shape[0])
            for ci in range(y.shape[1])
            for hi in range(y.shape[2])
            for wi in range(y.shape[3])
        )

    printer(x[1, 2, 3, 4:(4+k)])
    printer(y[1, 2, 3-0, 4, 0+0, :])
    printer(y[1, 2, 3-1, 4, 0+1, :])
    printer(y[1, 2, 3-2, 4, 0+2, :])
    printer.hline()

    printer(x[1, 2, 3:(3+k), 4])
    printer(y[1, 2, 3, 4-0, :, 0+0])
    printer(y[1, 2, 3, 4-1, :, 0+1])
    printer(y[1, 2, 3, 4-2, :, 0+2])
    printer.hline()

    printer(x[1, 2, 3:(3+k), 4:(4+k)])
    printer(y[1, 2, 3,   4,   :, :])
    printer(y[1, 2, 3+1, 4,   :, :])
    printer(y[1, 2, 3,   4+1, :, :])
    printer.hline()

    display_tensor(x)
    display_tensor(y)

def display_tensor(x: torch.Tensor):
    printer(x)
    printer(x.shape)
    printer(x.numel())
    printer.hline()

if __name__ == "__main__":
    with util.Timer("main"):
        main()
