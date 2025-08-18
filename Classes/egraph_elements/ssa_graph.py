"""
First approach when trying to develop the tool.
Is not longer used.
"""

from __future__ import annotations
from egglog import (Expr, i64Like, StringLike, i64, rewrite, rule, vars_, var,
                    ruleset, function, method, eq, ne, constant, Vec, union,
                    delete, relation)


class Boolean(Expr):

    def __and__(self, other: Boolean) -> Boolean:
        ...

    def __or__(self, other: Boolean) -> Boolean:
        ...


class SSA(Expr):

    def __init__(self, value: i64Like) -> None:
        ...

    @classmethod
    def function(self, func_name: StringLike) -> SSA:
        ...

    @method(cost=5)
    @classmethod
    def label(cls, label: StringLike) -> SSA:
        ...

    def __add__(self, a: SSA) -> SSA:
        ...

    def __sub__(self, a: SSA) -> SSA:
        ...

    def __ne__(self, a: SSA) -> SSA:
        ...

    def to_bool(self) -> Boolean:
        ...


@function
def cond_branch(condition: SSA, if_true: SSA, if_false: SSA) -> SSA:
    ...


label_block = relation("LabelBody", SSA, Vec[SSA])

T = constant("True", Boolean)
F = constant("False", Boolean)

a, b, c = vars_("a b c", SSA)
x, y = vars_("x y", i64)
if_true, if_false = vars_("true false", SSA)
block_code = var("bc", Vec[SSA])


@ruleset
def SSA_basic_ruleset():
    yield rewrite(SSA(x) + SSA(y)).to(SSA(x + y))
    yield rewrite(SSA(x) - SSA(y)).to(SSA(x - y))
    yield rewrite(SSA(x).to_bool()).to(T, ne(x).to(0))
    yield rewrite(SSA(x).to_bool()).to(F, eq(x).to(0))
    yield rewrite(cond_branch(a, if_true,
                              if_false)).to(if_true,
                                            eq(a.to_bool()).to(T))
    yield rewrite(cond_branch(a, if_true,
                              if_false)).to(if_false,
                                            eq(a.to_bool()).to(F))
    yield rule(cond_branch(a, b, c)).then(a.to_bool())
    yield rule(label_block(a, block_code),
               block_code.length().bool_gt(0)).then(
                   union(a).with_(block_code[0]),
                   delete(label_block(a, block_code)), block_code.pop())
