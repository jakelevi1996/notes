from jutility import util

table = util.Table(
    util.Column("a"),
    util.Column("b"),
    util.Column("c"),
    util.Column("ab",   title="a^b"),
    util.Column("bc",   title="b^c"),
    util.Column("ab_c", title="(a^b)^c"),
    util.Column("a_bc", title="a^(b^c)"),
    util.Column("eq"),
)

for a in [0, 1]:
    for b in [0, 1]:
        for c in [0, 1]:
            ab = a ^ b
            bc = b ^ c
            ab_c = ab ^ c
            a_bc = a ^ bc
            table.update(
                a=a,
                b=b,
                c=c,
                ab=ab,
                bc=bc,
                ab_c=ab_c,
                a_bc=a_bc,
                eq=(ab_c==a_bc),
            )
