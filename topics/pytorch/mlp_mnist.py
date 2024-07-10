import os
import numpy as np
import torch
import torchvision
from jutility import util, plotting

CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))

def get_data_loaders(batch_size=100):
    transforms = [torchvision.transforms.ToTensor(), torch.flatten]
    data_kwargs = {
        "root":         CURRENT_DIR,
        "download":     True,
        "transform":    torchvision.transforms.Compose(transforms),
    }
    train_dataset = torchvision.datasets.MNIST(train=True , **data_kwargs)
    test_dataset  = torchvision.datasets.MNIST(train=False, **data_kwargs)

    load_kwargs = {
        "batch_size":   batch_size,
        "shuffle":      True,
    }
    train_loader = torch.utils.data.DataLoader(train_dataset, **load_kwargs)
    test_loader  = torch.utils.data.DataLoader(test_dataset,  **load_kwargs)

    return train_loader, test_loader

class Mlp(torch.nn.Module):
    def __init__(
        self,
        input_dim,
        output_dim,
        num_hidden_layers,
        hidden_dim,
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

def get_accuracy(model, data_loader):
    num_samples = 0
    num_correct = 0
    for x, t in data_loader:
        y = model.forward(x)
        accuracy_tensor = (y.argmax(dim=1) == t)
        num_samples += accuracy_tensor.numel()
        num_correct += accuracy_tensor.sum().item()

    return num_correct / num_samples

def main():
    torch.manual_seed(0)

    train_loader, test_loader = get_data_loaders()

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
    table.update(level=1, epoch=0)
    for epoch in range(num_epochs):
        for i, (x, t) in enumerate(train_loader):
            y = model.forward(x)
            loss = torch.nn.functional.cross_entropy(y, t)
            optimiser.zero_grad()
            loss.backward()
            optimiser.step()
            table.update(epoch=epoch, batch=i, batch_loss=loss.item())

        table.print_last()
        table.update(level=1, epoch=epoch+1)

    batch_loss = table.get_data("batch_loss")
    downsample_ratio = 20
    mean, ucb, lcb = util.confidence_bounds(
        np.array(batch_loss),
        split_dim=0,
        downsample_ratio=downsample_ratio,
    )
    x = np.linspace(0, num_epochs, len(batch_loss))
    x_ds = x[::downsample_ratio]
    mp = plotting.MultiPlot(
        plotting.Subplot(
            plotting.Line(x, batch_loss, c="b", a=0.3, z=20),
            plotting.Line(x_ds, mean, c="b", z=30),
            plotting.FillBetween(x_ds, ucb, lcb, c="b", a=0.3, z=10),
            xlabel="Epoch",
            ylabel="Loss",
            title="Loss curve",
        ),
        plotting.Subplot(
            plotting.Line(table.get_data("train_acc"), c="b", label="Train"),
            plotting.Line(table.get_data("test_acc"),  c="r", label="Test"),
            plotting.Legend(),
            xlabel="Epoch",
            ylabel="Accuracy",
            title="Accuracy curve",
        ),
        figsize=[10, 4],
    )
    mp.save("mlp_mnist", os.path.join(CURRENT_DIR, "img"))

if __name__ == "__main__":
    with util.Timer("main"):
        main()
