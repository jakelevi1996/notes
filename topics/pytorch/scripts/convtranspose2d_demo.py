import os
import torch
from jutility import plotting, util

CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
OUTPUT_DIR  = os.path.abspath(os.path.join(CURRENT_DIR, "..", "img"))

def main(
    kernel_size=2,
    stride=2,
    x_size=5,
    w_arange=True,
    x_arange=True,
):
    w = torch.nn.ConvTranspose2d(1, 1, kernel_size, stride)
    w.requires_grad_(False)
    w.bias.zero_()
    w.weight.zero_()
    w.weight += 1
    if w_arange:
        w.weight += torch.arange(w.weight.numel()).reshape(w.weight.shape)
        # w.weight.copy_(100 ** w.weight)

    x = torch.ones([1, x_size, x_size])
    if x_arange:
        x += torch.arange(x.numel()).reshape(x.shape)

    y = w.forward(x)

    printer = util.Printer("ConvTranspose2d demo", OUTPUT_DIR)
    printer(w.weight.shape, w.weight, sep="\n\n")
    printer.hline()
    printer(x.shape, x, y.shape, y, sep="\n\n")
    printer.hline()

    x_up = torch.zeros(y.shape)
    start = kernel_size // 2
    end = start + (stride * x_size)
    x_up[:, start:end:stride, start:end:stride] = x

    w_up = torch.nn.Conv2d(1, 1, kernel_size, padding="same")
    w_up.requires_grad_(False)
    w_up.bias *= 0
    w_up.weight.copy_(w.weight.flip(dims=[2, 3]))

    y_up = w_up.forward(x_up)

    printer(w_up.weight, x, x_up, y, y_up, sep="\n\n")
    printer("\nMax diff:", (y - y_up).abs().max().item())
    printer.hline()

    mp = plotting.MultiPlot(
        plotting.Subplot(plotting.ImShow(x[0]),             title="x"),
        plotting.Subplot(plotting.ImShow(x_up[0]),          title="x_up"),
        plotting.Subplot(plotting.ImShow(w.weight[0, 0]),   title="w"),
        plotting.Subplot(plotting.ImShow(y[0]),             title="y"),
        plotting.Subplot(plotting.ImShow(y_up[0]),          title="y_up"),
        title="ConvTranspose2d demo",
        figsize=[8, 6],
    )
    mp.save("ConvTranspose2d demo", OUTPUT_DIR)

if __name__ == "__main__":
    torch.set_printoptions(
        precision=3,
        linewidth=10000,
        sci_mode=False,
        threshold=1000,
    )
    torch.manual_seed(0)

    main(
        # kernel_size=2,
        kernel_size=3,
        # kernel_size=4,
        # kernel_size=5,
        # kernel_size=6,
        # kernel_size=7,
        stride=2,
        # stride=3,
        # stride=4,
        # stride=5,
        # stride=6,
        # stride=7,
        x_size=5,
        # x_size=10,
        # x_size=100,
        # w_arange=True,
        w_arange=False,
        x_arange=True,
        # x_arange=False,
    )
