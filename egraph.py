# mypy: disable-error-code=empty-body

from __future__ import annotations
from behemoth import *
from egglog import *

from typing import Callable, TypeAlias

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

    def __lshift__(self, other: Arithmetics) -> Arithmetics:
        pass


@function
def sum(x: Arithmetics | Unit, y: Arithmetics | Unit) -> Arithmetics:
    pass

@function
def mult(x: Arithmetics | Unit, y: Arithmetics | Unit) -> Arithmetics:
    pass

@function
def lshift(x: Arithmetics | Unit, y: Arithmetics | Unit) -> Arithmetics:
    pass

assignment: ArithmeticsRelation = relation("Assign", Arithmetics | Unit, Arithmetics | Unit)    #type: ignore
                                                                                                # Mypy complains about not being overload functions, but is not necessary
a, b = vars_("a b", Arithmetics)
x, y = vars_("x y", i64)
v = var("v", String)

egraph.register(
    rewrite(sum(a, b)).to(a + b),
    rewrite(mult(a, b)).to(a * b),
    rewrite(lshift(a, b)).to(a << b),
    rewrite(Arithmetics(x) + Arithmetics(y)).to(Arithmetics(x + y)),
    rewrite(Arithmetics(x) * Arithmetics(y)).to(Arithmetics(x * y)),
    rewrite(Arithmetics(x) << Arithmetics(y)).to(Arithmetics(x << y)),
    rule(assignment(Arithmetics.var(v), b)).then(
        set_(Arithmetics.var(v)).to(b),
        delete(Arithmetics.var(v))
    )
)