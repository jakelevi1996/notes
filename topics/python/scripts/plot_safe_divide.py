import numpy as np
from jutility import plotting

def safe_divide(a: np.ndarray, b: np.ndarray, eps: float):
    return np.where(b > 0, a, -a) / np.clip(np.abs(b), eps, None)

x = np.linspace(-2, 2, 500)
r_true = 1 / x
r_safe = safe_divide(1, x, eps=1e-1)
plotting.plot(
    plotting.Line(x, r_true,  c="b", label="True", lw=10, a=0.5),
    plotting.Line(x, r_safe, c="r", label="Safe"),
    plotting.Legend(),
    ylim=[-15, 15],
    figsize=[6, 4],
)
