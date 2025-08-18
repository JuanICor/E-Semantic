"""
Invoker class for the egraph process
"""
from llvm_parser import ParseResult
from Classes.egraph_elements import Instruction, Trace

from .processor import EgraphProcessor
from .handler_factory import HandlerFactory


class HandlerInvoker:

    def __init__(self, processor: EgraphProcessor) -> None:
        self.var_mapping: dict[str, str] = {}
        self._handlers = HandlerFactory()
        self._processor = processor

    def set_variables_mapping(self, var_map: dict[str, str]) -> None:
        self.var_mapping = var_map

    def upload_instruction(self, instruction_data: ParseResult) -> Instruction:
        handler = self._handlers.get_handler(instruction_data.pop('opcode'),
                                             self._processor)

        return handler.upload(instruction_data)

    def upload_trace(self, instructions: list[Instruction]) -> Trace:
        handler = self._handlers.get_handler("trace", self._processor)

        return handler.upload({"instructions": instructions})

    def upload_function(self, function_name: str, traces: list[Trace]) -> None:
        handler = self._handlers.get_handler("function", self._processor)

        handler.upload({"name": function_name, "traces": traces})

    def get_variable_value(self, variable: str) -> list[str]:
        register = self.var_mapping[variable]
        return self._handlers["extract"].execute({"extract_reg": register})
