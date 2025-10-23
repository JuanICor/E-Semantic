from collections import defaultdict
from collections.abc import Iterable
from typing import Any, Final, Generic, NamedTuple, TypeAlias, TypeVar, cast

import rustworkx as rx
from llvm_parser.types import (
    AllocaInstruction,
    CFGBlock,
    CFGFunction,
    ConditionalBranch,
    LoadInstruction,
    StoreInstruction,
    UnconditionalBranch,
)
from llvm_parser.types import BaseInstruction as BaseLLVMInstruction
from llvm_parser.types import Instructions as LLVMInstruction

Label: TypeAlias = str
GraphIndex: TypeAlias = int
Cdg: TypeAlias = dict[Label, list[Label]]
BranchInstruction: TypeAlias = ConditionalBranch | UnconditionalBranch
DominatorsCache: TypeAlias = dict[tuple[GraphIndex, GraphIndex], bool]

InstructionT = TypeVar('InstructionT', bound=BaseLLVMInstruction)


class GammaInstruction(BaseLLVMInstruction):
    """
    Gamma Node for SSA Translation
    """

    ret_reg: str
    condition: str
    true_value: str
    false_value: str


class MuInstruction(BaseLLVMInstruction):
    """
    Mu Node for SSA Translation
    """
    ret_reg: str
    initial_value: str
    loop_value: str


class EtaInstruction(BaseLLVMInstruction):
    """
    Eta Node for SSA Translation
    """
    ret_reg: str
    condition: str
    value: str


class MonadicAlloca(AllocaInstruction):
    """
    Monadic Alloca Node
    """
    input_state: str
    output_state: str


class MonadicLoad(LoadInstruction):
    """
    Monadic Load Node
    """
    input_state: str
    output_state: str


class MonadicStore(StoreInstruction):
    """
    Monadic Store Node
    """
    input_state: str
    output_state: str


MGSAInstruction: TypeAlias = (LLVMInstruction | GammaInstruction
                              | MuInstruction | EtaInstruction | MonadicAlloca
                              | MonadicLoad | MonadicStore)


class LoopInfo(NamedTuple):
    """Information about a Loop in the CFG"""
    entry: Label
    condition: str
    loop_nodes: set[Label]


class _BackEdge(NamedTuple):
    """A loops BackEdge"""
    head: GraphIndex
    tail: GraphIndex


class DominatorsChecker:
    """Check Dominance relationship for a given Graph"""

    def __init__(self, graph: rx.PyDiGraph["BasicBlock", None]):
        self.entry_node: Final = 0
        self.idoms: Final = rx.immediate_dominators(graph, 0)
        self._dom_cache: DominatorsCache = {}

    def dominates(self, dom: GraphIndex, node: GraphIndex) -> bool:
        key = (dom, node)

        if key in self._dom_cache:
            return self._dom_cache[key]

        result = self._compute_dominance(dom, node)
        self._dom_cache[key] = result
        return result

    def _compute_dominance(self, dom: GraphIndex, node: GraphIndex) -> bool:
        """Helper method to compute dominance relationship"""
        curr = node

        while curr != self.entry_node:
            if curr == dom:
                return True

            cached_key = (dom, curr)
            if cached_key in self._dom_cache:
                return self._dom_cache[cached_key]

            curr = self.idoms[curr]

        return dom == self.entry_node


class Instruction(Generic[InstructionT]):
    """
    Instructions of a Basic Block
    """

    def __init__(self, meta: InstructionT) -> None:
        self._data = meta

    @property
    def opcode(self) -> str:
        return self._data['opcode']

    def __getitem__(self, key: str) -> Any:
        return self._data[key]  # type: ignore

    def __contains__(self, key: str) -> bool:
        return key in self._data

    def __repr__(self) -> str:
        rep: str = "Instruction( "

        for field, value in self._data.items():
            rep = rep + f"{field}: {value} "

        return rep + ")"

    def get(self, key: str, default: Any = None) -> Any:
        return self._data.get(key, default)

    def has_register(self, register: str) -> bool:
        return register in self._data.values()

    def replace_register(self, old_register: str, new_register: str) -> None:
        for key, value in self._data.items():
            if value == old_register:
                self._data[key] = new_register

    def to_dict(self) -> InstructionT:
        return self._data


