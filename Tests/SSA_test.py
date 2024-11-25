from __future__ import annotations
from egglog import runtime
from egglog import *

import sys
from typing import TypeAlias

#SSAObj: TypeAlias = runtime.RuntimeExpr
class Boolean(Expr):
    def __and__(self, a: Boolean) -> Boolean: ...

    def __or__(self, a: Boolean) -> Boolean: ...

class SSA(Expr):
    def __init__(self, value: i64Like) -> None: ...

    @classmethod
    def function(cls, var: StringLike) -> SSA: ...

    @classmethod
    def label(cls, value: i64Like) -> SSA: ...

    def __mul__(self, a: SSA) -> SSA: ...

    def __add__(self, a: SSA) -> SSA: ...

    def __sub__(self, a: SSA) -> SSA: ...

    @method(cost=2)
    def __lshift__(self, a: SSA) -> SSA: ...

    def to_bool(self) -> Boolean: ...


@function
def load(variable: SSA) -> SSA: ...

@function
def store(variable: SSA) -> SSA:
    return variable

@function
def branch(block: SSA, label: SSA) -> SSA: ...

@function
def cond_branch(condition: Boolean, label1: SSA, label2: SSA) -> SSA: ...

def istore(value: i64) -> SSA:
    return SSA(value)

label_block = relation("LabelAssign", SSA, SSA)

"""
def store(value: SSA | i64Like) -> SSA:
    if isinstance(value, SSAObj):
        return value
    else:
        return SSA(value)
"""


def init_simple_example(e: EGraph) -> tuple[SSA, SSA]:

    var2_1 = e.let("1.1", istore(6))
    var3_1 = e.let("2.1", istore(4))
    var5_1 = e.let("3.1", load(var2_1))
    var6_1 = e.let("4.1", load(var3_1))
    var7_1 = e.let("5.1", var5_1 - var6_1)
    var4_1 = e.let("6.1", store(var7_1))
    var8_1 = e.let("7.1", load(var4_1))

    var2_2 = e.let("1.2", istore(6))
    var3_2 = e.let("2.2", istore(4))
    var5_2 = e.let("3.2", load(var3_2))
    var6_2 = e.let("4.2", load(var2_2))
    var7_2 = e.let("5.2", var5_2 - var6_2)
    var8_2 = e.let("6.2", SSA(0) - var7_2)
    var4_2 = e.let("7.2", store(var8_2))
    var9_2 = e.let("8.2", load(var4_2))

    return (var8_1, var9_2)

def init_mult_example(e: EGraph) -> tuple[SSA, SSA, SSA]:
    var2_1 = e.let("1.1", SSA.function("scanf"))
    var9_1 = e.let("2.1", load(var2_1))
    var10_1 = e.let("3.1", var9_1 * SSA(2))
    var11_1 = e.let("4.1", load(var10_1))

    var2_2 = e.let("1.2", SSA.function("scanf"))
    var9_2 = e.let("2.2", load(var2_2))
    var10_2 = e.let("3.2", var9_2 * SSA(2))
    var11_2 = e.let("4.2", load(var10_2))

    var2_3 = e.let("1.3", SSA.function("scanf"))
    var9_3 = e.let("2.3", load(var2_3))
    var10_3 = e.let("3.3", var9_3 << SSA(1))
    var11_3 = e.let("4.3", load(var10_3))

    return (var11_1, var11_2, var11_3)


def init_eqClass01(e: EGraph) -> tuple[SSA, SSA]:
    var3_1 = e.let("1.1", istore(1))
    var4_1 = e.let("2.1", load(var3_1))
    var5_1 = e.let("3.1", var4_1.to_bool())
    var6_1 = e.let("4.1", SSA.label(6))
    var7_1 = e.let("5.1", SSA.label(7))
    e.let("6.1", cond_branch(var5_1, var6_1, var7_1))
    var2a_1 = e.let("7.1", istore(-1000))
    var8_1 = e.let("8.1", branch(var6_1, SSA.label(8)))
    e.let("9.1", label_block(var6_1, var2a_1))
    var2b_1 = e.let("10.1", istore(1000))
    var8_1 = e.let("11.1", branch(var7_1, SSA.label(8)))
    e.let("12.1", label_block(var7_1, var2b_1))
    var9_1 = e.let("13.1", load(var2a_1) + SSA(50))

    var3_2 = e.let("1.2", istore(0))
    var4_2 = e.let("2.2", load(var3_2))
    var5_2 = e.let("3.2", var4_2.to_bool())
    var6_2 = e.let("4.2", SSA.label(6))
    var7_2 = e.let("5.2", SSA.label(7))
    cond_2 = e.let("6.2", cond_branch(var5_2, var6_2, var7_2))
    var2a_2 = e.let("7.2", istore(1000))
    var8_2 = e.let("8.2", branch(var6_2, SSA.label(8)))
    e.let("9.2", label_block(var6_2, var2a_2))
    var2b_2 = e.let("10.2", istore(-1000))
    var8_2 = e.let("11.2", branch(var7_1, SSA.label(8)))
    e.let("12.2", label_block(var7_2, var2b_2))
    var9_2 = e.let("13.2", load(var2a_1) + SSA(50))

    return (var9_1, var9_2)

def display_and_saturate(e: EGraph, *vars: SSA) -> None:
    e.display()
    input("Press Enter to continue...")

    e.saturate()
    e.display()

    for v in vars:
        print(e_graph.extract(v))

    e.check(eq(vars[0]).to(vars[1]))


if __name__ == "__main__":
    e_graph: EGraph = EGraph()
    TRUE = constant("True", Boolean)
    FALSE = constant("False", Boolean)
    flag: str = ""

    a, b, c = vars_("a b c", SSA)
    x, y = vars_("x y", i64)
    v = var("v", String)
    c = var("t", Boolean)
    e_graph.register(
        rewrite(SSA(x) + SSA(y)).to(SSA(x + y)),
        rewrite(SSA(x) * SSA(y)).to(SSA(x * y)),
        rewrite(SSA(x) - SSA(y)).to(SSA(x - y)),
        rewrite(SSA(x) << SSA(y)).to(SSA(x << y)),
        rewrite(a * SSA(x)).to(a << SSA(x / 2),
                               eq(x % 2).to(0), x < 5),
        rewrite(a << SSA(x)).to(a * SSA(x * 2)),
        rewrite(load(a)).to(a),
        rewrite(SSA(x).to_bool()).to(TRUE,
                                     ne(x).to(0)),
        rewrite(SSA(x).to_bool()).to(FALSE,
                                     eq(x).to(0)),
        rewrite(cond_branch(TRUE, a, b)).to(a),
        rewrite(cond_branch(FALSE, a, b)).to(b),
        rewrite(branch(a, b)).to(a),
        rule(label_block(SSA.label(x), a)).then(set_(SSA.label(x)).to(a)),
    )
    if len(sys.argv[1:]) > 0:
        flag = sys.argv[1]

    if flag == "":
        test_var = e_graph.let("0.1", SSA(2) * SSA(4))
        display_and_saturate(e_graph, test_var)

    elif int(flag) == 1:
        display_and_saturate(e_graph, *init_simple_example(e_graph))

    elif int(flag) == 2:
        display_and_saturate(e_graph, *init_eqClass01(e_graph))

    elif int(flag) == 3:
        display_and_saturate(e_graph, *init_mult_example(e_graph))
