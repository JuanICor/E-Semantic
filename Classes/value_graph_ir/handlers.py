"""
Command classes for the egraph processor
"""

from abc import ABC, abstractmethod
from typing import Any, TypeAlias
from typing_extensions import override

from llvm_parser.types import (GlobalValues, GlobalString, GlobalStruct,
                               BinaryInstruction, ConversionInstruction,
                               CallInstruction, CompareInstruction,
                               ConditionalBranch, UnconditionalBranch,
                               ReturnInstruction)

from Classes.cfg import (MGSAInstruction, MonadicLoad, MonadicStore,
                         MonadicAlloca, GammaInstruction, MuInstruction)

from Classes.egraph_elements import (Leaf, add, sub, mul, truncate, equals,
                                     nequals, strict_less, strict_greater)

from .value_graph import ValueGraph, GlobalVariablesManager

BranchInstruction: TypeAlias = ConditionalBranch | UnconditionalBranch


class GlobalVariablesHandler(ABC):
    """Handles different types of global variables"""

    def __init__(self, manager: GlobalVariablesManager) -> None:
        self._globals_manager = manager

    @abstractmethod
    def upload(self, data: GlobalValues) -> None:
        ...


class GlobalStructHandler(GlobalVariablesHandler):
    """Handles global Struct variables"""

    @override
    def upload(self, data: GlobalStruct) -> None:
        ...


class GlobalStringHandler(GlobalVariablesHandler):
    """Handles global String variables"""

    @override
    def upload(self, data: GlobalString) -> None:
        identifier = data["string_name"]
        value = data["string_value"]

        self._globals_manager.add_global_string(identifier, value)


class ValueGraphNodesHandler(ABC):
    """Handles different instruction nodes of ValueGraph"""

    def __init__(self, value_graph: ValueGraph) -> None:
        self._value_graph = value_graph

    @abstractmethod
    def upload(self, node_data: MGSAInstruction) -> None:
        ...


class AllocHandler(ValueGraphNodesHandler):
    """Handles 'alloca' instructions"""

    @override
    def upload(self, node_data: MonadicAlloca) -> None:
        graph_node = node_data["ret_reg"]
        instruction_state = node_data["output_state"]
        input_state = node_data["input_state"]

        self._value_graph.add_alloca_instruction(graph_node, instruction_state,
                                                 input_state)


class LoadHandler(ValueGraphNodesHandler):
    """Handles 'load' instructions"""

    @override
    def upload(self, node_data: MonadicLoad) -> None:
        graph_node = node_data["ret_reg"]
        instruction_state = node_data["output_state"]
        input_register = node_data["load_reg"]
        input_state = node_data["input_state"]

        self._value_graph.add_load_instruction(graph_node, instruction_state,
                                               input_register, input_state)


class StoreHandler(ValueGraphNodesHandler):
    """Handles 'store' instructions"""

    @override
    def upload(self, node_data: MonadicStore) -> None:
        instruction_state = node_data["output_state"]
        store_target = node_data["ret_reg"]
        store_value = node_data["stored_value"]
        input_state = node_data["input_state"]

        self._value_graph.add_store_instruction(instruction_state,
                                                store_target, store_value,
                                                input_state)


class CallHandler(ValueGraphNodesHandler):
    """Handles 'call' instructions"""

    @override
    def upload(self, node_data: CallInstruction) -> None:
        function = node_data["function"]
        arguments = node_data["arguments"]
        node = node_data.get("ret_reg", None)

        self._value_graph.add_call(node, function, arguments)


class ConversionOpsHandler(ValueGraphNodesHandler):
    """Handles Conversion instructions"""

    @override
    def upload(self, node_data: ConversionInstruction) -> None:
        node = node_data["ret_reg"]
        argument = node_data["arg"]

        self._value_graph.add_conversion_instruction(node, self.operation,
                                                     argument)

    @abstractmethod
    def operation(self, expr: Leaf) -> Leaf:
        ...


class TruncHandler(ConversionOpsHandler):
    """Handles the 'trunc' operator"""

    @override
    def operation(self, expr: Leaf) -> Leaf:
        return truncate(expr)


class BinaryOpsHandler(ValueGraphNodesHandler):
    """Generic class for binary instructions"""

    @override
    def upload(self, node_data: BinaryInstruction) -> None:
        node = node_data["ret_reg"]
        left_arg = node_data["arg_1"]
        right_arg = node_data["arg_2"]

        self._value_graph.add_binary_op(node, self.operation, left_arg,
                                        right_arg)

    @abstractmethod
    def operation(self, left_expr: Leaf, right_expr: Leaf) -> Leaf:
        ...


class AddHandler(BinaryOpsHandler):
    """Handles the 'add' operator"""

    @override
    def operation(self, left_expr: Leaf, right_expr: Leaf) -> Leaf:
        return add(left_expr, right_expr)


class SubHandler(BinaryOpsHandler):
    """Handles the 'sub' operator"""

    @override
    def operation(self, left_expr: Leaf, right_expr: Leaf) -> Leaf:
        return sub(left_expr, right_expr)


class MultHandler(BinaryOpsHandler):
    """Handles the 'mul' operator"""

    @override
    def operation(self, left_expr: Leaf, right_expr: Leaf) -> Leaf:
        return mul(left_expr, right_expr)


class CompareHandler(ValueGraphNodesHandler):
    """Handles 'icmp' instructions"""

    operations = {
        'eq': equals,
        'ne': nequals,
        'slt': strict_less,
        'sgt': strict_greater,
    }

    @override
    def upload(self, node_data: CompareInstruction) -> None:
        node = node_data["ret_reg"]
        comparison = self.operations[node_data["comp_op"]]
        arg_1 = node_data["arg_1"]
        arg_2 = node_data["arg_2"]

        self._value_graph.add_comparison(node, comparison, arg_1, arg_2)


class BranchHandler(ValueGraphNodesHandler):
    """Handles branch instructions"""

    @override
    def upload(self, _node_data: BranchInstruction) -> None:
        pass


class GammaHandler(ValueGraphNodesHandler):
    """Handles 'gamma' instructions"""

    @override
    def upload(self, node_data: GammaInstruction) -> None:
        node = node_data["ret_reg"]
        condition = node_data["condition"]
        true_node = node_data["true_value"]
        false_node = node_data["false_value"]

        self._value_graph.add_gamma_node(node, condition, true_node,
                                         false_node)


class MuHandler(ValueGraphNodesHandler):
    """Handles 'mu' instructions"""

    @override
    def upload(self, node_data: MuInstruction):
        node = node_data["ret_reg"]
        init_value = node_data["initial_value"]
        iter_value = node_data["loop_value"]

        self._value_graph.add_mu_node(node, init_value, iter_value)


class ReturnHandler(ValueGraphNodesHandler):
    """Handles 'return' instructions"""

    @override
    def upload(self, _node_data: ReturnInstruction) -> None:
        pass


class NoneHandler(ValueGraphNodesHandler):
    """Default Handler, does nothing"""

    @override
    def upload(self, _node_data: dict[str, Any]) -> None:
        ...
