from __future__ import annotations
from typing import TypeAlias

from egglog import Expr, function as eggFunction
from egglog.builtins import i64Like, BoolLike, StringLike, Vec
from egglog.conversion import converter

converter(list, Vec, lambda l: Vec(*l))


class Leaf(Expr):

    @classmethod
    def int(cls, value: i64Like) -> Leaf:
        ...

    @classmethod
    def bool(cls, value: BoolLike) -> Leaf:
        ...

    @classmethod
    def string(cls, value: StringLike) -> Leaf:
        ...

    @classmethod
    def state(cls, value: StringLike) -> Leaf:
        ...


Components: TypeAlias = Vec[Leaf] | list[Leaf]


class Function(Expr):

    def __init__(self, name: StringLike, traces: Components) -> None:
        ...


@eggFunction
def alloca(state: Leaf) -> Leaf:
    ...


@eggFunction
def store(ptr: Leaf, data: Leaf, state: Leaf) -> Leaf:
    ...


@eggFunction
def load(ptr: Leaf, state: Leaf) -> Leaf:
    ...


@eggFunction
def truncate(argument: Leaf) -> Leaf:
    ...


@eggFunction
def add(lhs: Leaf, rhs: Leaf) -> Leaf:
    ...


@eggFunction
def mul(lhs: Leaf, rhs: Leaf) -> Leaf:
    ...


@eggFunction
def shl(lhs: Leaf, rhs: Leaf) -> Leaf:
    ...


@eggFunction
def sub(lhs: Leaf, rhs: Leaf) -> Leaf:
    ...


@eggFunction(egg_fn='¬')
def neg(literal: Leaf) -> Leaf:
    ...


@eggFunction
def equals(lhs: Leaf, rhs: Leaf) -> Leaf:
    ...


@eggFunction
def nequals(lhs: Leaf, rhs: Leaf) -> Leaf:
    ...


@eggFunction(egg_fn='slt')
def strict_less(lhs: Leaf, rhs: Leaf) -> Leaf:
    ...


@eggFunction(egg_fn='sgt')
def strict_greater(lhs: Leaf, rhs: Leaf) -> Leaf:
    ...


CallArgs: TypeAlias = Vec[Leaf] | list[Leaf]


@eggFunction
def call(name: StringLike, arguments: CallArgs) -> Leaf:
    ...


@eggFunction(egg_fn=chr(0x03B3))
def gamma(condition: Leaf, true_value: Leaf, false_value: Leaf) -> Leaf:
    ...

@eggFunction(egg_fn=chr(0x03BC))
def mu(init_value: Leaf, iterated_value: Leaf) -> Leaf:
    ...
