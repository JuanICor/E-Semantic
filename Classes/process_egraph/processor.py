"""
Resolver class for the egraph process
"""
from collections.abc import Callable
from typing import TypeAlias
from egglog import EGraph, Ruleset
from egglog.builtins import Vec, Set

from Classes.egraph_elements import (Instruction, Operand, Trace, State,
                                     Function, eval_instructions)

UnaryOperation: TypeAlias = Callable[[Operand], Operand]
BinaryOperation: TypeAlias = Callable[[Operand, Operand], Operand]


class EgraphProcessor:

    def __init__(self, ruleset: Ruleset) -> None:
        self.egraph = EGraph()
        self._ruleset = ruleset
        self._egraph_id: int = 0

    def _generate_egraph_id(self) -> str:
        id = str(self._egraph_id)
        self._egraph_id += 1

        return id

    def _saturate_graph(self) -> None:
        self.egraph.run(self._ruleset.saturate())

    def _get_operand_expression(expr: str | int | bool) -> Operand:

        if isinstance(expr, int): return Operand.integer(expr)

        if isinstance(expr, bool): return Operand.boolean(expr)

        return Operand(expr)

    def write_unary_op(self, operation: UnaryOperation, res_reg: str,
                       expr: str | int) -> Instruction:

        operand_expr = self._get_operand_expression(expr)

        return self.egraph.let(self._generate_egraph_id(),
                               Instruction(res_reg, operation(operand_expr)))

    def write_binary_op(self, operation: BinaryOperation, res_reg: str,
                        arg1: str | int, arg2: str | int) -> Instruction:

        operand_arg1 = self._get_operand_expression(arg1)
        operand_arg2 = self._get_operand_expression(arg2)

        return self.egraph.let(
            self._generate_egraph_id(),
            Instruction(res_reg, operation(operand_arg1, operand_arg2)))

    def write_trace(self, trace: list[Instruction]) -> Trace:
        instruction_trace = self.egraph.let(self._generate_egraph_id(),
                                            Vec(*trace))
        trace_state = self.egraph.let(
            self._generate_egraph_id(),
            eval_instructions(instruction_trace, State.empty(), 0))

        return self.egraph.let(self._generate_egraph_id(),
                               Trace(instruction_trace, trace_state))

    def write_function(self, func_name: str, traces: list[Trace]) -> Function:
        return self.egraph.let(self._generate_egraph_id(),
                               Function(func_name, Set(*traces)))

    # def write_load_or_store(self, res_reg: str, temp_reg: str | int) -> None:
    #     return self.egraph.let(self._generate_egraph_id(), Instruction(res_reg, temp_reg))

    # def write_function(self, res_reg: str, function_name: str) -> None:
    #     self._regs_mapping[res_reg] = self.egraph.let(
    #         self._generate_egraph_id(), SSA.function(function_name))

    # def register_expression(self) -> None:
    #     ...

    # def register_blocks(self, block_label: str) -> None:
    #     self._regs_mapping[block_label] = self.egraph.let(
    #         self._generate_egraph_id(),
    #         SSA.label(block_label[:block_label.find('.')] + '_' +
    #                   block_label[block_label.rfind('/') + 1:]))

    def extract_expression(self, expr_id: str) -> str:
        expr_ssa = self._regs_mapping[expr_id]

        self._saturate_graph()

        return str(self.egraph.extract(expr_ssa))
