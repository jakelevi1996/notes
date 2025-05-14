import torch
import juml

torch.manual_seed(0)
juml.test_utils.torch_set_print_options()

class Quadratic:
    def __init__(
        self,
        a: torch.Tensor,
        b: torch.Tensor,
        c: torch.Tensor,
    ):
        self.a = a
        self.b = b
        self.c = c

    @classmethod
    def from_random(cls, m: int):
        h = torch.normal(0, 1, [m, m])
        a = h + h.mT
        b = torch.normal(0, 1, [m])
        c = torch.normal(0, 1, [1])
        return cls(a, b, c)

    @classmethod
    def from_data(cls, x: torch.Tensor, y: torch.Tensor):
        n, m = x.shape
        rc = [
            [row, col]
            for row in range(m)
            for col in range(row, m)
        ]
        row, col = zip(*rc)
        xx = x.unsqueeze(-1) * x.unsqueeze(-2)
        xxut = xx[:, row, col]
        d = torch.cat([xxut, x, torch.ones(n, 1)], dim=1)

        s = torch.linalg.solve(d, y)

        hut, b, c = torch.split(s, [len(rc), m, 1])
        h = torch.zeros([m, m])
        h[row, col] = hut
        a = 0.5 * (h + h.mT)

        return cls(a, b, c)

    def forward(self, x: torch.Tensor) -> torch.Tensor:
        return ((x @ self.a) * x).sum(dim=-1) + x @ self.b + self.c

    def get_turning_point(self) -> torch.Tensor:
        return torch.linalg.solve(self.a, -0.5*self.b)

    def __repr__(self) -> str:
        return (
            "Quadratic(\na=\n%s,\nb=%s,\nc=%s,\n)"
            % (self.a, self.b, self.c)
        )

m = 7
m = 3
n = m*(m+1)//2 + m + 1

q = Quadratic.from_random(m)
x = torch.normal(0, 1, [n, m])
y = q.forward(x)

q2 = Quadratic.from_data(x, y)
x_opt = q2.get_turning_point()
x_opt.requires_grad_(True)
q.forward(x_opt).backward()

print(n)
print(x.shape)
print(y.shape)
print(q)
print(q2)
print(x_opt)
print(x_opt.grad)
