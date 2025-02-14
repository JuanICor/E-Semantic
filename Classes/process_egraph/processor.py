"""
Resolver class for the egraph process
"""
from collections.abc import Callable
from egglog import EGraph, Ruleset
from typing import TypeAlias

from Classes.ssa_graph import SSA

BinaryOperation: TypeAlias = Callable[[SSA, SSA], SSA]


class EgraphProcessor:
    _regs_mapping: dict[str, SSA]

    def __init__(self, ruleset: Ruleset) -> None:
        self.egraph = EGraph()
        self._regs_mapping = {}
        self._ruleset = ruleset
        self._egraph_id: int = 0

    def _value_to_SSA(self, argument: str) -> SSA:
        if argument.isdigit():
            return SSA(int(argument))

        return self._regs_mapping[argument]

    def _generate_egraph_id(self) -> str:
        id = str(self._egraph_id)
        self._egraph_id += 1

        return id

    def _saturate_graph(self) -> None:
        self.egraph.run(self._ruleset.saturate())

    def write_binary_op(self, operation: BinaryOperation, res_reg: str,
                        arg1: str, arg2: str) -> None:
        ssa_arg1 = self._value_to_SSA(arg1)
        ssa_arg2 = self._value_to_SSA(arg2)

        self._regs_mapping[res_reg] = self.egraph.let(
            self._generate_egraph_id(), operation(ssa_arg1, ssa_arg2))

    def write_load_or_store(self, res_reg: str, temp_reg: str) -> None:
        temp_ssa = self._value_to_SSA(temp_reg)

        self._regs_mapping[res_reg] = self.egraph.let(
            self._generate_egraph_id(), temp_ssa)

    def write_function(self, res_reg: str, function_name: str) -> None:
        self._regs_mapping[res_reg] = self.egraph.let(
            self._generate_egraph_id(), SSA.function(function_name))

    def register_expression(self) -> None:
        ...

    def extract_expression(self, expr_id: str) -> None:
        expr_ssa = self._regs_mapping[expr_id]

        self._saturate_graph()

        print(f"Extracted expression: {self.egraph.extract(expr_ssa)}")
