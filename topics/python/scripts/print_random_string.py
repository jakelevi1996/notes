from jutility import util, cli
import numpy as np

def main(
    seed:       (int | None),
    n:          int,
    lower:      int,
    upper:      int,
    numeric:    int,
    special:    int,
    prefix:     str,
):
    rng = np.random.default_rng(seed)

    table = util.Table.key_value()
    table.update(
        k="AlphaNum",
        v=AlphaNum(lower, numeric, prefix).sample(rng),
    )
    table.update(
        k="AlphaNumSpecial",
        v=AlphaNumSpecial(lower, upper, numeric, special).sample(rng),
    )
    table.update(
        k="Xx",
        v="`%s`" % Xx(n).sample(rng),
    )
    util.hline()

class StrGen:
    def sample(self, rng: np.random.Generator) -> str:
        raise NotImplementedError()

    def get_char_range(self, c1: str, c2: str) -> list[str]:
        return [chr(i) for i in range(ord(c1), ord(c2)+1)]

class Block:
    def __init__(self, char_list: list[str], n: int):
        self.char_list = char_list
        self.n = n

    def sample(self, rng: np.random.Generator) -> str:
        return "".join(rng.choice(self.char_list, self.n, replace=False))

class AlphaNum(StrGen):
    def __init__(
        self,
        lower:      int,
        numeric:    int,
        prefix:     int,
    ):
        self.prefix = prefix
        self.blocks = [
            Block(self.get_char_range("a", "z"), lower),
            Block(self.get_char_range("0", "9"), numeric),
        ]

    def sample(self, rng: np.random.Generator) -> str:
        s = "".join(b.sample(rng) for b in self.blocks)
        return self.prefix + "".join(rng.permutation(list(s)))

class AlphaNumSpecial(StrGen):
    def __init__(
        self,
        lower:      int,
        upper:      int,
        numeric:    int,
        special:    int,
    ):
        self.blocks = [
            Block(self.get_char_range("a", "z"), lower),
            Block(self.get_char_range("A", "Z"), upper),
            Block(self.get_char_range("0", "9"), numeric),
            Block(list("!?%_-+="), special),
        ]

    def sample(self, rng: np.random.Generator) -> str:
        s = "".join(b.sample(rng) for b in self.blocks)
        return "".join(rng.permutation(list(s)))

class Xx(StrGen):
    def __init__(self, n: int):
        self.n = n

    def sample(self, rng: np.random.Generator) -> str:
        return "".join(rng.choice(["X", "x", " "], self.n))

if __name__ == "__main__":
    parser = cli.Parser(
        cli.Arg("seed",     type=int, default=None),
        cli.Arg("n",        type=int, default=50),
        cli.Arg("lower",    type=int, default=4),
        cli.Arg("upper",    type=int, default=4),
        cli.Arg("numeric",  type=int, default=4),
        cli.Arg("special",  type=int, default=4),
        cli.Arg("prefix",   type=str, default="_"),
    )
    args = parser.parse_args()

    with util.Timer("main"):
        main(**args.get_kwargs())
