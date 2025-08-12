"""
See EG https://arxiv.org/pdf/1611.00712
"""

import numpy as np
from jutility import plotting

rng = np.random.default_rng(0)

x = rng.uniform(0, 1, int(1e6))
y = -np.log(-np.log(x))

mp = plotting.MultiPlot(
    plotting.Subplot(
        plotting.Hist(x, 50, ec=None),
    ),
    plotting.Subplot(
        plotting.Hist(-np.log(x), 50, ec=None),
    ),
    plotting.Subplot(
        plotting.Hist(-np.log(-np.log(x)), 50, ec=None),
    ),
    plotting.Subplot(
        plotting.Hist(x, 50, ec=None),
        log_y=True,
    ),
    plotting.Subplot(
        plotting.Hist(-np.log(x), 50, ec=None),
        log_y=True,
    ),
    plotting.Subplot(
        plotting.Hist(-np.log(-np.log(x)), 50, ec=None),
        log_y=True,
    ),
    figsize=[10, 5],
)
mp.save()
