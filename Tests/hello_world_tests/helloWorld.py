from __future__ import annotations
from egglog import *

egraph = EGraph()

@egraph.class_
class CompMath(Expr):
    def __init__(self, value: i64Like) -> None:
        pass

    @classmethod
    def var(cls, v: StringLike) -> CompMath:
        pass

    def __add__(self, other: CompMath) -> CompMath:
        pass

    def __mul__(self, other: CompMath) -> CompMath:
        pass

    def __lt__(self, other: CompMath) -> CompMath:
        pass

    def __gt__(self, other: CompMath) -> CompMath:
        pass

    def val(self) -> i64:
        pass

a, b = vars_("a b", CompMath)
x, y = vars_("x y", i64)

egraph.register(
    rewrite(a > b).to(CompMath(-1) * a < CompMath(-1) * b),
    rewrite(a < b).to(CompMath(-1) * a > CompMath(-1) * b),
    rewrite(CompMath(x) + CompMath(y)).to(CompMath(x + y)),
    rewrite(CompMath(x) * CompMath(y)).to(CompMath(x * y)),
)

if __name__ == "__main__":
    expr1 = egraph.let("expr1", CompMath(6) + CompMath(2) > CompMath(7))
    expr2 = egraph.let("expr2", CompMath(-8) < CompMath(-1) * CompMath(7))

    egraph.run(5)

    try:
        egraph.check(eq(expr1).to(expr2))
        print("The expressions are equal.")
    except Exception:
        print("The expressions are not equal.")
