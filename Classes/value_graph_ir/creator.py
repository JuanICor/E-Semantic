"""
Invoker class for the egraph process
"""
from llvm_parser.types import GlobalValues
from Classes.graphs.cfg import CFG, BasicBlock

from .handlers import ParametersHandler
from .handler_factory import InstructionsHandlerFactory, GlobalsHandlerFactory
from .value_graph import ValueGraph, GlobalVariablesManager


class ValueGraphCreator:
    """
    Invoker class in Command Pattern, passes information
    to the corresponding handler for each instruction
    """

    def __init__(self, global_vars_manager: GlobalVariablesManager) -> None:
        self._gvars_manager = global_vars_manager
        self._globals_factory = GlobalsHandlerFactory(global_vars_manager)

    def process_global_variables(self, variables: list[GlobalValues]) -> None:

        for var in variables:
            if 'struct_name' in var:
                handler = self._globals_factory.get_handler("struct")
            else:
                handler = self._globals_factory.get_handler("string")

            handler.upload(var)

    def process_function(self, cfg: CFG) -> ValueGraph:
        """Process a single function and return its ValueGraph"""
        processor, instruction_factory = self._create_function_processor()

        self._process_parameters(cfg.parameters, ParametersHandler(processor))

        for basic_block in cfg.blocks():
            self._process_block(basic_block, instruction_factory)

        return processor

    def _create_function_processor(
            self) -> tuple[ValueGraph, InstructionsHandlerFactory]:
        processor = ValueGraph(self._gvars_manager)
        instructions_factory = InstructionsHandlerFactory(processor)

        return processor, instructions_factory

    def _process_parameters(self, params: list[str | list[str]],
                            handler: ParametersHandler) -> None:
        for param in params:
            handler.simple_parameter(param)

    def _process_block(self, block: BasicBlock,
                       factory: InstructionsHandlerFactory) -> None:
        for instruction in block.instructions:
            handler = factory.get_handler(instruction.opcode)
            handler.upload(instruction.to_dict())