class BasicBlock:
    """
    Basic Block of a Control Flow Graph (CFG)
    """

    def __init__(self, label: str, predecessors: list[str],
                 successors: list[str]) -> None:
        self.label = label
        self.preds = predecessors
        self.succs = successors
        self.instructions: list[Instruction[MGSAInstruction]] = []

    def add_instructions(self, instructions: list[LLVMInstruction]) -> None:
        for instr_data in instructions:
            self.instructions.append(Instruction(instr_data))

    def get_instructions_indexes(self, opcode: str) -> list[int]:
        indexes = []

        for idx, instruction in enumerate(self.instructions):
            if instruction.opcode == opcode:
                indexes.append(idx)

        return indexes

    def get_branch_instruction(self) -> BranchInstruction | None:
        """Returns the block branch instruction"""
        for instr in self.instructions[::-1]:
            if instr.opcode == "br":
                return cast(BranchInstruction, instr)

        return None

    def get_instructions_with_reg(
            self, register: str) -> list[Instruction[MGSAInstruction]]:
        instructions = []

        for instruction in self.instructions:
            if instruction.has_register(register):
                instructions.append(instruction)

        return instructions

    def declared_registers(self) -> list[str]:
        registers = []

        for instruction in self.instructions:
            return_register = instruction.get("ret_reg")

            if return_register:
                registers.append(return_register)

        return registers

    def replace_instruction(self, index: int,
                            instruction: Instruction[MGSAInstruction]) -> None:
        self.instructions[index] = instruction

    def __repr__(self) -> str:
        return f"Block({self.label}, instrs={len(self.instructions)})"


