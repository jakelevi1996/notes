import math
import numpy as np
from jutility import plotting

f = math.log

eps = 1e-15

# Approx Newton
x = 0.1
delta = 1e-5
f_list_an = []

while True:
    fx = f(x)
    dfdx = (f(x + delta) - fx) / delta
    x -= fx / dfdx
    f_list_an.append(fx)
    f_list_an.append(f(x + delta))

    if abs(fx) < eps:
        break

# Binary search
x_lo = 0.1
x_hi = 2.3
f_list_bs = [f(x_lo), f(x_hi)]

while True:
    x_new = (x_lo + x_hi) / 2
    fx_new = f(x_new)
    f_list_bs.append(fx_new)

    if fx_new < 0:
        x_lo = x_new
    else:
        x_hi = x_new

    if abs(fx_new) < eps:
        break

plotting.plot(
    plotting.Line(
        np.abs(np.array(f_list_bs)),
        label="Binary search",
    ),
    plotting.Line(
        np.abs(np.array(f_list_an)),
        label="Approx Newton",
        c="r",
    ),
    plotting.Legend(),
    log_y=True,
)
