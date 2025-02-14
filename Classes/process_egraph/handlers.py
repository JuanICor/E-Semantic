"""
Command classes for the egraph processor
"""

from abc import ABC, abstractmethod
from typing import cast, Any
from typing_extensions import override
from schema import Schema

from Classes.ssa_graph import SSA
from Classes.process_egraph.processor import EgraphProcessor


class InstructionHandlers(ABC):

    def __init__(self) -> None:
        self._processor: EgraphProcessor
        self._extension: str

    def set_processor(self, processor: EgraphProcessor) -> None:
        self._processor = processor

    def set_extension(self, extension: str) -> None:
        self._extension = extension

    def _generate_unique_id(self, register: str) -> str:
        if not register.isdigit():
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
                "res_reg": str,
                "arg1": str,
            },
            ignore_extra_keys=True,
        )

        if not schema.is_valid(instruction):
            raise ValueError("Invalid instruction passed to the load handler")

    @override
    def execute(self, instr: dict[str, Any]) -> None:
        self._check_args(instr)

        res_id = self._generate_unique_id(cast(str, instr["res_reg"]))
        arg1_id = self._generate_unique_id(cast(str, instr["arg1"]))

        self._processor.write_load_or_store(res_id, arg1_id)


class StoreHandler(InstructionHandlers):

    @staticmethod
    def _check_args(instruction: dict[str, Any]) -> None:
        schema = Schema(
            {
                "res_reg": str,
                "arg1": str,
            },
            ignore_extra_keys=True,
        )

        if not schema.is_valid(instruction):
            raise ValueError("Invalid instruction passed to the store handler")

    @override
    def execute(self, instr: dict[str, Any]) -> None:
        self._check_args(instr)

        res_id = self._generate_unique_id(cast(str, instr["res_reg"]))
        arg1_id = self._generate_unique_id(cast(str, instr["arg1"]))

        self._processor.write_load_or_store(res_id, arg1_id)


class CallHandler(InstructionHandlers):

    @staticmethod
    def _check_args(instruction: dict[str, Any]) -> None:
        schema = Schema(
            {
                "function_name": str,
            },
            ignore_extra_keys=True,
        )

        if not schema.is_valid(instruction):
            raise ValueError("Invalid arguments for call handler.")

    @override
    def execute(self, instr: dict[str, Any]) -> None:
        self._check_args(instr)

        res_id = self._generate_unique_id(cast(str, instr["res_reg"]))

        self._processor.write_function(res_id, instr["function_name"])


class BinaryOpsHandler(InstructionHandlers):

    def _check_args(self, instruction: dict[str, Any]) -> None:
        schema = Schema(
            {
                "res_reg": str,
                "arg1": str,
                "arg2": str,
            },
            ignore_extra_keys=True,
        )

        if not schema.is_valid(instruction):
            raise ValueError(
                f"Invalid instruction passed to {self.__class__.__name__}")

    @override
    def execute(self, instr: dict[str, Any]) -> None:
        self._check_args(instr)

        res_id = self._generate_unique_id(cast(str, instr["res_reg"]))
        arg1_id = self._generate_unique_id(cast(str, instr["arg1"]))
        arg2_id = self._generate_unique_id(cast(str, instr["arg2"]))

        self._processor.write_binary_op(self.operation, res_id, arg1_id,
                                        arg2_id)

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


class ExtractionHandler(InstructionHandlers):

    @override
    def execute(self, instr: dict[str, Any]) -> None:
        var_id = self._generate_unique_id(cast(str, instr["extract_reg"]))

        self._processor.extract_expression(var_id)
