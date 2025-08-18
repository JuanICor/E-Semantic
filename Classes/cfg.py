from collections import defaultdict
from collections.abc import Callable, Iterable
from functools import reduce
from typing import (Any, TypeAlias, NamedTuple, Generic, TypeVar, cast)
import rustworkx as rx

from llvm_parser.types import (CFGFunction, CFGBlock, BaseInstruction as
                               BaseLLVMInstruction, UnconditionalBranch,
                               ConditionalBranch, Instructions as
                               LLVMInstruction)

Label: TypeAlias = str
GraphIndex: TypeAlias = int
CDG: TypeAlias = dict[Label, list[Label]]

InstrType = TypeVar('InstrType', bound=BaseLLVMInstruction)


class GammaInstruction(BaseLLVMInstruction):
    ret_reg: str
    condition: str
    true_value: str
    false_value: str


class MuInstruction(BaseLLVMInstruction):
    ret_reg: str
    initial_value: str
    loop_value: str


class EtaInstruction(BaseLLVMInstruction):
    ret_reg: str
    condition: str
    value: str


GSAInstruction: TypeAlias = LLVMInstruction | GammaInstruction | MuInstruction | EtaInstruction


class LoopInfo(NamedTuple):
    header: Label
    loop_nodes: set[Label]


class Instruction(Generic[InstrType]):
    """
    Instructions of a Basic Block
    """

    def __init__(self, meta: InstrType) -> None:
        self._data = meta

    @property
    def opcode(self) -> str:
        return self._data['opcode']

    def __getitem__(self, key: str) -> Any:
        return self._data[key]  # type: ignore

    def __repr__(self) -> str:
        return f"Instr({self._data})"


class BasicBlock:
    """
    Basic Block of a Control Flow Graph (CFG)
    """

    def __init__(self, label: str, predecessors: list[str],
                 successors: list[str]) -> None:
        self.label = label
        self.preds = predecessors
        self.succs = successors
        self.instructions: list[Instruction[GSAInstruction]] = []

    def add_instructions(self, instructions: list[LLVMInstruction]) -> None:
        for instr_data in instructions:
            self.instructions.append(Instruction(instr_data))

    def phi_instructions_indexes(self) -> list[int]:
        indexes = []

        for idx, instruction in enumerate(self.instructions):
            if instruction.opcode == 'phi':
                indexes.append(idx)

        return indexes

    def get_branch_instruction(
            self) -> UnconditionalBranch | ConditionalBranch | None:

        for instr in self.instructions[::-1]:
            if instr.opcode == "br":
                return cast(UnconditionalBranch | ConditionalBranch, instr)

        return None

    def replace_instruction(self, index: int,
                            instruction: Instruction[GSAInstruction]) -> None:
        self.instructions[index] = instruction

    def __repr__(self) -> str:
        return f"Block({self.label}, instrs={len(self.instructions)})"


class CFG:
    """
    Provides all necessary methods to manipulate the Control Flow Graph of a Function
    """

    def __init__(self, function: CFGFunction):
        self.function_name = function['name']
        self.parameters = function['params']
        self.ret_type = function['ret_type']

        self._graph: rx.PyDiGraph[BasicBlock,
                                  None] = rx.PyDiGraph(multigraph=False)
        self._block_to_index: dict[Label, GraphIndex] = {}
        self._index_of_block: dict[GraphIndex, Label] = {}
        self._build_graph(function['blocks'])

    def _build_graph(self, blocks: CFGBlock) -> None:
        """Internal method to build the CFG from a CFGBlock dict."""
        blocks_items = blocks.items()

        for name, data in blocks_items:
            bb = BasicBlock(name,
                            predecessors=data["preds"],
                            successors=data["succ"])
            bb.add_instructions(data["instructions"])

            idx = self._graph.add_node(bb)
            self._block_to_index[name] = idx
            self._index_of_block[idx] = name

        for name, data in blocks_items:
            src_idx = self._block_to_index[name]
            for succ in data["succ"]:
                self._graph.add_edge(src_idx, self._block_to_index[succ], None)

    def blocks(self) -> Iterable[BasicBlock]:
        """Iterator over all basic blocks in the CFG"""
        for block in self._graph.nodes():
            yield block

    def control_dependency_graph(self) -> CDG:
        """Calculate the Control Dependence Graph (CDG)"""
        postdom_frontier = self._postdominator_frontier()
        cdg: CDG = defaultdict(list)

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

    def get_loops(self) -> list[LoopInfo]:
        """Find Natural Loops inside the CFG"""
        dom = self._compute_dominators()
        loops: list[LoopInfo] = []
        is_back_edge: Callable[[int, int], bool] = lambda x, y: y in dom[x]

        for head, tail in self._graph.edge_list():
            if is_back_edge(head, tail):
                loops.append(
                    LoopInfo(self._index_of_block[tail],
                             self._get_nodes_in_loop(tail, head)))

        return loops

    # TODO: Change algorithm to Lengaur-Tarjan
    def _compute_dominators(self) -> dict[GraphIndex, set[GraphIndex]]:
        dom = {0: {0}}
        all_nodes = self._graph.node_indices()

        for node in all_nodes[1:]:
            dom[node] = set(all_nodes)

        while True:
            changed = False
            for node in all_nodes[1:]:
                preds = self._graph.predecessor_indices(node)
                new_dom = {node} | reduce(set.intersection,
                                          (dom[p] for p in preds))

                if new_dom != dom[node]:
                    dom[node] = new_dom
                    changed = True

            if not changed:
                break

        return dom

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


if __name__ == "__main__":
    #Load complex and get the loop info from it
    import json

    with open('complex.json', 'r') as f:
        data = json.load(f)

    # Get the first function from the loaded data
    function_data = data['functions'][0]

    # Create CFG from the function data
    cfg = CFG(function_data)
    loops = cfg.get_loops()
