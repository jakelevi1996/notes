from jutility import util, cli
import numpy as np

def main(
    args: cli.ParsedArgs,
    seed: int,
):
    rng = np.random.default_rng(seed)
    with cli.verbose:
        sg = args.init_object("strgen")
        assert isinstance(sg, StrGen)

    print("```\n%s\n```" % sg.sample(rng))

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

    @classmethod
    def get_cli_arg(cls) -> cli.ObjectArg:
        return cli.ObjectArg(
            cls,
            cli.Arg("lower",    type=int, default=4),
            cli.Arg("numeric",  type=int, default=4),
            cli.Arg("prefix",   type=str, default="_"),
        )

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
            Block(list("!£$%_-+="), special),
        ]

    def sample(self, rng: np.random.Generator) -> str:
        s = "".join(b.sample(rng) for b in self.blocks)
        return "".join(rng.permutation(list(s)))

    @classmethod
    def get_cli_arg(cls) -> cli.ObjectArg:
        return cli.ObjectArg(
            cls,
            cli.Arg("lower",    type=int, default=4),
            cli.Arg("upper",    type=int, default=4),
            cli.Arg("numeric",  type=int, default=4),
            cli.Arg("special",  type=int, default=4),
        )

class Xx(StrGen):
    def __init__(self, n: int):
        self.n = n

    def sample(self, rng: np.random.Generator) -> str:
        return "".join(rng.choice(["X", "x", " "], self.n))

    @classmethod
    def get_cli_arg(cls) -> cli.ObjectArg:
        return cli.ObjectArg(
            cls,
            cli.Arg("n", type=int, default=50),
        )

if __name__ == "__main__":
    parser = cli.Parser(
        cli.Arg("seed", type=int, default=None),
        cli.ObjectChoice(
            "strgen",
            AlphaNum.get_cli_arg(),
            AlphaNumSpecial.get_cli_arg(),
            Xx.get_cli_arg(),
            default="Xx",
            is_group=True,
        )
    )
    args = parser.parse_args()

    with util.Timer("main"):
        main(args, **args.get_kwargs())
