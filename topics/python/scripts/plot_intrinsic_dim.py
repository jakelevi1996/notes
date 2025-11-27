import torch
from jutility import plotting, util, cli
import juml


def main(
    args:   cli.ParsedArgs,
    seed:   int,
    N:      float,
    D:      int,
    D_int:  int,
):
    torch.manual_seed(seed)
    juml.test_utils.torch_set_print_options(threshold=int(1e9))

    A = torch.zeros([D, D])
    i = torch.arange(D)
    A[i[:D_int], i[:D_int]] = 1
    print(A)

    eps = torch.normal(0, 1, [int(N), D, 1])
    eAe = eps.mT @ A @ eps
    eeAee = eps @ (eps.mT @ A @ eps) @ eps.mT
    eeAee_mean = eeAee.mean(0)
    print(eeAee_mean)

    eeAee_expected = torch.full([D], D_int, dtype=torch.float32)
    eeAee_expected[:D_int] += 2
    print(torch.stack([eeAee_mean[i, i], eeAee_expected]))

    kw = {
        "vmin": eeAee_mean.min(),
        "vmax": eeAee_mean.max(),
    }
    mp = plotting.MultiPlot(
        plotting.Subplot(
            plotting.ColourMesh(eeAee_mean, **kw),
            title=util.format_dict(args.get_kwargs()),
        ),
        plotting.ColourBar(**kw),
        wr=[1, 0.1],
    )
    mp.save()

if __name__ == "__main__":
    parser = cli.Parser(
        cli.Arg("seed",     type=int,   default=0),
        cli.Arg("N",        type=float, default=1e6),
        cli.Arg("D",        type=int,   default=10),
        cli.Arg("D_int",    type=int,   default=3),
    )
    args = parser.parse_args()

    with util.Timer("main"):
        main(args, **args.get_kwargs())
