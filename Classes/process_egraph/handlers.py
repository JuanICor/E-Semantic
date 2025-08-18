"""
Command classes for the egraph processor
"""

from abc import ABC, abstractmethod
from typing import Any, cast

from egglog import Expr
from schema import Schema, Or
from typing_extensions import override

from Classes.process_egraph.processor import EgraphProcessor
from Classes.egraph_elements import Instruction


class GraphElementHandlers(ABC):

    def __init__(self, processor: EgraphProcessor) -> None:
        self._processor = processor
        self._extension = ""

    def _generate_unique_id(self, register: str | int) -> str:
        if isinstance(register, str):
            return register + "." + self._extension

        return register

    @abstractmethod
    def upload(self, data: dict[str, Any]) -> Expr:
        ...


class LoadHandler(GraphElementHandlers):

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
    def upload(self, data: dict[str, Any]) -> Expr:
        self._check_args(data)

        res_id = self._generate_unique_id(cast(str, data["ret_reg"]))
        arg_1_id = self._generate_unique_id(cast(str, data["arg_1"]))

        return self._processor.write_load_or_store(res_id, arg_1_id)


class StoreHandler(GraphElementHandlers):

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
    def upload(self, data: dict[str, Any]) -> Expr:
        self._check_args(data)

        res_id = self._generate_unique_id(cast(str, data["ret_reg"]))
        arg_1_id = self._generate_unique_id(cast(str | int, data["arg_1"]))

        return self._processor.write_load_or_store(res_id, arg_1_id)


class CallHandler(GraphElementHandlers):

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
    def upload(self, data: dict[str, Any]) -> Expr:
        self._check_args(data)

        res_id = self._generate_unique_id(cast(str, data["ret_reg"]))

        return self._processor.write_function(res_id, data["function"])


class UnaryOpsHandler(GraphElementHandlers):

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
    def upload(self, data: dict[str, Any]) -> Expr:
        self._check_args(data)

        res_id = self._generate_unique_id(cast(str, data["ret_reg"]))
        arg_1_id = self._generate_unique_id(cast(str | int, data["arg_1"]))

        return self._processor.write_unary_op(self.operation, res_id, arg_1_id)

    @abstractmethod
    def operation(self, expr: Instruction) -> Instruction:
        ...


class TruncHandler(UnaryOpsHandler):

    @override
    def operation(self, expr: Instruction) -> Instruction:
        return expr


class BinaryOpsHandler(GraphElementHandlers):

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
    def upload(self, data: dict[str, Any]) -> Expr:
        self._check_args(data)

        res_id = self._generate_unique_id(cast(str, data["ret_reg"]))
        arg_1_id = self._generate_unique_id(cast(str | int, data["arg_1"]))
        arg_2_id = self._generate_unique_id(cast(str | int, data["arg_2"]))

        return self._processor.write_binary_op(self.operation, res_id,
                                               arg_1_id, arg_2_id)

    @abstractmethod
    def operation(self, left_expr: Instruction,
                  right_expr: Instruction) -> Instruction:
        ...


class AddHandler(BinaryOpsHandler):

    @override
    def operation(self, left_expr: Instruction,
                  right_expr: Instruction) -> Instruction:
        return left_expr + right_expr


class SubHandler(BinaryOpsHandler):

    @override
    def operation(self, left_expr: Instruction,
                  right_expr: Instruction) -> Instruction:
        return left_expr - right_expr


class MultHandler(BinaryOpsHandler):

    @override
    def operation(self, left_expr, right_expr):
        return left_expr * right_expr


class GreaterThanHandler(BinaryOpsHandler):

    @override
    def operation(self, left_expr: Instruction,
                  right_expr: Instruction) -> Instruction:
        return left_expr > right_expr


class LessEqualHandler(BinaryOpsHandler):

    @override
    def operation(self, left_expr: Instruction,
                  right_expr: Instruction) -> Instruction:
        return left_expr <= right_expr


class LabelInstructionsHandler(GraphElementHandlers):

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
    def upload(self, data: dict[str, Any]) -> Expr:

        label_id = self._generate_unique_id(data["label"])

        regs_id = []

        for reg in data["instructions"]:
            regs_id.append(self._generate_unique_id(reg))

        self._processor.register_label_code(label_id, regs_id)


class BranchHandler(GraphElementHandlers):

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
    def upload(self, data: dict[str, Any]) -> Expr:
        self._check_args(data)

        condition = self._generate_unique_id(cast(str, data["ret_reg"]))
        label1_id = self._generate_unique_id(cast(str | int, data["arg_1"]))
        label2_id = self._generate_unique_id(cast(str | int, data["arg_2"]))

        self._processor.write_cond_branch(condition, label1_id, label2_id)


class TraceHandler(GraphElementHandlers):

    @override
    def upload(self, data: dict[str, Any]) -> Expr:
        ...


class FunctionHandler(GraphElementHandlers):

    @override
    def upload(self, data: dict[str, Any]) -> Expr:
        ...

class ExtractionHandler(GraphElementHandlers):

    @override
    def upload(self, instr: dict[str, Any]) -> None:
        var_id = self._generate_unique_id(cast(str, instr["extract_reg"]))

        return self._processor.extract_expression(var_id)


class NoneHandler(GraphElementHandlers):

    @override
    def upload(self, _instr: dict[str, Any]) -> None:
        None
