from __future__ import annotations
from egglog import *

egraph = EGraph()

@egraph.class_
class Arithmetics(Expr):
    def __init__(self, value: i64Like) -> None:
        pass

    @classmethod
    def var(cls, v: StringLike) -> Arithmetics:
        pass

    def __add__(self, other: Arithmetics) -> Arithmetics:
        pass

    def __mul__(self, other: Arithmetics) -> Arithmetics:
        pass

@function
def sum(x: Arithmetics, y: Arithmetics) -> Arithmetics:
    pass

@function
def mult(x: Arithmetics, y: Arithmetics) -> Arithmetics:
    pass

a, b = vars_("a b", Arithmetics)
x, y = vars_("x y", i64)

egraph.register(
    rewrite(a > b).to(Arithmetics(-1) * a < Arithmetics(-1) * b),
    rewrite(a < b).to(Arithmetics(-1) * a > Arithmetics(-1) * b),
    rewrite(sum(a, b)).to(a + b),
    rewrite(mult(a, b)).to(a * b),
    rewrite(Arithmetics(x) + Arithmetics(y)).to(Arithmetics(x + y)),
    rewrite(Arithmetics(x) * Arithmetics(y)).to(Arithmetics(x * y)),
)