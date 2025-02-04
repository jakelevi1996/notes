import numpy as np
from jutility import plotting

x = np.linspace(-10, 10, 500)
lines = [
    plotting.Line(x, np.abs(x),             label="abs"),
    plotting.Line(x, np.tanh(x) * x,        label="tanhglu"),
    plotting.Line(x, x / (1 + np.exp(-x)),  label="swish"),
    plotting.Line(x, np.log1p(np.exp(x)),   label="softplus"),
]
plotting.ColourPicker.from_colourise(lines)
plotting.plot(
    *lines,
    plotting.Legend(),
    ylim=[-1, 4],
    xlim=[-8, 5],
    figsize=[6, 4],
)
