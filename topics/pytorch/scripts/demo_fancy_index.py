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
juml.test_utils.torch_set_print_options(threshold=1e5)

printer.heading("NHW")

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

printer.heading("NCHW")

printer("INPUT:")
nchw = [2, 8, 3, 5]
x = torch.arange(math.prod(nchw)).reshape(nchw) + 1.0
print_tensor(x)

c, h, w = x.shape[-3:]

heads = 2
d_qkv = c // heads
k = 3

ac = torch.arange(c)
ah = torch.arange(h)
aw = torch.arange(w)
ak = torch.arange(k)

printer("FLATTEN:")
ih = ah.reshape(h, 1).expand(h, w).reshape(h*w)
iw = aw.reshape(1, w).expand(h, w).reshape(h*w)
y = x[..., ih, iw]
print_tensor(y)

printer("FLATTEN + TRANSPOSE:")
ic = ac
ih = ah.reshape(h, 1).expand(h, w).reshape(h*w, 1)
iw = aw.reshape(1, w).expand(h, w).reshape(h*w, 1)
y = x[..., ic, ih, iw]
print_tensor(y)

printer("FLATTEN + TRANSPOSE + UNFLATTEN:")
ic = ac.reshape(heads, 1, d_qkv)
ih = ah.reshape(h, 1).expand(h, w).reshape(h*w, 1, 1, 1)
iw = aw.reshape(1, w).expand(h, w).reshape(h*w, 1, 1, 1)
y = x[..., ic, ih, iw]
print_tensor(y)

printer("FLATTEN + TRANSPOSE + UNFLATTEN + FLATTEN:")
ic = ac.reshape(1, c).expand(h*w, c).reshape(h*w*heads, 1, d_qkv)
ih = ah.reshape(h, 1, 1).expand(h, w, heads).reshape(h*w*heads, 1, 1)
iw = aw.reshape(1, w, 1).expand(h, w, heads).reshape(h*w*heads, 1, 1)
y = x[..., ic, ih, iw]
print_tensor(y)

q = x.flatten(-2, -1).mT.unflatten(-1, [heads, 1, d_qkv]).flatten(-4, -3)
printer(list(y.shape) == [2, 30, 1, 4])
printer(list(y.shape) == list(q.shape))
printer(torch.all(y == q).item())
printer.hline()

printer("INPUT:")
print_tensor(x)

printer("UNFOLD:")
ih = ah.reshape(h, 1).expand(h, w).reshape(h, w, 1)
iw = aw.reshape(1, w).expand(h, w).reshape(h, w, 1)
dy = ak.reshape(k, 1).expand(k, k).flatten() - (k//2)
dx = ak.reshape(1, k).expand(k, k).flatten() - (k//2)
ih = (ih + dy) % h
iw = (iw + dx) % w
y = x[..., ih, iw]
print_tensor(y)

printer("UNFOLD + TRANSPOSE:")
ic = ac.reshape(c, 1)
ih = ah.reshape(h, 1).expand(h, w).reshape(h, w, 1, 1)
iw = aw.reshape(1, w).expand(h, w).reshape(h, w, 1, 1)
dy = ak.reshape(k, 1).expand(k, k).flatten() - (k//2)
dx = ak.reshape(1, k).expand(k, k).flatten() - (k//2)
ih = (ih + dy) % h
iw = (iw + dx) % w
y = x[..., ic, ih, iw]
print_tensor(y)

printer("UNFOLD + TRANSPOSE + RESHAPE:")
ic = ac.reshape(1, c).expand(h*w, c).reshape(h*w*heads, d_qkv, 1)
ih = ah.reshape(h, 1, 1).expand(h, w, heads).reshape(h*w*heads, 1, 1)
iw = aw.reshape(1, w, 1).expand(h, w, heads).reshape(h*w*heads, 1, 1)
dy = ak.reshape(k, 1).expand(k, k).flatten() - (k//2)
dx = ak.reshape(1, k).expand(k, k).flatten() - (k//2)
ih = (ih + dy) % h
iw = (iw + dx) % w
y = x[..., ic, ih, iw]
print_tensor(y)

k = torch.nn.functional.pad(x, [1, 1, 1, 1], "circular")
k = torch.nn.functional.unfold(k, 3)
k = k.mT.unflatten(-1, [2, 4, 9]).flatten(-4, -3)
printer(list(y.shape) == [2, 30, 4, 9])
printer(list(y.shape) == list(k.shape))
printer(torch.all(y == k).item())
printer.hline()
