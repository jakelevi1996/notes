# `topics/pytorch/scripts/README.md`

## Contents

- [`topics/pytorch/scripts/README.md`](#topicspytorchscriptsreadmemd)
  - [Contents](#contents)
  - [`topics/pytorch/scripts/demo_double_descent.py`](#topicspytorchscriptsdemo_double_descentpy)
  - [`topics/pytorch/scripts/demo_quantile.py`](#topicspytorchscriptsdemo_quantilepy)
  - [`topics/pytorch/scripts/demo_conv_vs_linear.py`](#topicspytorchscriptsdemo_conv_vs_linearpy)

## `topics/pytorch/scripts/demo_double_descent.py`

```sh
python topics/pytorch/scripts/demo_double_descent.py
# Time taken for `main` = 6.8436 seconds
```

![](../img/demo_double_descent_i300n10,30,100,300,1000,3000,10000o10r5se0st0.001.png)

```sh
python topics/pytorch/scripts/demo_double_descent.py --input_dim 100
# Time taken for `main` = 21.5127 seconds
```

![](../img/demo_double_descent_i100n10,30,100,300,1000,3000,10000o10r5se0st0.001.png)

```sh
python topics/pytorch/scripts/demo_double_descent.py --input_dim 1000
# Time taken for `main` = 18.2575 seconds
```

![](../img/demo_double_descent_i1000n10,30,100,300,1000,3000,10000o10r5se0st0.001.png)

## `topics/pytorch/scripts/demo_quantile.py`

```
topics/pytorch/scripts/demo_quantile.py
```

![](../img/demo_quantile.png)

## `topics/pytorch/scripts/demo_conv_vs_linear.py`

```
python topics/pytorch/scripts/demo_conv_vs_linear.py
```

![](../img/demo_conv_vs_linear_iFn100,64,80,60r5.png)
```
python topics/pytorch/scripts/demo_conv_vs_linear.py --include_reshape
```

![](../img/demo_conv_vs_linear_iTn100,64,80,60r5.png)
