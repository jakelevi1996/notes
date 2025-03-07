import torch
from jutility import util
import juml

printer = util.Printer(
    filename="demo_torch_profile",
    dir_name="topics/pytorch/scripts/results",
    print_to_console=False,
)

dataset = juml.datasets.Cifar10()

with util.Timer("model"):
    model = juml.models.Cnn(
        input_shape=dataset.get_input_shape(),
        output_shape=dataset.get_output_shape(),
        kernel_size=5,
        channel_dim=64,
        blocks=[2, 2],
        stride=2,
        embedder=juml.models.embed.Identity(),
        pooler=juml.models.pool.Average2d(),
    )

batch_size = 100
x, t = next(iter(dataset.get_data_loader("train", batch_size)))

with torch.profiler.profile(
    activities=[
        torch.profiler.ProfilerActivity.CPU,
        torch.profiler.ProfilerActivity.CUDA,
    ],
    profile_memory=True,
    with_flops=True,
) as prof:
    with torch.profiler.record_function("y = model.forward(x)"):
        y = model.forward(x)

printer(prof.key_averages().table(sort_by="cpu_time_total"))

util.hline()

time_batch_us = max(i.cpu_time for i in prof.key_averages())
time_batch = time_batch_us * 1e-6
time_element = time_batch / batch_size
print("Time per element = %s seconds" % time_element)
