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

    for n in n_list:
        for _ in range(repeats):
            x = torch.normal(0, 1, [n, input_dim])
            w = torch.normal(0, 1, [input_dim, output_dim])
            t = x @ w + torch.normal(0, std, [n, output_dim])
            x_test = torch.normal(0, 1, [n, input_dim])
            t_test = x_test @ w + torch.normal(0, std, [n, output_dim])

            cov_xt_io = x.T @ t
            cov_xx_ii = x.T @ x
            cov_xx_ii.diagonal().add_(1e-3)
            w = torch.linalg.solve(cov_xx_ii, cov_xt_io)
            results.update("solve", n, w, x, t, x_test, t_test)

            u, sd, v = torch.linalg.svd(x)
            s_inv = torch.zeros(x.T.shape)
            s_inv.diagonal().copy_(1 / sd)
            w = v.T @ s_inv @ u.T @ t
            results.update("svd", n, w, x, t, x_test, t_test)

            w, _, _, _ = torch.linalg.lstsq(x, t)
            results.update("lstsq", n, w, x, t, x_test, t_test)

            w, _, _, _ = torch.linalg.lstsq(x, t, driver="gelsd")
            results.update("lstsq_gelsd", n, w, x, t, x_test, t_test)

    results.plot(input_dim, name)

class Results:
    def __init__(self, *w_types: str):
        self.w_types = w_types
        self.num_w = len(w_types)
        self.norm_results = {
            wt: plotting.NoisyData(log_x=True, log_y=True)
            for wt in w_types
        }
        self.mse_results = {
            wt: plotting.NoisyData(log_x=True, log_y=True)
            for wt in w_types
        }
        self.mse_test_results = {
            wt: plotting.NoisyData(log_x=True, log_y=True)
            for wt in w_types
        }
        self.table = util.Table(
            util.TimeColumn(),
            util.CountColumn(),
            util.Column("n"),
            util.Column("w_type", width=15),
            util.Column("norm",         ".5f"),
            util.Column("mse",          ".5f"),
            util.Column("mse_test",     ".5f"),
        )

    def update(
        self,
        w_type: str,
        n:      int,
        w:      torch.Tensor,
        x:      torch.Tensor,
        t:      torch.Tensor,
        x_test: torch.Tensor,
        t_test: torch.Tensor,
    ):
        norm = w.square().mean().item()
        mse  = ((x @ w) - t).square().mean().item()
        mse_test = ((x_test @ w) - t_test).square().mean().item()
        self.norm_results[w_type].update(n, norm)
        self.mse_results[w_type ].update(n, mse)
        self.mse_test_results[w_type].update(n, mse_test)
        self.table.update(
            n=n,
            w_type=w_type,
            norm=norm,
            mse=mse,
            mse_test=mse_test,
        ),

    def plot(self, input_dim: int, name: str):
        cp = plotting.ColourPicker(self.num_w, cyclic=True)
        mp = plotting.MultiPlot(
            plotting.Subplot(
                *[
                    nd.plot(c=cp.next(), label=wt)
                    for wt, nd in self.mse_results.items()
                ],
                plotting.VLine(input_dim, c="k", ls="--"),
                log_x=True,
                log_y=True,
                xlabel="Train sample size",
                title="MSE (train)",
            ),
            plotting.Subplot(
                *[
                    nd.plot(c=cp.next(), label=wt)
                    for wt, nd in self.mse_test_results.items()
                ],
                plotting.VLine(input_dim, c="k", ls="--"),
                log_x=True,
                log_y=True,
                xlabel="Train sample size",
                title="MSE (test)",
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
                plotting.Line([], c="k", ls="--", label="Input dim"),
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
