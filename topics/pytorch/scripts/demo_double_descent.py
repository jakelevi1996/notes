import torch
from jutility import plotting, util, cli

def main(
    name:       str,
    seed:       int,
    repeats:    int,
    input_dim:  int,
    output_dim: int,
    n_list:     list[int],
):
    torch.manual_seed(seed)

    results = Results("svd", "lstsq", "lstsq_gelsd")

    for n in n_list:
        for _ in range(repeats):
            x = torch.rand([n, input_dim])
            t = torch.rand([n, output_dim])

            u, sd, v = torch.linalg.svd(x)
            s_inv = torch.zeros(x.T.shape)
            s_inv.diagonal().copy_(1/sd)
            w = v.T @ s_inv @ u.T @ t
            results.update("svd", n, w, x, t)

            w, _, _, _ = torch.linalg.lstsq(x, t)
            results.update("lstsq", n, w, x, t)

            w, _, _, _ = torch.linalg.lstsq(x, t, driver="gelsd")
            results.update("lstsq_gelsd", n, w, x, t)

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
        self.table = util.Table(
            util.TimeColumn(),
            util.CountColumn(),
            util.Column("n"),
            util.Column("w_type", width=15),
            util.Column("norm", ".5f"),
            util.Column("mse",  ".5f"),
        )

    def update(
        self,
        w_type: str,
        n:      int,
        w:      torch.Tensor,
        x:      torch.Tensor,
        t:      torch.Tensor,
    ):
        norm    = w.square().mean().item()
        mse     = ((x @ w) - t).square().mean().item()
        self.norm_results[w_type    ].update(n, norm)
        self.mse_results[w_type     ].update(n, mse)
        self.table.update(n=n, w_type=w_type, norm=norm, mse=mse)

    def plot(self, input_dim: int, name: str):
        cp = plotting.ColourPicker(self.num_w, cyclic=True)
        mp = plotting.MultiPlot(
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
            plotting.Subplot(
                *[
                    nd.plot(c=cp.next(), label=wt)
                    for wt, nd in self.mse_results.items()
                ],
                plotting.VLine(input_dim, c="k", ls="--"),
                log_x=True,
                log_y=True,
                xlabel="Train sample size",
                title="MSE",
            ),
            figsize=[10, 4],
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
        cli.Arg("seed",         type=int, default=0),
        cli.Arg("repeats",      type=int, default=5),
        cli.Arg("input_dim",    type=int, default=300),
        cli.Arg("output_dim",   type=int, default=10),
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
