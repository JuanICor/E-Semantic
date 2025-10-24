import importlib
from abc import ABC, abstractmethod
from typing import cast, TypeAlias, Final
from typing_extensions import override

from .value_graph import ValueGraph, GlobalVariablesManager
from .handlers_config import (instructions_handlers_path,
                              global_variables_handlers_path, HandlerName)
from .handlers import ValueGraphNodesHandler, GlobalVariablesHandler

Handlers: TypeAlias = ValueGraphNodesHandler | GlobalVariablesHandler
HandlersCache: TypeAlias = dict[str, Handlers]


class HandlerFactory(ABC):
    """Handlers Factory Interface"""

    def __init__(self) -> None:
        self._instances: HandlersCache = {}
        self._handlers_module: Final = 'Classes.value_graph_ir.handlers'

    @property
    @abstractmethod
    def class_map(self) -> dict[str, HandlerName]:
        """Mapping of handler names to their respective class paths"""

    @abstractmethod
    def _create_handler(self, handler_class: type[Handlers]) -> Handlers:
        """Create a handler instance with appropriate dependencies"""

    def get_handler(self, name: str) -> Handlers:
        if name not in self.class_map:
            raise ValueError(f"No handler for '{name}'")

        if name not in self._instances:
            handler_class = self._import_handler(self.class_map[name])
            self._instances[name] = self._create_handler(handler_class)

        return self._instances[name]

    def _import_handler(self, handler_name: str) -> Handlers:
        module = importlib.import_module(self._handlers_module)
        return cast(Handlers, getattr(module, handler_name))


class GlobalsHandlerFactory(HandlerFactory):
    """Creates Global Variables Handlers dinamically"""

    def __init__(self, manager: GlobalVariablesManager):
        super().__init__()
        self.manager: Final = manager

    @property
    @override
    def class_map(self) -> dict[str, HandlerName]:
        return global_variables_handlers_path

    @override
    def _create_handler(
            self, handler_class: type[Handlers]) -> GlobalVariablesHandler:
        return cast(GlobalVariablesHandler, handler_class(self.manager))


class InstructionsHandlerFactory(HandlerFactory):
    """Creates Instruction Handlers dinamically"""

    def __init__(self, processor: ValueGraph) -> None:
        super().__init__()
        self.processor: Final = processor

    @property
    @override
    def class_map(self) -> dict[str, HandlerName]:
        return instructions_handlers_path

    @override
    def _create_handler(
            self, handler_class: type[Handlers]) -> ValueGraphNodesHandler:
        return cast(InstructionsHandlerFactory, handler_class(self.processor))
