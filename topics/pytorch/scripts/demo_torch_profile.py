import torch
from torch.autograd.profiler_util import FunctionEventAvg
from jutility import util, units
import juml

def get_max_flops_event(
    event_list: list[FunctionEventAvg],
) -> FunctionEventAvg:
    return max(event_list, key=(lambda i: i.flops))

def get_max_time_event(
    event_list: list[FunctionEventAvg],
) -> FunctionEventAvg:
    return max(event_list, key=(lambda i: i.cpu_time))

x = torch.rand([5000, 5000])
y = torch.rand([5000, 5000])
with torch.profiler.profile(
    activities=[
        torch.profiler.ProfilerActivity.CPU,
        torch.profiler.ProfilerActivity.CUDA,
    ],
    profile_memory=True,
    with_flops=True,
) as prof:
    with torch.profiler.record_function("matmul"):
        z = x @ y

max_flops_event = get_max_flops_event(prof.key_averages())
matmul_t = max_flops_event.cpu_time * 1e-6
matmul_f = max_flops_event.flops
matmul_flops_per_s = matmul_f / matmul_t
util.hline()
print("Time  (matmul)   = %.6f seconds" % (matmul_t))
print("FLOPS (matmul)   = %s" % units.metric.format(matmul_f))
print("FLOPS per second = %s" % units.metric.format(matmul_flops_per_s))
util.hline()

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

time_batch_s = get_max_time_event(prof.key_averages()).cpu_time * 1e-6
time_element_s = time_batch_s / batch_size
print("Time per element = %.6f seconds" % time_element_s)

flops_per_element = matmul_flops_per_s * time_element_s
print("FLOPS per element = %s" % units.metric.format(flops_per_element))

max_flops_event = get_max_flops_event(prof.key_averages())
forward_t = max_flops_event.cpu_time * 1e-6
forward_f = max_flops_event.flops
forward_flops_per_s = forward_f / forward_t
print("FLOPS per second = %s" % units.metric.format(forward_flops_per_s))

efficiency = forward_flops_per_s / matmul_flops_per_s
print("Efficiency (forward vs matmul) = %.5f"  % efficiency)
