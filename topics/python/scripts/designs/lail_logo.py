import numpy as np
from jutility import plotting, util, cli

gr = (1 + np.sqrt(5)) / 2

lw = 10

plotting.plot(
    plotting.Line(
        [0,  0, 1, 1.5, 2],
        [gr, 0, 0, gr,  0],
        lw=lw,
    ),
    plotting.Line(
        [2.5, 2.5],
        [gr,  0],
        lw=lw,
    ),
    plotting.Line(
        [3,  3, 4],
        [gr, 0, 0],
        lw=lw,
    ),
    axis_equal=True,
    axis_off=True,
)
