import torch
import juml

juml.test_utils.torch_set_print_options()

n = 5

x = torch.arange(n*n).reshape(n, n) + 1.0
print(x)

rc = [
    [row, col]
    for row in range(n)
    for col in range(row, n)
]
r, c = zip(*rc)

print(x[r, c])
