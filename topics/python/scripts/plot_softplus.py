import torch
from jutility import plotting

def softplus(x: torch.Tensor) -> torch.Tensor:
    return torch.logaddexp(torch.tensor(0), x)

x = torch.linspace(-10, 10, 200)
y = softplus(x)

plotting.plot(plotting.Line(x, y))
