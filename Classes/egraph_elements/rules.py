from __future__ import annotations
from typing import Iterable

from egglog import ruleset, unstable_combine_rulesets
from egglog.egraph import rewrite, ne, eq
from egglog.builtins import i64, Vec, String

from .nodes import (Function, Leaf, load, store, alloca, add, sub, mul, shl,
                    gamma, neg, truncate, equals)


@ruleset
def function_ruleset(name: String, roots: Vec[Leaf]) -> Iterable:
    return [
        rewrite(Function(name, roots)).to(roots[0],
                                        roots.length() <= i64(1)),
    ]


@ruleset
def arithmetic_ruleset(x: i64, y: i64, l1: Leaf, l2: Leaf,
                       l3: Leaf) -> Iterable:
    return [
        # Simple Reduction
        rewrite(add(Leaf.int(x), Leaf.int(y))).to(Leaf.int(x + y)),
        rewrite(sub(Leaf.int(x), Leaf.int(y))).to(Leaf.int(x - y)),
        rewrite(mul(Leaf.int(x), Leaf.int(y))).to(Leaf.int(x * y)),
        # Arithmetic Relations
        rewrite(add(l1, l1)).to(mul(l1, Leaf.int(2))),
        rewrite(add(l1, l1)).to(shl(l1, Leaf.int(1))),
        rewrite(mul(l1, Leaf.int(4))).to(shl(l1, Leaf.int(2))),
        # Integer Commitativity
        rewrite(add(l1, l2)).to(add(l2, l1)),
        rewrite(mul(l1, l2)).to(mul(l2, l1)),
        # Integer Assosiativity
        rewrite(add(l1, add(l2, l3))).to(add(add(l1, l2), l3))
    ]


@ruleset
def boolean_ruleset(b: Leaf) -> Iterable:
    return [
        # ¬
        rewrite(neg(neg(b))).to(b),
        rewrite(neg(Leaf.bool(True))).to(Leaf.bool(False)),
        rewrite(neg(Leaf.bool(False))).to(Leaf.bool(True)),
        rewrite(neg(Leaf.int(0))).to(Leaf.int(1)),
        rewrite(neg(Leaf.int(1))).to(Leaf.int(0)),
        # ==
        rewrite(equals(b, b)).to(Leaf.bool(True))
    ]


@ruleset
def memory_ruleset(data: Leaf, ptr: Leaf, ptr2: Leaf, state: Leaf) -> Iterable:
    return [
        rewrite(load(ptr, store(ptr2, data, state))).to(load(ptr, state)),
        rewrite(load(ptr, store(ptr, data, state))).to(data)
    ]


@ruleset
def gated_operands_ruleset(cond: Leaf, truev: Leaf, falsev: Leaf,
                           x: i64) -> Iterable:
    return [
        # Gamma Reduction
        rewrite(gamma(Leaf.bool(True), truev, falsev)).to(truev),
        rewrite(gamma(Leaf.bool(False), truev, falsev)).to(falsev),
        rewrite(gamma(Leaf.int(x), truev,
                      falsev)).to(truev,
                                  ne(Leaf.int(x)).to(Leaf.int(0))),
        rewrite(gamma(Leaf.int(x), truev,
                      falsev)).to(falsev,
                                  eq(Leaf.int(x)).to(Leaf.int(0))),
        # Branch Changes
        rewrite(gamma(cond, truev, falsev)).to(gamma(neg(cond), falsev,
                                                     truev)),
    ]


@ruleset
def conversion_operands_ruleset(x: Leaf) -> Iterable:
    return [
        rewrite(truncate(x)).to(x),
    ]


graph_ruleset = unstable_combine_rulesets(arithmetic_ruleset, boolean_ruleset,
                                          memory_ruleset,
                                          gated_operands_ruleset,
                                          conversion_operands_ruleset)
