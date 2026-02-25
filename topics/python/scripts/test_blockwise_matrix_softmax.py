import torch
import juml

def blockwise_matrix_softmax(
    x_io:   torch.Tensor,
    d1:     int,
    b1:     int,
    d2:     int,
    b2:     int,
):
    x_jbkd  =       x_io.reshape(d1, b1, d2, b2)
    x_jkbd  =     x_jbkd.transpose(1, 2)
    x_jkc   =     x_jkbd.reshape(d1, d2, b1*b2)
    y_jkc   =      x_jkc.softmax(2)
    y_jkbd  =      y_jkc.reshape(d1, d2, b1, b2)
    y_jbkd  =     y_jkbd.transpose(1, 2)
    y_io    =     y_jbkd.reshape(d1*b1, d2*b2)
    return y_io

torch.manual_seed(0)
juml.test_utils.torch_set_print_options(precision=5)

d1 = 5
b1 = 2
d2 = 4
b2 = 3

x_io = torch.normal(0, 1, [d1*b1, d2*b2])
y_io = blockwise_matrix_softmax(x_io, d1, b1, d2, b2)

print(x_io)
print(y_io)

i = 3
j = 1
print(i, j)
print(y_io[i*b1:i*b1+b1, j*b2:j*b2+b2])
print(y_io[i*b1:i*b1+b1, j*b2:j*b2+b2].sum())
