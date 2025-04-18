import math
import torch
from jutility import util, cli, plotting
import juml

def main(
    name:               str,
    nmhw:               tuple[int, int, int, int],
    repeats:            int,
    include_reshape:    bool,
):
    n, m, h, w = nmhw

    x_nmhw = torch.rand(nmhw)
    x_nim = x_nmhw.flatten(-2, -1).mT

    conv = torch.nn.Conv2d(m, m, 1)
    linear = juml.models.Linear(m, m)
    conv_nd = plotting.NoisyData()
    linear_nd = plotting.NoisyData()

    conv_timer      = util.Timer("conv")
    linear_timer    = util.Timer("linear")

    util.hline()
    for i in range(repeats):
        for _ in range(repeats):
            with conv_timer:
                x = conv.forward(x_nmhw)
            conv_nd.update(i, conv_timer.get_last())

        for _ in range(repeats):
            with linear_timer:
                if include_reshape:
                    x_nim = x_nmhw.flatten(-2, -1).mT
                x = linear.forward(x_nim)
                if include_reshape:
                    x = x.mT.unflatten(-1, [h, w])
            linear_nd.update(i, linear_timer.get_last())

    plotting.plot(
        conv_nd.plot(c="m"),
        linear_nd.plot(c="b"),
        plotting.Legend.from_plottables(
            plotting.NoisyData().plot(c="m", label="conv"),
            plotting.NoisyData().plot(c="b", label="linear"),
        ),
        ylim=[0, 0.1],
        plot_name=name,
        dir_name="topics/pytorch/img",
    )

if __name__ == "__main__":
    parser = cli.Parser(
        cli.Arg("nmhw",     type=int, default=[100, 64, 80, 60], nargs=4),
        cli.Arg("repeats",  type=int, default=5),
        cli.Arg("include_reshape", action="store_true"),
    )
    args = parser.parse_args()
    name = "demo_conv_vs_linear_%s" % args.get_summary()

    with util.Timer("main"):
        main(name=name, **args.get_kwargs())
