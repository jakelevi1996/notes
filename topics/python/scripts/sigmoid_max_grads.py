import math
import torch
from jutility import plotting

x = torch.linspace(-8, 8, 200)

q = x.sigmoid()
dq = q * (1 - q)
ddq = dq * (1 - 2 * q)

dq_max = 1/4
dq_max_q = 1/2
dq_max_x = 0
dq_max_ddq = 0

ddq_max = 1/4 * (2 / math.sqrt(27))
ddq_max_q = 1/2 - 1 / (2 * math.sqrt(3))
ddq_max_dq = ddq_max_q * (1 - ddq_max_q)
ddq_max_x = math.log(ddq_max_q / (1 - ddq_max_q))

print("Empirical max:   ", ddq.max().item())
print("Theoretical max: ", ddq_max)

mp = plotting.MultiPlot(
    plotting.Subplot(
        plotting.Line(x, q),
        plotting.AxLine(
            [dq_max_x, dq_max_q],
            slope=dq_max,
            c="r",
            ls=":",
        ),
        plotting.Scatter(dq_max_x, dq_max_q, c="r"),
        plotting.Scatter(ddq_max_x, ddq_max_q, c="g"),
    ),
    plotting.Subplot(
        plotting.Line(x, dq),
        plotting.HLine(dq_max, c="r", ls="--"),
        plotting.AxLine(
            [ddq_max_x, ddq_max_dq],
            slope=ddq_max,
            c="g",
            ls=":",
        ),
        plotting.Scatter(dq_max_x, dq_max, c="r"),
        plotting.Scatter(ddq_max_x, ddq_max_dq, c="g"),
    ),
    plotting.Subplot(
        plotting.Line(x, ddq),
        plotting.HLine(ddq_max, c="g", ls="--"),
        plotting.Scatter(dq_max_x, dq_max_ddq, c="r"),
        plotting.Scatter(ddq_max_x, ddq_max, c="g"),
    ),
    plotting.LegendSubplot(
        plotting.Line(label="$\\sigma(x)$"),
        plotting.Scatter(None, None, label="$(0, 1/2)$", c="r"),
        plotting.Scatter([], [], label="$(x^*, q^*)$", c="g"),
        plotting.Line(label="$q^* = (1 - 1/\\sqrt{3})$", a=0),
        plotting.Line(label="$x^* = \\sigma^{-1}(q^*)$", a=0),
        loc="upper center"
    ),
    plotting.LegendSubplot(
        plotting.Line(label="$\\sigma^\prime(x)$"),
        plotting.Scatter([], [], label="$(0, 1/4)$", c="r"),
        plotting.Scatter([], [], label="$(x^*, \\sigma^\prime(x^*))$", c="g"),
        plotting.Line(label="Max gradient", ls=":", c="k"),
        plotting.Line(label="Max value", ls="--", c="k"),
        loc="upper center"
    ),
    plotting.LegendSubplot(
        plotting.Line(label="$\\sigma^{\prime\prime}(x)$"),
        plotting.Scatter([], [], label="$(0, 0)$", c="r"),
        plotting.Scatter([], [], label="$(x^*, (1/4)(2/\\sqrt{27}))$", c="g"),
        loc="upper center"
    ),
    nc=3,
    hr=[1, 0.1],
    figsize=[8, 4],
)
mp.save("sigmoid_max_grads")
