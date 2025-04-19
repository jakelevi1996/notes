import math
import torch
from jutility import util
import juml

printer = util.Printer(
    "demo_fancy_index",
    dir_name="topics/pytorch/scripts/results",
    print_to_console=False,
)
print_tensor = juml.test_utils.TensorPrinter(printer)
juml.test_utils.torch_set_print_options()

printer("INPUT:")
x_shape = [2, 9, 5]
x = torch.arange(math.prod(x_shape)).reshape(x_shape) + 1.0
print_tensor(x)

h, w = x.shape[-2:]

printer("IDENTITY:")
ih = torch.arange(h).reshape(h, 1)
iw = torch.arange(w).reshape(1, w)
y = x[..., ih, iw]
print_tensor(y)

printer("TRANSPOSE:")
ih = torch.arange(h).reshape(1, h)
iw = torch.arange(w).reshape(w, 1)
y = x[..., ih, iw]
print_tensor(y)

printer("UNFLATTEN:")
ih = torch.arange(h).reshape(3, 3, 1)
iw = torch.arange(w).reshape(1, 1, w)
y = x[..., ih, iw]
print_tensor(y)

printer("UNFLATTEN + TRANSPOSE:")
ih = torch.arange(h).reshape(3, 1, 3)
iw = torch.arange(w).reshape(1, w, 1)
y = x[..., ih, iw]
print_tensor(y)

printer("INPUT:")
print_tensor(x)

printer("UNFLATTEN + FLATTEN:")
ih = torch.arange(h).reshape(3, 3, 1).expand(3, 3, w).reshape(3, 3*w)
iw = torch.arange(w).reshape(1, 1, w).expand(1, 3, w).reshape(1, 3*w)
y = x[..., ih, iw]
print_tensor(y)

printer("UNFOLD:")
k = 3
ih = torch.arange(h).reshape(h, 1).expand(h, w).reshape(h, w, 1)
iw = torch.arange(w).reshape(1, w).expand(h, w).reshape(h, w, 1)
dy = torch.arange(k).reshape(k, 1).expand(k, k).flatten() - (k//2)
dx = torch.arange(k).reshape(1, k).expand(k, k).flatten() - (k//2)
ih = (ih + dy) % h
iw = (iw + dx) % w
y = x[..., ih, iw]
print_tensor(y)

printer("UNFOLD + FLATTEN:")
k = 3
ih = torch.arange(h).reshape(h, 1).expand(h, w).reshape(h*w, 1)
iw = torch.arange(w).reshape(1, w).expand(h, w).reshape(h*w, 1)
dy = torch.arange(k).reshape(k, 1).expand(k, k).flatten() - (k//2)
dx = torch.arange(k).reshape(1, k).expand(k, k).flatten() - (k//2)
ih = (ih + dy) % h
iw = (iw + dx) % w
y = x[..., ih, iw]
print_tensor(y)
