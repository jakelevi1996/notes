import numpy as np
from jutility import plotting

def count_consecutive_increases(y: np.ndarray) -> np.ndarray:
    dy = np.diff(y, prepend=y[0])
    mask = np.where(dy > 0, 1, 0)

    naive_counts = np.cumsum(mask)
    reset_inds = (mask == 0)
    reset_vals = np.diff(naive_counts[reset_inds], prepend=0)

    mask[reset_inds] = -reset_vals
    counts = np.cumsum(mask)

    return counts

rng = np.random.default_rng(0)

n = 50
x = np.linspace(0, 5, n)
y = np.exp(-x) + rng.normal(0, 0.05, n)
c = count_consecutive_increases(y)

x = np.arange(y.size)

mp = plotting.MultiPlot(
    plotting.Subplot(
        plotting.Line(x, y, c="k"),
        plotting.Scatter(x, y, c=c, cmap="cool"),
    ),
    plotting.ColourBar(c.min(), c.max(), "cool", ticks=range(c.max()+1)),
    width_ratios=[1, 0.1],
    figsize=[6, 4],
)
mp.save("count_consecutive_increases")
