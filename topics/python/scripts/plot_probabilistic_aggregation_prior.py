import torch
from jutility import plotting, util

bx = 10
hx = 20
by = bx + (bx - 1) * (hx - 1)
assert by == hx * (bx - 1) + 1
assert by == hx * bx - (hx - 1)
print(util.format_dict({"bx": bx, "hx": hx, "by": by}))

p = torch.zeros([by])
p[0] = 1
c = torch.stack([p.roll(i) for i in range(bx)], dim=0)
x = torch.arange(by).tolist()
cp = plotting.ColourPicker(hx, False)
lines = [plotting.Step(x, p.tolist(), c=cp.next(), where="post")]
for _ in range(hx - 1):
    p = c.sum(dim=0) / bx
    c = torch.stack([p.roll(i) for i in range(bx)], dim=0)
    lines.append(plotting.Step(x, p.tolist(), c=cp.next(), where="post"))

plotting.plot(*lines, ylim=[0, 1.1/bx])
