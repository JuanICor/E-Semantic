"""
Command classes for the egraph processor
"""

from abc import ABC, abstractmethod
from typing import Any, cast

from Classes.process_egraph.processor import EgraphProcessor
from Classes.ssa_graph import SSA
from schema import Schema, Or
from typing_extensions import override


class InstructionHandlers(ABC):

    def __init__(self) -> None:
        self._processor: EgraphProcessor
        self._extension: str

    def set_processor(self, processor: EgraphProcessor) -> None:
        self._processor = processor

    def set_extension(self, extension: str) -> None:
        self._extension = extension

    def _generate_unique_id(self, register: str | int) -> str:
        if isinstance(register, str):
            return register + "." + self._extension

        return register

    @abstractmethod
    def execute(self, instr: dict[str, Any]) -> None:
        ...


class LoadHandler(InstructionHandlers):

    @staticmethod
    def _check_args(instruction: dict[str, Any]) -> None:
        schema = Schema(
            {
                "ret_reg": str,
                "arg_1": str,
            },
            ignore_extra_keys=True,
        )

        if not schema.is_valid(instruction):
            raise ValueError("Invalid instruction passed to the load handler")

    @override
    def execute(self, instr: dict[str, Any]) -> None:
        self._check_args(instr)

        res_id = self._generate_unique_id(cast(str, instr["ret_reg"]))
        arg_1_id = self._generate_unique_id(cast(str, instr["arg_1"]))

        self._processor.write_load_or_store(res_id, arg_1_id)


class StoreHandler(InstructionHandlers):

    @staticmethod
    def _check_args(instruction: dict[str, Any]) -> None:
        schema = Schema(
            {
                "ret_reg": str,
                "arg_1": Or(str, int),
            },
            ignore_extra_keys=True,
        )

        if not schema.is_valid(instruction):
            raise ValueError(
                "Invalid instruction passed to the store handler.")

    @override
    def execute(self, instr: dict[str, Any]) -> None:
        self._check_args(instr)

        res_id = self._generate_unique_id(cast(str, instr["ret_reg"]))
        arg_1_id = self._generate_unique_id(cast(str | int, instr["arg_1"]))

        self._processor.write_load_or_store(res_id, arg_1_id)


class CallHandler(InstructionHandlers):

    @staticmethod
    def _check_args(instruction: dict[str, Any]) -> None:
        schema = Schema(
            {
                "function": str,
            },
            ignore_extra_keys=True,
        )

        if not schema.is_valid(instruction):
            raise ValueError("Invalid arguments for call handler.")

    @override
    def execute(self, instr: dict[str, Any]) -> None:
        self._check_args(instr)

        res_id = self._generate_unique_id(cast(str, instr["ret_reg"]))

        self._processor.write_function(res_id, instr["function"])


class UnaryOpsHandler(InstructionHandlers):

    def _check_args(self, instruction: dict[str, Any]) -> None:
        schema = Schema(
            {
                "ret_reg": str,
                "arg_1": Or(str, int),
            },
            ignore_extra_keys=True,
        )

        if not schema.is_valid(instruction):
            raise ValueError(
                f"Invalid instruction passed to {self.__class__.__name__}")

    @override
    def execute(self, instr: dict[str, Any]) -> None:
        self._check_args(instr)

        res_id = self._generate_unique_id(cast(str, instr["ret_reg"]))
        arg_1_id = self._generate_unique_id(cast(str | int, instr["arg_1"]))

        self._processor.write_unary_op(self.operation, res_id, arg_1_id)

    @abstractmethod
    def operation(self, expr: SSA) -> SSA:
        ...


class TruncHandler(UnaryOpsHandler):

    @override
    def operation(self, expr: SSA) -> SSA:
        return expr


class BinaryOpsHandler(InstructionHandlers):

    def _check_args(self, instruction: dict[str, Any]) -> None:
        schema = Schema(
            {
                "ret_reg": str,
                "arg_1": Or(str, int),
                "arg_2": Or(str, int),
            },
            ignore_extra_keys=True,
        )

        if not schema.is_valid(instruction):
            raise ValueError(
                f"Invalid instruction passed to {self.__class__.__name__}")

    @override
    def execute(self, instr: dict[str, Any]) -> None:
        self._check_args(instr)

        res_id = self._generate_unique_id(cast(str, instr["ret_reg"]))
        arg_1_id = self._generate_unique_id(cast(str | int, instr["arg_1"]))
        arg_2_id = self._generate_unique_id(cast(str | int, instr["arg_2"]))

        self._processor.write_binary_op(self.operation, res_id, arg_1_id,
                                        arg_2_id)

    @abstractmethod
    def operation(self, left_expr: SSA, right_expr: SSA) -> SSA:
        ...


class AddHandler(BinaryOpsHandler):

    @override
    def operation(self, left_expr: SSA, right_expr: SSA) -> SSA:
        return left_expr + right_expr


class SubHandler(BinaryOpsHandler):

    @override
    def operation(self, left_expr: SSA, right_expr: SSA) -> SSA:
        return left_expr - right_expr


class MultHandler(BinaryOpsHandler):

    @override
    def operation(self, left_expr, right_expr):
        return left_expr * right_expr


class GreaterThanHandler(BinaryOpsHandler):

    @override
    def operation(self, left_expr: SSA, right_expr: SSA) -> SSA:
        return left_expr > right_expr


class LessEqualHandler(BinaryOpsHandler):

    @override
    def operation(self, left_expr: SSA, right_expr: SSA) -> SSA:
        return left_expr <= right_expr


class LabelInstructionsHandler(InstructionHandlers):

    @staticmethod
    def _check_args(instruction: dict[str, Any]) -> None:
        schema = Schema({
            "label": str,
            "instructions": [str],
        })

        if not schema.is_valid(instruction):
            raise ValueError(
                f"Invalid instruction passed to label instruction handler")

    @override
    def execute(self, instr: dict[str, Any]) -> None:

        label_id = self._generate_unique_id(instr["label"])

        regs_id = []

        for reg in instr["instructions"]:
            regs_id.append(self._generate_unique_id(reg))

        self._processor.register_label_code(label_id, regs_id)

class BranchHandler(InstructionHandlers):

    @staticmethod
    def _check_args(instruction: dict[str, Any]) -> None:
        schema = Schema(
            {
                "ret_reg": str,
                "arg_1": Or(str, int),
                "arg_2": Or(str, int),
            },
            ignore_extra_keys=True,
        )

        if not schema.is_valid(instruction):
            raise ValueError(
                f"Invalid arguments for branch handler. {instruction}")

    @override
    def execute(self, instr: dict[str, Any]) -> None:
        self._check_args(instr)

        condition = self._generate_unique_id(cast(str, instr["ret_reg"]))
        label1_id = self._generate_unique_id(cast(str | int, instr["arg_1"]))
        label2_id = self._generate_unique_id(cast(str | int, instr["arg_2"]))

        self._processor.write_cond_branch(condition, label1_id, label2_id)


class NoneHandler(InstructionHandlers):

    @override
    def execute(self, _instr: dict[str, Any]) -> None:
        None


class LabelHandler(InstructionHandlers):

    @override
    def execute(self, instr: dict[str, Any]) -> None:
        label_id = self._generate_unique_id(cast(str, instr["label"]))

        self._processor.register_blocks(label_id)


class ExtractionHandler(InstructionHandlers):

    @override
    def execute(self, instr: dict[str, Any]) -> None:
        var_id = self._generate_unique_id(cast(str, instr["extract_reg"]))

        return self._processor.extract_expression(var_id)
