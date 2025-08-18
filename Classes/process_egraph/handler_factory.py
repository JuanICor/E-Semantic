import importlib
from typing import cast, TypeAlias

from .processor import EgraphProcessor
from .handlers_config import handler_class_path
from .handlers import GraphElementHandlers, NoneHandler

HandlersCache: TypeAlias = dict[str, GraphElementHandlers]


class HandlerFactory:

    def __init__(self) -> None:
        self.class_map = handler_class_path
        self._instances: HandlersCache = {}

    def get_handler(self, name: str,
                    processor: EgraphProcessor) -> GraphElementHandlers:
        if name not in self.class_map:
            return NoneHandler()
            # raise ValueError(f"No handler for '{name}'")

        if name not in self._instances:
            self._instances[name] = self._import_class(
                self.class_map[name])(processor)

        return self._instances[name]

    def _import_class(self, path: str) -> GraphElementHandlers:
        module_name, class_name = path.rsplit(".", 1)
        module = importlib.import_module(module_name)
        return cast(GraphElementHandlers, getattr(module, class_name))
