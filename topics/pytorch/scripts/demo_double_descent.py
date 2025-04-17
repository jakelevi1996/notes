import torch
from jutility import plotting, util, cli

def main(
    name:       str,
    seed:       int,
    repeats:    int,
    input_dim:  int,
    output_dim: int,
    std:        float,
    n_list:     list[int],
):
    torch.manual_seed(seed)

    results = Results("svd", "lstsq", "lstsq_gelsd", "solve")
    timer   = util.Timer(verbose=False)

    for n in n_list:
        for _ in range(repeats):
            x = torch.normal(0, 1, [n, input_dim])
            w = torch.normal(0, 1, [input_dim, output_dim])
            y = x @ w + torch.normal(0, std, [n, output_dim])
            x_test = torch.normal(0, 1, [n, input_dim])
            y_test = x_test @ w + torch.normal(0, std, [n, output_dim])
            args = [n, x, y, x_test, y_test]

            with timer:
                cov_xy_io = x.T @ y
                cov_xx_ii = x.T @ x
                cov_xx_ii.diagonal().add_(1e-3)
                w = torch.linalg.solve(cov_xx_ii, cov_xy_io)
            results.update("solve", w, timer.get_last(), *args)

            with timer:
                u, sd, v = torch.linalg.svd(x)
                s_inv = torch.zeros(x.T.shape)
                s_inv.diagonal().copy_(1 / sd)
                w = v.T @ s_inv @ u.T @ y
            results.update("svd", w, timer.get_last(), *args)

            with timer:
                w, _, _, _ = torch.linalg.lstsq(x, y)
            results.update("lstsq", w, timer.get_last(), *args)

            with timer:
                w, _, _, _ = torch.linalg.lstsq(x, y, driver="gelsd")
            results.update("lstsq_gelsd", w, timer.get_last(), *args)

        print(results.table.format_header())

    results.plot(input_dim, std, name)

class Results:
    def __init__(self, *w_types: str):
        self.w_types = w_types
        self.num_w = len(w_types)
        self.rmse_results = {
            wt: plotting.NoisyData(log_x=True, log_y=True)
            for wt in w_types
        }
        self.rmse_test_results = {
            wt: plotting.NoisyData(log_x=True, log_y=True)
            for wt in w_types
        }
        self.time_results = {
            wt: plotting.NoisyData(log_x=True, log_y=True)
            for wt in w_types
        }
        self.norm_results = {
            wt: plotting.NoisyData(log_x=True, log_y=True)
            for wt in w_types
        }
        self.table = util.Table(
            util.TimeColumn(),
            util.CountColumn(),
            util.Column("n"),
            util.Column("w_type", width=15),
            util.Column("rmse",         ".5f"),
            util.Column("rmse_test",    ".5f"),
            util.Column("time",         ".5f"),
            util.Column("norm",         ".5f"),
        )

    def update(
        self,
        w_type: str,
        w:      torch.Tensor,
        t:      float,
        n:      int,
        x:      torch.Tensor,
        y:      torch.Tensor,
        x_test: torch.Tensor,
        y_test: torch.Tensor,
    ):
        norm = w.square().mean().item()
        rmse = ((x @ w) - y).square().mean().sqrt().item()
        rmse_test = ((x_test @ w) - y_test).square().mean().sqrt().item()
        self.rmse_results[w_type].update(n, rmse)
        self.rmse_test_results[w_type].update(n, rmse_test)
        self.time_results[w_type].update(n, t)
        self.norm_results[w_type].update(n, norm)
        self.table.update(
            n=n,
            w_type=w_type,
            rmse=rmse,
            rmse_test=rmse_test,
            time=t,
            norm=norm,
        ),

    def plot(
        self,
        input_dim:  int,
        std:        float,
        name:       str,
    ):
        hv = "$(d_{in}, \\sigma)$"
        cp = plotting.ColourPicker(self.num_w, cyclic=True)
        mp = plotting.MultiPlot(
            plotting.Subplot(
                *[
                    nd.plot(c=cp.next(), label=wt)
                    for wt, nd in self.rmse_results.items()
                ],
                plotting.VLine(input_dim,   c="k", ls="--"),
                plotting.HLine(std,         c="k", ls="--"),
                log_x=True,
                log_y=True,
                xlabel="Train sample size",
                title="RMSE (train)",
            ),
            plotting.Subplot(
                *[
                    nd.plot(c=cp.next(), label=wt)
                    for wt, nd in self.rmse_test_results.items()
                ],
                plotting.VLine(input_dim,   c="k", ls="--"),
                plotting.HLine(std,         c="k", ls="--"),
                log_x=True,
                log_y=True,
                xlabel="Train sample size",
                title="RMSE (test)",
            ),
            plotting.Subplot(
                *[
                    nd.plot(c=cp.next(), label=wt)
                    for wt, nd in self.time_results.items()
                ],
                plotting.VLine(input_dim, c="k", ls="--"),
                log_x=True,
                log_y=True,
                xlabel="Train sample size",
                title="Time taken",
            ),
            plotting.Subplot(
                *[
                    nd.plot(c=cp.next(), label=wt)
                    for wt, nd in self.norm_results.items()
                ],
                plotting.VLine(input_dim, c="k", ls="--"),
                log_x=True,
                log_y=True,
                xlabel="Train sample size",
                title="Parameter norm",
            ),
            figsize=[10, 8],
            legend=plotting.FigureLegend(
                *[
                    plotting.NoisyData().plot(c=cp.next(), label=wt)
                    for wt in self.w_types
                ],
                plotting.Line([], c="k", ls="--", label=hv),
            ),
        )
        mp.save(name, "topics/pytorch/img")

if __name__ == "__main__":
    parser = cli.Parser(
        cli.Arg("seed",         type=int,   default=0),
        cli.Arg("repeats",      type=int,   default=5),
        cli.Arg("input_dim",    type=int,   default=300),
        cli.Arg("output_dim",   type=int,   default=10),
        cli.Arg("std",          type=float, default=1e-3),
        cli.Arg(
            "n_list",
            type=int,
            nargs="+",
            default=[10, 30, 100, 300, 1000, 3000, 10000],
        ),
    )
    args = parser.parse_args()
    name = "demo_double_descent_%s" % args.get_summary()

    with util.Timer("main"):
        main(name=name, **args.get_kwargs())
