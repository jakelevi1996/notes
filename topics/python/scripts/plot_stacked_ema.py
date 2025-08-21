import numpy as np
from jutility import plotting

t = 1500
depth = 100
alpha = 0.1
threshold = 0.5
threshold_str = "Threshold = %s" % threshold

x = np.zeros([depth, t])
x[0] = 1

for ti in range(1, t):
    for di in range(1, depth):
        x[di, ti] = (1 - alpha) * x[di, ti-1] + alpha * x[di-1, ti-1]

x_masked = np.where(x < threshold, x.max(), x)
a = np.argmin(x_masked, 1)

cp = plotting.ColourPicker(depth, False)

mp = plotting.MultiPlot(
    plotting.Subplot(
        *[
            plotting.Line(x[di], c=c)
            for di, c in enumerate(reversed(list(cp)))
        ],
        plotting.HLine(threshold, c="k", ls="--", label=threshold_str),
        plotting.Legend(),
        xlabel="Time",
        ylabel="Filter output",
    ),
    plotting.Subplot(
        plotting.Line(range(depth, 0, -1), a, c="k"),
        xlabel="Layer",
        ylabel="Time until threshold",
    ),
    cp.get_colourbar(horizontal=True, label="Layer"),
    figsize=[10, 5],
    hr=[1, 0.1],
    title="Stacked EMAs ($\\alpha = %s$)" % alpha,
)
mp.save("plot_stacked_ema")
