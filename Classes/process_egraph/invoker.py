"""
Invoker class for the egraph process
"""
from typing import TypeAlias

from llvm_parser import ParseResult

from Classes.process_egraph.handlers import InstructionHandlers, NoneHandler
from Classes.process_egraph.processor import EgraphProcessor

HandlerList: TypeAlias = list[tuple[str, InstructionHandlers]]
HandlerDict: TypeAlias = dict[str, InstructionHandlers]

class HandlerInvoker:
    var_mapping: dict[str, str]
    _handlers: HandlerDict

    def __init__(self) -> None:
        self.var_mapping = {}
        self._handlers = {}

    def register_handler(self, handler_id: str, handler: InstructionHandlers) -> None:
        self._handlers[handler_id] = handler

    def register_handler_list(self, handler_list: HandlerList) -> None:
        self._handlers = dict(handler_list)

    def set_variables_mapping(self, var_map: dict[str, str]) -> None:
        self.var_mapping = var_map

    def set_handlers_extension(self, extension: str) -> None:
        for handler in self._handlers.values():
            handler.set_extension(extension)

    def set_handlers_processor(self, processor: EgraphProcessor) -> None:
        for handler in self._handlers.values():
            handler.set_processor(processor)

    def upload_instruction_data(self, instruction_data: ParseResult) -> None:
        opcode, instr_value = next(iter(instruction_data.items()))
        handler = self._handlers.get(opcode, NoneHandler())

        handler.execute(instr_value)

    def upload_block_instrs(self, label: str, instrs: list[str]) -> None:
        handler = self._handlers["label_block"]

        handler.execute({"label": label, "instructions": instrs})

    def upload_blocks(self, labels: list[str]) -> None:
        handler = self._handlers["labels"]

        for label in labels:
            handler.execute({"label": label})

    def get_variable_value(self, variable: str) -> list[str]:
        register = self.var_mapping[variable]
        return self._handlers["extract"].execute({"extract_reg": register})
