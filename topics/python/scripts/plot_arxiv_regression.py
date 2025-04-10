import os
import urllib.request
import torch
from jutility import plotting, util
import juml

data_path = "data/arxiv.csv"
if not os.path.isfile(data_path):
    dir_name = os.path.dirname(data_path)
    url = "https://arxiv.org/stats/get_monthly_submissions"
    if not os.path.isdir(dir_name):
        os.makedirs(dir_name)
    with util.Timer("Download \"%s\" from \"%s\"" % (data_path, url)):
        urllib.request.urlretrieve(url, data_path)

lines = util.load_text(data_path).strip().split("\n")
dates, n_str, _ = zip(*[line.split(",") for line in lines[1:]])
n = [int(ni) for ni in n_str]
t = list(range(len(n)))
offset = 6
step = 12 * 10

layer_exp = juml.models.Linear(1, 1)
layer_exp.init_batch(
    x=torch.tensor(t[70:-5], dtype=torch.float32).unsqueeze(-1),
    t=torch.tensor(n[70:-5], dtype=torch.float32).unsqueeze(-1).log(),
)
m_exp = layer_exp.w_io.flatten().detach().exp()
c_exp = layer_exp.b_o.flatten().detach().exp()

layer_lin = juml.models.Linear(1, 1)
layer_lin.init_batch(
    x=torch.tensor(t[70:-5], dtype=torch.float32).unsqueeze(-1),
    t=torch.tensor(n[70:-5], dtype=torch.float32).unsqueeze(-1),
)
m_lin = layer_lin.w_io.flatten().detach()
c_lin = layer_lin.b_o.flatten().detach()


x = torch.arange(0, 600, 50) * 1.0
y_exp = c_exp * (m_exp ** x)
y_lin = c_lin + (m_lin *  x)

print("Inferred lines:")
print("y = %10.3f * (%10.6f ^ x)" % (c_exp, m_exp))
print("y = %10.3f + (%10.6f * x)" % (c_lin, m_lin))

lines = [
    plotting.Line(t, n, c="k", label="Data"),
    plotting.Line(x, y_lin, c="r", m="o", ls="--", label="Linear"),
    plotting.Line(x, y_exp, c="g", m="o", ls="--", label="Exponential"),
]
kwargs = {
    "xticks": t[offset::step],
    "xticklabels": dates[offset::step],
}
mp = plotting.MultiPlot(
    plotting.Subplot(*lines, **kwargs),
    plotting.Subplot(*lines, **kwargs, log_y=True),
    figsize=[10, 4],
    legend=plotting.FigureLegend(*lines),
)
mp.save("plot_arxiv_regression")
