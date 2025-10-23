import json

from collections import defaultdict
from collections.abc import Callable
from typing import TypeAlias
from Classes.egraph_elements import Function, Leaf, call, alloca, load, store, gamma

ConversionOp: TypeAlias = Callable[[Leaf], Leaf]
BinaryOp: TypeAlias = Callable[[Leaf, Leaf], Leaf]
ComparisonOp: TypeAlias = Callable[[Leaf, Leaf], Leaf]


class GlobalVariablesManager:
    """Manages global variables shared across all functions"""

    def __init__(self) -> None:
        self._global_vars: dict[str, Leaf] = {}

    def add_global_string(self, variable: str, value: str) -> None:
        self._global_vars[variable] = Leaf.string(value)

    def get_global_variable(self, variable: str) -> Leaf:
        """Get a global variable value"""
        return self._global_vars[variable]

    def has_global_variable(self, variable: str) -> bool:
        """Check if global variable exists"""
        return variable in self._global_vars


class ValueGraph:
    """Custom Intermediate Graph for the function's Egraph construction"""

    def __init__(self, global_vars_manager: GlobalVariablesManager) -> None:
        self._nodes_mapping: dict[str, Leaf] = {}
        self._states_mapping: dict[str, Leaf] = {}
        self._nodes_in_degree = defaultdict(int)
        self._global_manager = global_vars_manager

    def _add_node(self, node: str, value: Leaf) -> None:
        if node not in self._nodes_mapping:
            self._nodes_mapping[node] = value

    def _get_argument_value(self, argument: str | int) -> Leaf:
        if isinstance(argument, str):
            if argument in self._nodes_mapping:
                self._nodes_in_degree[argument] += 1
                return self._nodes_mapping[argument]

            if self._global_manager.has_global_variable(argument):
                return self._global_manager.get_global_variable(argument)

            raise ValueGraphException(
                f"{argument} does not exists in Value Graph")

        return Leaf.int(argument)

    def _get_state_value(self, state: str) -> Leaf:
        if state in self._states_mapping:
            return self._states_mapping[state]

        if state != "s0":
            raise ValueGraphException(
                f"{state} does not exists in Value Graph")

        return Leaf.state(state)

    def add_parameter(self, parameter: str) -> None:
        """Add a parameter to the value graph"""
        parameter_value = Leaf.param(parameter)
        self._add_node(parameter, parameter_value)


    def add_alloca_instruction(self, node: str, state: str,
                               input_state: str) -> None:
        """Add an alloca instruction to the value graph"""
        input_state_value = self._get_state_value(input_state)
        alloca_result = alloca(input_state_value)

        self._add_node(node, alloca_result)
        self._states_mapping[state] = alloca_result

    def add_load_instruction(self, node: str, state: str, load_register: str,
                             input_state: str) -> None:
        """Add a load instruction to the value graph"""
        input_state_value = self._get_state_value(input_state)
        register_node = self._get_argument_value(load_register)
        load_result = load(register_node, input_state_value)

        self._add_node(node, load_result)
        self._states_mapping[state] = load_result

    def add_store_instruction(self, state: str, store_node: str,
                              value_node: str, input_state: str) -> None:
        """Add a store instruction to the value graph"""
        input_state_value = self._get_state_value(input_state)
        target_value = self._get_argument_value(store_node)
        store_value = self._get_argument_value(value_node)

        store_result = store(target_value, store_value, input_state_value)

        self._states_mapping[state] = store_result

    def add_conversion_instruction(self, node: str, operation: ConversionOp,
                                   arg: str) -> None:
        argument_value = self._get_argument_value(arg)

        self._add_node(node, operation(argument_value))

    def add_binary_op(self, node: str, operation: BinaryOp, arg1: str,
                      arg2: str) -> None:
        lhv = self._get_argument_value(arg1)
        rhv = self._get_argument_value(arg2)

        self._add_node(node, operation(lhv, rhv))

    def add_comparison(self, node: str, comparison: ComparisonOp, arg1: str,
                       arg2: str) -> None:
        lhv = self._get_argument_value(arg1)
        rhv = self._get_argument_value(arg2)

        self._add_node(node, comparison(lhv, rhv))

    def add_call(self, node: str | None, function: str,
                 arguments: list[str]) -> None:
        args = [self._get_argument_value(arg) for arg in arguments]
        result = call(function, args)

        if node is not None:
            self._add_node(node, result)

    def add_gamma_node(self, node: str, condition: str, true_node: str,
                       false_node: str) -> None:
        cond_value = self._get_argument_value(condition)
        true_value = self._get_argument_value(true_node)
        false_value = self._get_argument_value(false_node)

        gamma_value = gamma(cond_value, true_value, false_value)
        self._add_node(node, gamma_value)

    def _get_roots(self) -> list[Leaf]:

        is_global_var = self._global_manager.has_global_variable
        roots: list[Leaf] = []

        for node, value in self._nodes_mapping.items():
            if not is_global_var(node) and self._nodes_in_degree[node] == 0:
                roots.append(value)

        return roots

    def get_function_node(self, name: str) -> Function | None:
        """Get the function node by combining all root nodes"""
        roots = self._get_roots()

        if not roots:
            return None

        return Function(name, roots)

    def __repr__(self) -> str:
        graph_info = {
            k: {
                'value': str(v),
                'indegree': self._nodes_in_degree[k]
            }
            for k, v in self._nodes_mapping.items()
        }
        return json.dumps(graph_info, indent=2)


class ValueGraphException(Exception):
    """
    Exception to be raised on ValueGraph related errors
    """
