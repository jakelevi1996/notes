from jutility import plotting, util, cli
import torch
import juml

juml.test_utils.torch_set_print_options(threshold=int(1e9))
torch.manual_seed(0)

printer = util.Printer("print_gaussian_moments")
print_tensor = juml.test_utils.TensorPrinter(printer)

for d, n in [[5, 1e3], [20, 1e3], [5, 1e7], [10, 5e6], [20, 1e6]]:
    with util.Timer("print_gaussian_moments", printer, hline=True):

        v = torch.normal(0, 1, [int(n), d, 1])

        p = v @ (v.mT @ v) @ v.mT

        pm = p.mean(dim=0)

        print_tensor(pm)

    printer(3 + (d - 1))

    hi = pm.max().item()
    lo = pm.min().item()
    plot_name = "Gaussian moments (d = %s, n = %s)" % (d, n)

    mp = plotting.MultiPlot(
        plotting.Subplot(plotting.ImShow(pm)),
        plotting.ColourBar(lo, hi, ticks=[lo, hi, (lo + hi)/2]),
        width_ratios=[1, 0.1],
        title=plot_name,
        title_font_size=12,
    )
    mp.save(plot_name)
