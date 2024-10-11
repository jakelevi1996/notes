import os
import torch
from jutility import plotting, util, cli

CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
OUTPUT_DIR  = os.path.abspath(os.path.join(CURRENT_DIR, "..", "img"))

def main(
    name,
    kernel_size=2,
    stride=2,
    x_size=5,
    w_arange=True,
    x_arange=True,
    w_uniform=False,
    x_uniform=False,
):
    w = torch.nn.ConvTranspose2d(1, 1, kernel_size, stride)
    w.requires_grad_(False)
    w.bias.zero_()
    w.weight.zero_()
    w.weight += 1
    if w_arange:
        w.weight += torch.arange(w.weight.numel()).reshape(w.weight.shape)
        # w.weight.copy_(100 ** w.weight)
    if w_uniform:
        w.weight.uniform_()

    x = torch.ones([1, x_size, x_size])
    if x_arange:
        x += torch.arange(x.numel()).reshape(x.shape)
    if x_uniform:
        x.uniform_()

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
        subplot(x,          name="x"),
        subplot(x_up,       name="x_up"),
        subplot(w.weight,   name="w"),
        subplot(y,          name="y"),
        subplot(y_up,       name="y_up"),
        title="ConvTranspose2d demo",
        figsize=[8, 6],
    )
    mp.save(name, OUTPUT_DIR)

def subplot(t: torch.Tensor, name: str):
    return plotting.Subplot(
        plotting.ImShow(t.squeeze()),
        title="%s %s" % (name, list(t.shape)),
    )

if __name__ == "__main__":
    torch.set_printoptions(
        precision=3,
        linewidth=10000,
        sci_mode=False,
        threshold=1000,
    )
    torch.manual_seed(0)

    parser = cli.ObjectParser(
        cli.Arg("kernel_size",  "k", type=int, default=3),
        cli.Arg("stride",       "s", type=int, default=2),
        cli.Arg("x_size",       "x", type=int, default=5),
        cli.Arg("w_arange",     "wa", action="store_true"),
        cli.Arg("x_arange",     "xa", action="store_true"),
        cli.Arg("w_uniform",    "wu", action="store_true"),
        cli.Arg("x_uniform",    "xu", action="store_true"),
    )
    args = parser.parse_args()

    name = cli.get_args_summary(args)
    main(name, **cli.get_arg_dict(args))
