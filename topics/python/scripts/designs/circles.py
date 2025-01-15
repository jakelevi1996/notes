import numpy as np
from jutility import plotting

x_list = np.linspace(0, 1, 5).tolist()

plotting.MultiPlot(
    plotting.Subplot(
        *[
            plotting.Circle([1-x, x], np.sqrt(2)/10, ec=None, fc=[1, x, x])
            for x in x_list
        ],
        axis_off=True,
        axis_equal=True,
        xlim=[-0.2, 1.2],
        ylim=[-0.2, 1.2],
    ),
    colour=[0, 0, 0.5],
    figsize=[10, 10],
).save()
