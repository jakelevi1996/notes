import numpy as np
from jutility import plotting, util

x = util.log_range(1e-5, 1e5, 200)
kw = {"log_x": True, "log_y": True, "grid_x": "major", "grid_y": "major"}
plotting.MultiPlot(
    *[
        plotting.Subplot(
            plotting.Line(x, (np.sqrt(x + eps) - np.sqrt(x)), lw=5),
            plotting.HLine(np.sqrt(eps), c="c"),
            plotting.VLine(eps/4, c="g"),
            plotting.Line(x, eps/(2 * np.sqrt(x)), c="r"),
            title="$\\varepsilon = %s$" % eps,
            **kw,
        )
        for eps in [0.01, 1, 100]
    ],
    legend=plotting.FigureLegend(
        plotting.Line([], lw=5,  label="$\\sqrt{x+\\varepsilon}-\\sqrt{x}$"),
        plotting.Line([], c="c", label="$\\sqrt{\\varepsilon}$"),
        plotting.Line([], c="g", label="$\\varepsilon/4$"),
        plotting.Line([], c="r", label="$\\varepsilon/(2\\sqrt{x})$"),
        fontsize=15,
    ),
    sharey=True,
    num_rows=1,
    figsize=[10, 3],
).save()
