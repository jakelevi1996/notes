from jutility import util

class ChangeCounter:
    """
    See [Many Hard Leetcode Problems are Easy Constraint Problems](
    https://buttondown.com/hillelwayne/archive/many-hard-leetcode-problems-are-easy-constraint/
    ):

    > Given a set of coin denominations, find the minimum number of coins
    required to make change for a given number. IE for USA coinage and 37
    cents, the minimum number is four (quarter, dime, 2 pennies).
    """
    def __init__(self, *denoms: int):
        self._denoms = sorted(denoms, reverse=True)

    def get_change(self, value: int):
        self.count = 0
        best_valid = None
        for d in self._denoms:
            coins_used = self._recurse(d, value - d, [d], best_valid)
            if (best_valid is None) or (len(coins_used) < len(best_valid)):
                best_valid = coins_used

        return best_valid, self.count

    def _recurse(
        self,
        coin:       int,
        value_left: int,
        coins_used: list[int],
        best_valid: list[int] | None,
    ) -> (list[int] | None):
        self.count += 1
        if value_left == 0:
            print("Found solution: %s" % coins_used)
            if (best_valid is None) or (len(coins_used) < len(best_valid)):
                best_valid = coins_used
        elif (best_valid is None) or (len(coins_used) < len(best_valid)):
            for d in self._denoms:
                if (d <= coin) and (d <= value_left):
                    best_valid = self._recurse(
                        d,
                        value_left - d,
                        coins_used + [d],
                        best_valid,
                    )

        return best_valid

util.print_hline(ChangeCounter(25, 10, 1).get_change(37))
util.print_hline(ChangeCounter(10, 9, 1).get_change(37))
util.print_hline(ChangeCounter(10, 9, 1).get_change(38))
util.print_hline(ChangeCounter(10, 9, 1).get_change(35))
util.print_hline(ChangeCounter(10, 8, 1).get_change(35))
