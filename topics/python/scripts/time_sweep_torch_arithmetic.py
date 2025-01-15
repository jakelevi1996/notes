import torch
from jutility import time_sweep, util

class Sum(time_sweep.Experiment):
    def setup(self, n):
        self.x = torch.rand([n])

    def run(self):
        return self.x.sum()

class LogSumExp(time_sweep.Experiment):
    def setup(self, n):
        self.x = torch.rand([n])

    def run(self):
        return self.x.logsumexp(-1)

class Add(time_sweep.Experiment):
    def setup(self, n):
        self.x = torch.rand([n])
        self.y = torch.rand([n])

    def run(self):
        return self.x + self.y

class Sub(time_sweep.Experiment):
    def setup(self, n):
        self.x = torch.rand([n])
        self.y = torch.rand([n])

    def run(self):
        return self.x - self.y

class Log(time_sweep.Experiment):
    def setup(self, n):
        self.x = torch.rand([n])

    def run(self):
        return self.x.log()

class Exp(time_sweep.Experiment):
    def setup(self, n):
        self.x = torch.rand([n])

    def run(self):
        return self.x.exp()

exp_list = [Sum(), LogSumExp(), Add(), Sub(), Log(), Exp()]
n_list   = util.log_range(1e6, 1e7, 10, unique_integers=True)

with util.Timer("time_sweep", hline=True):
    time_sweep.time_sweep(
        *exp_list,
        n_list=n_list,
        plot_name="Latency of PyTorch arithmetic",
    )
