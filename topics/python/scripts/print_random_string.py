import numpy as np

rng = np.random.default_rng(0)

c = ["X", "x", " "]
n = 50
s = "".join(c[i] for i in rng.integers(0, len(c), n).tolist())

print(s)
