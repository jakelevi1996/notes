import torch

n = 10
o = 5

x_no = torch.normal(0, 1, [n, o])
t_n  = torch.randint(0, o, [n])

print(x_no)
print(t_n)

loss = torch.mean(
    - x_no.take_along_dim(t_n.unsqueeze(-1), -1)
    + x_no.logsumexp(-1, True)
)
print(loss)
print(torch.nn.functional.cross_entropy(x_no, t_n))
