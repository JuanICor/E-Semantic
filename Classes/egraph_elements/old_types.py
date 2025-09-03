from __future__ import annotations
from typing import TypeAlias

from egglog import Expr, function as eggFunction, relation, Unit
from egglog.builtins import (i64Like, String, StringLike, BoolLike, Vec, Map,
                             Set)

Var: TypeAlias = String


class Function(Expr):

    def __init__(self, name: StringLike, traces: Set[Trace]) -> None:
        ...


class Trace(Expr):

    def __init__(self, instructions: Vec[Instruction], state: State) -> None:
        ...

    def return_value(self) -> Operand:
        ...


class State(Expr):

    def __init__(self, relation: Map[Var, Operand]) -> None:
        ...

    @classmethod
    def empty(self) -> State:
        ...

    def __getitem__(self, key: Var) -> Operand:
        ...

    def insert(self, instr: Instruction) -> State:
        ...

    def contains(self, key: Var) -> Unit:
        ...


class Instruction(Expr):

    def __init__(self, result_var: Var, operation: Operand) -> None:
        ...

    @classmethod
    def ret(cls, variable: Var) -> Instruction:
        ...


class Operand(Expr):

    def __init__(self, value: Var) -> None:
        ...

    @classmethod
    def integer(cls, value: i64Like) -> Operand:
        ...

    @classmethod
    def boolean(cls, value: BoolLike) -> Operand:
        ...

    @classmethod
    def function_call(cls, function_name: String) -> Operand:
        ...

    def __mul__(self, other: Operand) -> Operand:
        ...

    def __add__(self, other: Operand) -> Operand:
        ...

    def __sub__(self, other: Operand) -> Operand:
        ...

    def __lshift__(self, other: Operand) -> Operand:
        ...

    def __and__(self, other: Operand) -> Operand:
        ...

    def __or__(self, other: Operand) -> Operand:
        ...


@eggFunction(unextractable=True)
def eval_instructions(instructions: Vec[Instruction], state: State,
                      pcounter: i64Like) -> State:
    ...


@eggFunction(unextractable=True)
def semantic_function(operand: Operand, relation: Map[Var,
                                                      Operand]) -> Operand:
    ...


is_declaration = relation("Declaration", Function)
