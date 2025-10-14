import torch
from jutility import plotting, util

torch.manual_seed(2)

def get_random_orthogonal(d: int) -> torch.Tensor:
    A = torch.normal(0, 1, [d, d])
    Q, _ = torch.linalg.qr(A)

    return Q

def random_uniform(d: int, lo: float, hi: float) -> torch.Tensor:
    return lo + (hi - lo) * torch.rand(d)

class Loss:
    def __init__(self, A: torch.Tensor):
        self._A = A

    def forward(self, x: torch.Tensor) -> torch.Tensor:
        return x.mT @ self._A @ x

class Learner:
    def __init__(
        self,
        d:              int,
        opt_type:       type[torch.optim.Optimizer],
        loss:           Loss,
        use_closure:    bool=False,
    ):
        self._x = torch.ones([d, 1], requires_grad=True)
        self._opt = opt_type([self._x])
        self._loss = loss
        self._args = []

        if use_closure:
            self._args.append(lambda: loss.forward(self._x))

    def step(self) -> float:
        loss = self._loss.forward(self._x)
        self._opt.zero_grad()
        loss.backward()
        self._opt.step(*self._args)
        return loss.item()

d = 20
d = 10
n_small = 5
T = 10000

Q = get_random_orthogonal(d)

assert isinstance(Q, torch.Tensor)

eig_vals = torch.ones(d)
eig_vals[:n_small] = 10.0 ** random_uniform(n_small, -5, -3)

A = Q.mT @ (eig_vals.reshape(d, 1) * Q)

loss = Loss(A)

adam = Learner(d, torch.optim.Adam,  loss)
bfgs = Learner(d, torch.optim.LBFGS, loss, use_closure=True)

table = util.Table(
    util.TimeColumn(),
    util.CountColumn(),
    util.Column("adam", ".5f"),
    util.Column("bfgs", ".5f"),
    print_interval=util.TimeInterval(1),
)

for _ in range(T):
    table.update(
        adam=adam.step(),
        bfgs=bfgs.step(),
    )

plotting.plot(
    plotting.Line(table.get_data("adam"), c="b", label="Adam"),
    plotting.Line(table.get_data("bfgs"), c="r", label="L-BFGS"),
    plotting.Legend(),
    log_y=True,
    xlabel="t",
    ylabel="$y_t$",
    plot_name="adam_vs_lbfgs",
)
