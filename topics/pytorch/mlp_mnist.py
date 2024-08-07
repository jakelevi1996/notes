import os
import numpy as np
import torch
import torch.utils.data
import torchvision
from jutility import util, plotting

CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))

class Model(torch.nn.Module):
    def forward(self, x: torch.Tensor) -> torch.Tensor:
        raise NotImplementedError()

    def num_params(self):
        return sum(p.numel() for p in self.parameters())

    def __repr__(self):
        return "%s(num_params=%s)" % (type(self).__name__, self.num_params())

class Mlp(Model):
    def __init__(
        self,
        input_dim,
        output_dim,
        hidden_dim,
        num_hidden_layers,
        act_func=None,
    ):
        super().__init__()

        if act_func is None:
            act_func = torch.nn.ReLU

        layers = []
        layer_input_dim = input_dim
        for _ in range(num_hidden_layers):
            layers.append(torch.nn.Linear(layer_input_dim, hidden_dim))
            layers.append(act_func())
            layer_input_dim = hidden_dim

        layers.append(torch.nn.Linear(layer_input_dim, output_dim))
        self.model = torch.nn.Sequential(*layers)

    def forward(self, x):
        return self.model.forward(x)

def get_data_loader(train=True, batch_size=100):
    transforms = [torchvision.transforms.ToTensor(), torch.flatten]
    dataset = torchvision.datasets.MNIST(
        root=CURRENT_DIR,
        train=train,
        transform=torchvision.transforms.Compose(transforms),
        download=True,
    )
    data_loader = torch.utils.data.DataLoader(
        dataset,
        batch_size=batch_size,
        shuffle=True,
    )
    return data_loader

def get_accuracy(model, data_loader):
    num_samples = 0
    num_correct = 0
    for x, t in data_loader:
        y = model.forward(x)
        accuracy_tensor = (y.argmax(dim=-1) == t)
        num_samples += accuracy_tensor.numel()
        num_correct += accuracy_tensor.sum().item()

    return num_correct / num_samples

def plot_metrics(table: util.Table, plot_name, output_dir, **kwargs):
    kwargs.setdefault("title", plot_name)
    kwargs.setdefault("figsize", [10, 4])
    kwargs.setdefault("top_space", 0.2)
    mp = plotting.MultiPlot(
        plotting.Subplot(
            plotting.Line(table.get_data("batch_loss")),
            xlabel="Batch",
            ylabel="Loss",
            title="Loss curve",
        ),
        plotting.Subplot(
            plotting.Line(table.get_data("train_acc"), c="b", label="Train"),
            plotting.Line(table.get_data("test_acc"),  c="r", label="Test"),
            plotting.Legend(),
            xlabel="Epoch",
            ylabel="Accuracy",
            ylim=[0, 1],
            title="Accuracy curve",
        ),
        **kwargs,
    )
    mp.save(plot_name, output_dir)

def main():
    torch.manual_seed(0)

    train_loader = get_data_loader(train=True)
    test_loader  = get_data_loader(train=False)

    model = Mlp(
        input_dim=784,
        output_dim=10,
        # num_hidden_layers=3,
        # hidden_dim=1000,
        num_hidden_layers=2,
        hidden_dim=100,
    )

    optimiser = torch.optim.Adam(model.parameters(), lr=1e-3)

    table = util.Table(
        util.TimeColumn("t", width=-11),
        util.Column("epoch"),
        util.Column("batch"),
        util.Column("batch_loss", ".5f", width=10),
        util.CallbackColumn("train_acc", ".5f", width=10).set_callback(
            lambda: get_accuracy(model, train_loader),
            level=1,
        ),
        util.CallbackColumn("test_acc", ".5f", width=10).set_callback(
            lambda: get_accuracy(model, test_loader),
            level=1,
        ),
        print_interval=util.TimeInterval(1),
    )

    num_epochs = 3
    for epoch in range(num_epochs):
        table.update(level=1, epoch=epoch)
        for i, (x, t) in enumerate(train_loader):
            y = model.forward(x)
            loss = torch.nn.functional.cross_entropy(y, t)
            optimiser.zero_grad()
            loss.backward()
            optimiser.step()
            table.update(epoch=epoch, batch=i, batch_loss=loss.item())

        table.print_last()

    table.update(level=1, epoch=num_epochs)

    plot_name = "Metrics for %s" % model
    plot_metrics(table, plot_name, os.path.join(CURRENT_DIR, "img"))

if __name__ == "__main__":
    with util.Timer("main"):
        main()
