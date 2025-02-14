"""
Invoker class for the egraph process
"""
from collections import defaultdict
from typing import DefaultDict

from Classes.process_file import InstrInfo
from Classes.process_egraph.handlers import InstructionHandlers
from Classes.process_egraph.processor import EgraphProcessor

class HandlerInvoker:
    var_mapping: DefaultDict[str, list[str]]
    _handlers: dict[str, InstructionHandlers]

    def __init__(self) -> None:
        self.var_mapping = defaultdict(list)
        self._handlers = {}

    def register_handler(self, handler_id: str, handler: InstructionHandlers) -> None:
        self._handlers[handler_id] = handler

    def set_variables_mapping(self, map: dict[str, str]) -> None:
        for key, value in map.items():
            self.var_mapping[key].append(value)

    def set_handlers_extension(self, extension: str) -> None:
        for handler in self._handlers.values():
            handler.set_extension(extension)

    def set_handlers_processor(self, processor: EgraphProcessor) -> None:
        for handler in self._handlers.values():
            handler.set_processor(processor)

    def upload_instruction_data(self, instruction_data: InstrInfo) -> None:
        handler = self._handlers.get(instruction_data.opcode)

        if not handler:
            raise ValueError(f"Missing Handler for {instruction_data.opcode} opcode")

        handler.execute(instruction_data._asdict())

    def display_variables_value(self, *variables: str) -> None:
        for var in variables:
            for reg in self.var_mapping[var]:
                self._handlers["extract"].execute({"extract_reg": reg})
