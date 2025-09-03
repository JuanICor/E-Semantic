from pathlib import Path
from typing import cast, TypeAlias

from egglog import EGraph, eq
from egglog.bindings import EggSmolError

from llvm_parser import LlvmData
from llvm_parser.types import CFGFunction, GlobalValues

from Classes.egraph_elements import Leaf as EGraphNode, graph_ruleset
from Classes.process_file import FileProcessor
from Classes.file_context import FileContext
from Classes.cfg import CFG
from Classes.mgsa_transformer import MGSATransformer
from Classes.value_graph_ir import ValueGraph

FileName: TypeAlias = str


class Engine:
    """
    Class that implements the logic between modules.
    """

    def __init__(self) -> None:
        self._egraph = EGraph()
        self._egraph_ruleset = graph_ruleset
        self._file_data: dict[FileName, FileContext] = {}

    def compare_files(self, filepaths: list[str]) -> bool:
        """
        Compare functions across multiple files to check for semantic equivalence.

        Args:
            filepaths: List of file paths to compare

        Returns:
            bool: True if all files contain semantically equivalent functions
        """
        if len(filepaths) < 2:
            return True

        # Upload all files first
        for filepath_str in filepaths:
            filepath = Path(filepath_str)
            if filepath.stem not in self._file_data:
                self.upload_file(filepath)

        # Get all file contexts
        file_contexts = [self._file_data[Path(fp).stem] for fp in filepaths]

        # Find common function names across all files
        common_functions = set(file_contexts[0].get_all_function_names())
        for context in file_contexts[1:]:
            common_functions &= set(context.get_all_function_names())

        if not common_functions:
            return False

        # Saturate the egraph to enable equivalence checking
        self._saturate_egraph()

        # self._egraph.run(2, ruleset=self._egraph_ruleset)

        # Check if corresponding functions are equivalent in the egraph
        for func_name in common_functions:
            function_nodes = [
                context.get_function_node(func_name)
                for context in file_contexts
            ]

            # Check if all nodes are equivalent (same equivalence class)
            first_node = function_nodes[0]
            try:
                for node in function_nodes[1:]:
                    self._egraph.check(eq(first_node).to(node))
            except EggSmolError:
                return False

        return True

    def upload_file(self, filepath: Path) -> None:

        file_name = filepath.stem

        file_context = FileContext(filepath)
        file_data = self._get_file_data(filepath)
        prog_functions = cast(list[CFGFunction], file_data['functions'])

        file_context.graph_creator.process_global_variables(
            cast(GlobalValues, file_data['global_variables']))

        for func in prog_functions:
            function_cfg = self._convert_function_to_gsa(func)

            if not function_cfg.is_declaration:
                function_name = function_cfg.name

                function_repr = file_context.graph_creator.process_function(
                    function_cfg)
                function_node = self._upload_to_egraph(
                    function_cfg.name, function_repr,
                    file_name + '.' + function_name.replace('@', ''))

                file_context.function_nodes[function_name] = function_node

        self._file_data[file_name] = file_context

    def _get_file_data(self, filepath: Path) -> LlvmData:
        """Retrieve LLVM data for the given filepath"""
        processor = FileProcessor()
        file_data = processor.get_file_llvm_data(filepath)

        return file_data

    def _convert_function_to_gsa(self, function: CFGFunction) -> CFG:

        function_cfg = CFG(function)

        if function_cfg.is_declaration:
            return function_cfg

        transformer = MGSATransformer(function_cfg)
        transformer.transform()

        return transformer.cfg

    def _upload_to_egraph(self, function: str, egraph_repr: ValueGraph,
                          node_id: str) -> EGraphNode:

        if (func_value := egraph_repr.get_function_node(function)) is None:
            raise ValueError(f"No root value for function {function}")

        return self._egraph.let(node_id, func_value)

    def _saturate_egraph(self) -> None:
        self._egraph.run(self._egraph_ruleset.saturate())


if __name__ == "__main__":
    engine = Engine()
    FILE1 = "Examples/eqClass04/two_fors_example01.c"
    FILE2 = "Examples/eqClass04/two_fors_example02.c"

    RESULT = engine.compare_files([FILE1, FILE2])

    print("Functions are Semantically Equal!" if RESULT else
          "Could not determine if functions were semantiacally equal!")

    engine._egraph.display()
