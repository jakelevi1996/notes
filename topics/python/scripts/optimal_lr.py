import torch
from jutility import plotting, util

class Objective:
    def forward(self, x: torch.Tensor) -> torch.Tensor:
        raise NotImplementedError

    def grad(self, x: torch.Tensor) -> torch.Tensor:
        raise NotImplementedError

class HyperEllipsoid(Objective):
    def __init__(
        self,
        d:              int,
        condition_num:  float,
    ):
        self.a = torch.linspace(1/condition_num, 1, d)

    def forward(self, x: torch.Tensor) -> torch.Tensor:
        return 0.5 * (x.square() @ self.a)

    def grad(self, x: torch.Tensor) -> torch.Tensor:
        return self.a * x

class Learner:
    x:      torch.Tensor
    kwargs: dict

    def step(self, f: Objective):
        raise NotImplementedError

    def eval(self, f: Objective) -> torch.Tensor:
        return f.forward(self.x)

    def train(
        self,
        f:      Objective,
        steps:  int,
    ) -> tuple[torch.Tensor, list[float]]:
        x_list = [self.x.tolist()]
        f_list = [self.eval(f).item()]
        for _ in range(steps):
            self.step(f)
            x_list.append(self.x.tolist())
            f_list.append(self.eval(f).item())

        x = torch.tensor(x_list)
        return x, f_list

    def __repr__(self) -> str:
        return util.format_type(type(self), **self.kwargs, item_fmt="%s=%s")

class OptimalLr(Learner):
    def __init__(
        self,
        x0:     torch.Tensor,
        alpha:  float,
    ):
        self.x = x0
        self.alpha = alpha
        self.kwargs = {"$\\alpha$": alpha}

    def step(self, f: Objective):
        g = f.grad(self.x)
        fx = f.forward(self.x)
        fxp = f.forward(self.x + self.alpha * g)
        fxm = f.forward(self.x - self.alpha * g)
        lr = 0.5 * self.alpha * (fxp - fxm) / (fxp + fxm - 2 * fx)

        self.x -= lr * g

class OptimalLrMomentum(Learner):
    def __init__(
        self,
        x0:     torch.Tensor,
        alpha:  float,
        beta:   float,
    ):
        self.x = x0
        self.alpha = alpha
        self.beta = beta
        self.m = torch.zeros_like(x0)
        self.kwargs = {"$\\alpha$": "%.2f" % alpha, "$\\beta$": "%.2f" % beta}

    def step(self, f: Objective):
        g = f.grad(self.x)
        self.m *= self.beta
        self.m += g

        fx = f.forward(self.x)
        fxp = f.forward(self.x + self.alpha * self.m)
        fxm = f.forward(self.x - self.alpha * self.m)
        lr = 0.5 * self.alpha * (fxp - fxm) / (fxp + fxm - 2 * fx)

        self.x -= lr * self.m

class Momentum(Learner):
    def __init__(
        self,
        x0:     torch.Tensor,
        alpha:  float,
        beta:   float,
    ):
        self.x = x0
        self.alpha = alpha
        self.beta = beta
        self.m = torch.zeros_like(x0)
        self.kwargs = {"$\\alpha$": "%.2f" % alpha, "$\\beta$": "%.2f" % beta}

    def step(self, f: Objective):
        g = f.grad(self.x)
        self.m *= self.beta
        self.m += g

        self.x -= self.alpha * self.m

condition_num = 3
steps = 50

f = HyperEllipsoid(2, condition_num)

alpha_opt   = 2 / ((1 / condition_num) + 1)
alpha_opt_m = (2 / ((1 / condition_num) ** 0.5 + 1)) ** 2
beta_opt_m  = ((condition_num ** 0.5 - 1) / (condition_num ** 0.5 + 1)) ** 2

learner_list = [
    OptimalLr(torch.ones(2), 0.1),
    OptimalLrMomentum(torch.ones(2), 0.1, beta_opt_m),
    OptimalLrMomentum(torch.ones(2), 0.1, 0.01),
    Momentum(torch.ones(2), alpha_opt, 0),
    Momentum(torch.ones(2), alpha_opt_m, beta_opt_m),
]

x_lines = []
f_lines = []
legend_lines = []
cp = plotting.ColourPicker(len(learner_list), cmap_name="gist_rainbow")

for learner, c in zip(learner_list, cp):
    assert isinstance(learner, Learner)
    x, f_list = learner.train(f, steps)
    x_lines.append(plotting.Line(x[:, 0], x[:, 1], c=c))
    f_lines.append(plotting.Line(f_list, m="o", c=c))
    legend_lines.append(plotting.Line(c=c, label=repr(learner)))

w = 100
h = 100
x_1w    = torch.linspace(-1, 1, w).unsqueeze(-2)
y_h1    = torch.linspace(-1, 1, h).unsqueeze(-1)
x_hw    = torch.tile(x_1w, [h, 1])
y_hw    = torch.tile(y_h1, [1, w])
xy_hw2  = torch.stack([x_hw, y_hw], dim=-1)
z = f.forward(xy_hw2)

mp = plotting.MultiPlot(
    plotting.Subplot(
        plotting.Contour(x_1w.squeeze(), y_h1.squeeze(), torch.log(z), 20),
        *x_lines,
        axis_square=True,
        grid=False,
    ),
    plotting.Subplot(
        *f_lines,
        log_y=True,
    ),
    figsize=[8, 5],
    legend=plotting.FigureLegend(
        *legend_lines,
        num_rows=None,
        loc="outside lower center",
    ),
    title="$\\kappa = %i$" % condition_num,
)
mp.save()
