import torch
from jutility import plotting, util, cli

def main():
    table = util.Table(
        util.CountColumn(),
        util.Column("min", ".5f"),
        util.Column("qlo", ".5f"),
        util.Column("qhi", ".5f"),
        util.Column("max", ".5f"),
        print_interval=util.TimeInterval(1),
    )
    torch.manual_seed(0)
    n_list = util.log_range(10, 100000, 1000, unique_integers=True)
    for n in n_list.tolist():
        x = torch.normal(0, 1, [n])
        table.update(
            min=x.min().item(),
            qlo=x.quantile(0.01).item(),
            qhi=x.quantile(0.99).item(),
            max=x.max().item(),
        )

    lines = [
        plotting.Line(n_list, table.get_data("min"), label="min"),
        plotting.Line(n_list, table.get_data("qlo"), label="qlo"),
        plotting.Line(n_list, table.get_data("qhi"), label="qhi"),
        plotting.Line(n_list, table.get_data("max"), label="max"),
    ]
    plotting.ColourPicker.from_colourise(lines, cyclic=False)
    plotting.plot(
        *lines,
        plotting.Legend(),
        log_x=True,
        plot_name="demo_quantile",
        dir_name="topics/pytorch/img",
    )

if __name__ == "__main__":
    with util.Timer("main"):
        main()