class CFG:
    """
    Provides all necessary methods to manipulate the Control Flow Graph of a Function
    """

    def __init__(self, function: CFGFunction):
        self.name = function['name']
        self.parameters = function['params']
        self.ret_type = function['ret_type']
        self.is_declaration = not function.get('blocks')
        self._entry_blocks: list[GraphIndex] = []
        self._exit_blocks: list[GraphIndex] = []

        self._graph: rx.PyDiGraph[BasicBlock,
                                  None] = rx.PyDiGraph(multigraph=False)
        self._block_to_index: dict[Label, GraphIndex] = {}
        self._index_of_block: dict[GraphIndex, Label] = {}

        if function["blocks"]:
            self._build_graph(function['blocks'])

    def _build_graph(self, blocks: CFGBlock) -> None:
        """Internal method to build the CFG from a CFGBlock dict."""
        blocks_items = blocks.items()

        for name, block_data in blocks_items:
            bb = BasicBlock(name,
                            predecessors=block_data["preds"],
                            successors=block_data["succ"])
            bb.add_instructions(block_data["instructions"])

            idx = self._graph.add_node(bb)
            self._block_to_index[name] = idx
            self._index_of_block[idx] = name

            if not bb.preds:
                self._entry_blocks.append(idx)
            if not bb.succs:
                self._exit_blocks.append(idx)

        for name, block_data in blocks_items:
            src_idx = self._block_to_index[name]
            for succ in block_data["succ"]:
                self._graph.add_edge(src_idx, self._block_to_index[succ], None)

    @property
    def is_closed(self) -> bool:
        return len(self._entry_blocks) == 1 and len(self._exit_blocks) == 1

    def get_block(self, label: Label) -> BasicBlock:
        """Returns the BasicBlock corresponding with the given label"""
        return self._graph[self._block_to_index[label]]

    def blocks(self) -> Iterable[BasicBlock]:
        """Iterator over all basic blocks in the CFG"""
        yield from self._graph.nodes()

    def immediate_dominators(self) -> dict[Label, Label]:
        """Calculate the immediate dominators of the CFG"""
        if self._graph.num_nodes() < 2:
            return {}

        idoms = rx.immediate_dominators(self._graph, 0)

        return {
            self._index_of_block[node]: self._index_of_block[dom]
            for node, dom in idoms.items()
        }

    def control_dependency_graph(self) -> Cdg:
        """Calculate the Control Dependence Graph (CDG)"""
        postdom_frontier = self._postdominator_frontier()
        cdg: Cdg = defaultdict(list)

        for controlled, controllers in postdom_frontier.items():
            for controller in controllers:
                cdg[self._index_of_block[controller]].append(
                    self._index_of_block[controlled])

        return cdg

    def _postdominator_frontier(self) -> dict[GraphIndex, set[GraphIndex]]:
        """Computes the postdominator frontier of the graph"""
        reverse_graph = self._graph.copy()
        reverse_graph.reverse()

        return rx.dominance_frontiers(reverse_graph,
                                      self._graph.num_nodes() - 1)

    def strongly_conected_components(self) -> list[list[BasicBlock]]:
        sccs = rx.strongly_connected_components(self._graph)

        return [list(map(self._index_of_block, scc)) for scc in sccs]

    def loops(self) -> list[LoopInfo]:
        """Get Natural Loops information in the CFG"""
        dom_checker = DominatorsChecker(self._graph)
        loops: list[LoopInfo] = []
        is_back_edge = dom_checker.dominates

        for head, tail in self._graph.edge_list():
            if is_back_edge(tail, head):
                loops.append(
                    LoopInfo(entry=self._index_of_block[tail],
                             condition=self._get_loop_condition(
                                 _BackEdge(head, tail)),
                             loop_nodes=self._get_nodes_in_loop(tail, head)))

        return loops

    def _get_loop_condition(self, back_edge: _BackEdge) -> str:

        def is_conditional_branch(
                instruction: BranchInstruction | None) -> bool:
            return instruction is not None and 'condition' in instruction

        head_block = self._graph[back_edge.head]
        tail_block = self._graph[back_edge.tail]

        head_condition = head_block.get_branch_instruction()

        if is_conditional_branch(head_condition):
            return head_condition['condition']  # type: ignore

        tail_condition = tail_block.get_branch_instruction()

        if is_conditional_branch(tail_condition):
            return tail_condition['condition']  # type: ignore

        raise ValueError(
            f"Found loop back-edge withoout defined condition.\n{back_edge}")

    def _get_nodes_in_loop(self, header: GraphIndex,
                           tail: GraphIndex) -> set[Label]:
        loop_nodes = {header, tail}
        stack = [tail]

        while stack:
            node = stack.pop()
            for pred in self._graph.predecessor_indices(node):
                if pred not in loop_nodes:
                    loop_nodes.add(pred)
                    stack.append(pred)

        return {self._index_of_block[node] for node in loop_nodes}

    def to_dot(self) -> str:
        """
        Generate DOT representation of the CFG with actual block names
        """

        def node_attr(node: BasicBlock) -> dict[str, str]:
            safe_label = node.label.replace('%', '\\%')
            return {'label': safe_label, 'shape': 'circle'}

        return self._graph.to_dot(
            node_attr=node_attr,
            edge_attr=None,
            graph_attr={'rankdir': 'TB'}  # Top to Bottom layout
        )


if __name__ == "__main__":
    #Load complex and get the loop info from it
    import json

    with open('complex.json', 'r', encoding='utf-8') as f:
        data = json.load(f)

    # Get the first function from the loaded data
    function_data = data['functions'][0]

    # Create CFG from the function datatail
    cfg = CFG(function_data)

    print(f"Loops: {cfg.loops()}")
