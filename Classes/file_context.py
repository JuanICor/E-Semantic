from pathlib import Path
from typing import TypeAlias

from Classes.egraph_elements import Function as EGraphNode
from Classes.value_graph_ir import (ValueGraphCreator,
                                           GlobalVariablesManager)

FunctionName: TypeAlias = str


class FileContext:
    """Manages the processing context for a single file"""

    def __init__(self, filepath: Path) -> None:
        self.file = filepath.name
        self.global_manager = GlobalVariablesManager()
        self.function_nodes: dict[FunctionName, EGraphNode] = {}
        self.graph_creator = ValueGraphCreator(self.global_manager)

    def get_function_node(self, function_name: str) -> EGraphNode | None:
        """Get a functions egraph reference"""
        return self.function_nodes.get(function_name)

    def get_all_function_names(self) -> list[FunctionName]:
        """Get all function names processed in this file"""
        return list(self.function_nodes.keys())
