import torch
from jutility import plotting

def softplus(x: torch.Tensor) -> torch.Tensor:
    return torch.logaddexp(torch.tensor(0), x)

def binary_kl_y_logit(y: torch.Tensor, t: torch.Tensor) -> torch.Tensor:
    return (
        + torch.xlogy(t, t) + torch.xlogy(1 - t, 1 - t)
        + t * softplus(-y) + (1 - t) * softplus(y)
    )

def binary_kl_y_sigmoid(y: torch.Tensor, t: torch.Tensor) -> torch.Tensor:
    return (
        + torch.xlogy(t, t) + torch.xlogy(1 - t, 1 - t)
        - torch.xlogy(t, y) - torch.xlogy(1 - t, 1 - y)
    )

n = 200
m = 200

cp = plotting.ColourPicker(n, False)
t_n1 = torch.linspace(0, 1, n).reshape(n, 1)

y_1m = torch.linspace(0, 1, m).reshape(1, m)
kl_nm = binary_kl_y_sigmoid(y_1m, t_n1)
lines_sigmoid = [
    plotting.Line(y_1m[0], kl_nm[i], c=c)
    for i, c in enumerate(cp)
]

y_1m = torch.linspace(-5, 5, m).reshape(1, m)
kl_nm = binary_kl_y_logit(y_1m, t_n1)
lines_logit = [
    plotting.Line(y_1m[0], kl_nm[i], c=c)
    for i, c in enumerate(cp)
]

mp = plotting.MultiPlot(
    plotting.Subplot(
        *lines_sigmoid,
        xlabel="y",
        title="KL[t || y]",
        grid=False,
    ),
    plotting.Subplot(
        *lines_logit,
        xlabel="z",
        title="KL[t || $\\sigma$(z)]",
        grid=False,
    ),
    plotting.ColourBar(0, 1, "cool", label="t"),
    nr=1,
    wr=[10, 10, 1],
    figsize=[8, 3],
)
mp.save()
