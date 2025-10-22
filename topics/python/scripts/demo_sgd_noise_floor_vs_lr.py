import torch
from jutility import plotting, util

def main():
    std = 0.1
    d = 100
    n_steps = 1000
    n_repeats = 10
    n_lr = 10
    lr_list = util.log_range(0.01, 1, n_lr)

    torch.manual_seed(0)

    ncs = plotting.NoisyCurveSweep(log_y=True)

    table = util.Table(
        util.TimeColumn(),
        util.CountColumn(),
        util.Column("std",      ".5f"),
        util.Column("repeat",   "i"),
        util.Column("y_T",      ".5f"),
    )

    for lr in lr_list:
        for repeat in range(n_repeats):
            y_list = run_trial(
                lr=lr,
                std=std,
                d=d,
                n_steps=n_steps,
            )
            table.update(std=std, repeat=repeat, y_T=y_list[-1])
            ncs.update(lr, y_list)

    lines = ncs.plot(
        list(range(n_steps + 1)),
        cp=plotting.ColourPicker(n_lr, cyclic=False),
        label_fmt=util.FloatFormatter(4),
        alpha_fill=0,
    )
    mp = plotting.MultiPlot(
        plotting.Subplot(
            *lines,
            *[
                get_theory_line(lr, std, d, n_steps)
                for lr in lr_list
            ],
            log_y=True,
            xlabel="$t$",
            ylabel="$y_t$",
            title="Objective function value (constant $\\sigma$)",
        ),
        legend=plotting.FigureLegend(
            *lines,
            plotting.Line(c="k", ls=":", z=50, label="Theory"),
            num_rows=None,
            loc="outside center right",
            title="$\\alpha$",
        ),
    )
    mp.save("demo_sgd_noise_floor_vs_lr")

def run_trial(
    lr:         float,
    std:        float,
    d:          int,
    n_steps:    int,
) -> list[float]:
    x = torch.ones([d])
    y = 0.5 * x.square().sum().item()
    y_list = [y]

    for _ in range(n_steps):
        eps = torch.normal(0, std, [d])
        g = x + eps
        x -= lr * g
        y = 0.5 * x.square().sum().item()
        y_list.append(y)

    return y_list

def get_theory_line(
    lr:         float,
    std:        float,
    d:          int,
    n_steps:    int,
) -> plotting.Line:
    t = torch.arange(n_steps)
    x0 = torch.ones([d])
    y0 = 0.5 * x0.square().sum().item()
    noise_floor = (lr * std * std * d) / (2 * (2 - lr))
    y = ((1 - lr) ** (2 * t)) * (y0 - noise_floor) + noise_floor
    return plotting.Line(t, y, c="k", ls=":", z=50)

if __name__ == "__main__":
    with util.Timer("main"):
        main()
