"""
Resolver class for the egraph process
"""
from collections.abc import Callable
from typing import TypeAlias
from egglog import EGraph, Ruleset

from Classes.ssa_graph import SSA, cond_branch

UnaryOperation: TypeAlias = Callable[[SSA], SSA]
BinaryOperation: TypeAlias = Callable[[SSA, SSA], SSA]


class EgraphProcessor:
    _regs_mapping: dict[str, SSA]

    def __init__(self, ruleset: Ruleset) -> None:
        self.egraph = EGraph()
        self._regs_mapping = {}
        self._ifs_stack = []
        self._ruleset = ruleset
        self._egraph_id: int = 0

    def _value_to_SSA(self, argument: str | int) -> SSA:
        if isinstance(argument, int):
            return SSA(argument)

        return self._regs_mapping[argument]

    def _generate_egraph_id(self) -> str:
        id = str(self._egraph_id)
        self._egraph_id += 1

        return id

    def _saturate_graph(self) -> None:
        self.egraph.run(self._ruleset.saturate())

    def write_unary_op(self, operation: UnaryOperation, res_reg: str,
                       expr: str | int) -> None:

        ssa_expr = self._value_to_SSA(expr)

        self._regs_mapping[res_reg] = self.egraph.let(
            self._generate_egraph_id(), operation(ssa_expr))

    def write_binary_op(self, operation: BinaryOperation, res_reg: str,
                        arg1: str | int, arg2: str | int) -> None:

        ssa_arg1 = self._value_to_SSA(arg1)
        ssa_arg2 = self._value_to_SSA(arg2)

        self._regs_mapping[res_reg] = self.egraph.let(
            self._generate_egraph_id(), operation(ssa_arg1, ssa_arg2))

    def write_cond_branch(self, condition: str, if_true: str,
                          if_false: str) -> None:

        ssa_condition = self._value_to_SSA(condition)
        ssa_true = self._value_to_SSA(if_true)
        ssa_false = self._value_to_SSA(if_false)

        self._ifs_stack.append(
            self.egraph.let(self._generate_egraph_id(),
                            cond_branch(ssa_condition, ssa_true, ssa_false)))

    def write_load_or_store(self, res_reg: str, temp_reg: str | int) -> None:
        temp_ssa = self._value_to_SSA(temp_reg)

        self._regs_mapping[res_reg] = self.egraph.let(
            self._generate_egraph_id(), temp_ssa)

    def write_function(self, res_reg: str, function_name: str) -> None:
        self._regs_mapping[res_reg] = self.egraph.let(
            self._generate_egraph_id(), SSA.function(function_name))

    def register_expression(self) -> None:
        ...

    def register_blocks(self, block_label: str) -> None:
        self._regs_mapping[block_label] = self.egraph.let(
            self._generate_egraph_id(),
            SSA.label(block_label[:block_label.find('.')] + '_' +
                      block_label[block_label.rfind('/') + 1:]))

    def extract_expression(self, expr_id: str) -> str:
        expr_ssa = self._regs_mapping[expr_id]

        self._saturate_graph()

        return str(self.egraph.extract(expr_ssa))
