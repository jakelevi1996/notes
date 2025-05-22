from jutility import util, cli
import numpy as np

def main(
    args:   cli.ParsedArgs,
    n:      int,
    seed:   int,
):
    rng = np.random.default_rng(seed)
    with cli.verbose:
        sg = args.init_object("strgen")
        assert isinstance(sg, StrGen)

    print("```\n%s\n```" % sg.sample(n, rng, True))

class StrGen:
    def get_char_list(self) -> list[str]:
        raise NotImplementedError()

    def get_char_range(self, c1: str, c2: str) -> list[str]:
        return [chr(i) for i in range(ord(c1), ord(c2)+1)]

    def sample(self, n: int, rng: np.random.Generator, replace: bool) -> str:
        # cl = self.get_char_list()
        # return "".join(cl[i] for i in rng.integers(0, len(cl), n).tolist())
        return "".join(rng.choice(self.get_char_list(), n, replace))

    @classmethod
    def get_cli_arg(cls) -> cli.ObjectArg:
        return cli.ObjectArg(cls)

class Lower(StrGen):
    def get_char_list(self) -> list[str]:
        return self.get_char_range("a", "z")

class Upper(StrGen):
    def get_char_list(self) -> list[str]:
        return self.get_char_range("A", "Z")

class Numeric(StrGen):
    def get_char_list(self) -> list[str]:
        return self.get_char_range("0", "9")

class Special(StrGen):
    def get_char_list(self) -> list[str]:
        return list("!£$%_-+=")

class AlphaNumSpecial(StrGen):
    def get_subgens(self) -> list[StrGen]:
        return [Lower(), Upper(), Numeric(), Special()]

    def get_char_list(self) -> list[str]:
        return [
            c
            for sg  in self.get_subgens()
            for c   in sg.get_char_list()
        ]

class AlphaNumSpecialBlocks(AlphaNumSpecial):
    def __init__(
        self,
        lower:      int,
        upper:      int,
        numeric:    int,
        special:    int,
    ):
        self.block_lens = [lower, upper, numeric, special]

    def sample(self, n: int, rng: np.random.Generator, replace: bool) -> str:
        return "".join(
            sg.sample(ni, rng, False)
            for sg, ni in zip(self.get_subgens(), self.block_lens)
        )

    @classmethod
    def get_cli_arg(cls) -> cli.ObjectArg:
        return cli.ObjectArg(
            cls,
            cli.Arg("lower",    type=int, default=4),
            cli.Arg("upper",    type=int, default=4),
            cli.Arg("numeric",  type=int, default=4),
            cli.Arg("special",  type=int, default=4),
        )

class AlphaNumSpecialBlocksShuffle(AlphaNumSpecialBlocks):
    def sample(self, n: int, rng: np.random.Generator, replace: bool) -> str:
        s = AlphaNumSpecialBlocks(*self.block_lens).sample(n, rng, False)
        return "".join(rng.permutation(list(s)))

class Xx(StrGen):
    def get_char_list(self) -> list[str]:
        return ["X", "x", " "]

def get_all() -> list[type[StrGen]]:
    return [
        AlphaNumSpecial,
        AlphaNumSpecialBlocks,
        AlphaNumSpecialBlocksShuffle,
        Xx,
    ]

if __name__ == "__main__":
    parser = cli.Parser(
        cli.Arg("n",    type=int, default=50),
        cli.Arg("seed", type=int, default=None),
        cli.ObjectChoice(
            "strgen",
            *[sg_type.get_cli_arg() for sg_type in get_all()],
            default="Xx",
            is_group=True,
        )
    )
    args = parser.parse_args()

    with util.Timer("main"):
        main(args, **args.get_kwargs())
