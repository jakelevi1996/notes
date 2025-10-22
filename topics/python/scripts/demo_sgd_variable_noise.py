import torch
from jutility import plotting, util

def main():
    k = 0.1
    d = 100
    n_steps = 1000
    n_repeats = 10
    n_lr = 10
    lr_list = util.log_range(0.01, 0.2, n_lr)

    torch.manual_seed(0)

    ncs = plotting.NoisyCurveSweep()
    nd = plotting.NoisyData(log_y=True)

    table = util.Table(
        util.TimeColumn(),
        util.CountColumn(),
        util.Column("k",        ".5f"),
        util.Column("repeat",   "i"),
        util.Column("y_T",      ".5f"),
    )

    for lr in lr_list:
        for repeat in range(n_repeats):
            y_list = run_trial(
                lr=lr,
                k=k,
                d=d,
                n_steps=n_steps,
            )
            table.update(k=k, repeat=repeat, y_T=y_list[-1])
            ncs.update(lr, y_list)
            nd.update(lr, y_list[-1])

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
                get_theory_line(lr, k, d, n_steps)
                for lr in lr_list
            ],
            log_y=True,
            xlabel="$t$",
            ylabel="$y_t$",
            title="Objective function value (variable $\\sigma$)",
        ),
        legend=plotting.FigureLegend(
            *lines,
            plotting.Line(c="k", ls=":", z=50, label="Theory"),
            num_rows=None,
            loc="outside center right",
            title="$\\alpha$",
        ),
    )
    mp.save("demo_sgd_variable_noise_vs_k")

    kd = k * d
    x0 = torch.ones([d])
    y0 = 0.5 * x0.square().sum().item()

    lr_eval = util.log_range(0.01, 0.2, 200)
    rho_eval = ((1 - lr_eval) ** 2) + (lr_eval ** 2) * kd
    y_T_eval = (rho_eval ** n_steps) * y0

    lr_best = 1 / (1 + kd)
    rho_best = kd / (1 + kd)
    y_T_best = (rho_best ** n_steps) * y0

    lines = [
        nd.plot(c="c", label="Empirical"),
        plotting.Line(lr_eval, y_T_eval, c="k", ls=":", z=50, label="Theory"),
        plotting.Scatter(
            [lr_best],
            [y_T_best],
            c="r",
            m="*",
            z=50,
            label="($\\alpha^*, (\\rho^*)^T y_0)$",
        ),
    ]
    mp = plotting.MultiPlot(
        plotting.Subplot(
            *lines,
            log_x=True,
            log_y=True,
            xlabel="$\\alpha$",
            ylabel="$y_T$",
            title="Final objective function values (variable $\\sigma$)",
        ),
        legend=plotting.FigureLegend(
            *lines,
            num_rows=None,
            loc="outside center right",
        ),
    )
    mp.save("demo_sgd_variable_noise_final")

def run_trial(
    lr:         float,
    k:          float,
    d:          int,
    n_steps:    int,
) -> list[float]:
    x = torch.ones([d])
    y = 0.5 * x.square().sum().item()
    y_list = [y]

    for _ in range(n_steps):
        std = torch.sqrt(k * x.square().sum())
        eps = torch.normal(0, std, [d])
        g = x + eps
        x -= lr * g
        y = 0.5 * x.square().sum().item()
        y_list.append(y)

    return y_list

def get_theory_line(
    lr:         float,
    k:          float,
    d:          int,
    n_steps:    int,
) -> plotting.Line:
    t = torch.arange(n_steps)
    x0 = torch.ones([d])
    y0 = 0.5 * x0.square().sum().item()
    rho = ((1 - lr) ** 2) + (lr ** 2) * k * d
    y = (rho ** t) * y0
    return plotting.Line(t, y, c="k", ls=":", z=50)

if __name__ == "__main__":
    with util.Timer("main"):
        main()
