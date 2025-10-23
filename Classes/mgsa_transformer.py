from itertools import count
from typing import cast, TypedDict, TypeAlias
from llvm_parser.types import (PhiInstruction, ConditionalBranch,
                               AllocaInstruction, LoadInstruction,
                               StoreInstruction)

from Classes.graphs import (Label, CFG, BasicBlock, Instruction, GammaInstruction,
                         MuInstruction, EtaInstruction, MonadicAlloca,
                         MonadicLoad, MonadicStore, MGSAInstruction)

AssemblyInstruction: TypeAlias = AllocaInstruction | LoadInstruction | StoreInstruction


class AssemblyInstructionsData(TypedDict):
    """
    Information about assembly like instructions,
    like load and store.
    """
    block: Label
    index: int
    instruction: Instruction[AssemblyInstruction]


class PhiData(TypedDict):
    """
    Data about a single PHI node
    """
    block: Label
    index: int
    return_reg: str
    incoming_values: list[tuple[str, str]]


class MGSATransformer:
    """
    Converts a graph in SSA for to GSA by replacing Phi Instructions for Gamma and Mu Instructions.
    Also creates Eta Instructions were it corresponds.
    """

    def __init__(self, cfg: CFG) -> None:
        self.cfg = cfg
        self._loops = cfg.loops()
        self._idoms = cfg.immediate_dominators()

    def transform(self) -> None:

        assembly_nodes, phi_nodes = self._get_nodes_to_modify()

        self._transform_to_monadic_form(assembly_nodes)

        self._transform_phi_nodes(phi_nodes)

        self._place_eta_nodes()

    def _get_nodes_to_modify(
            self) -> tuple[list[AssemblyInstructionsData], list[PhiData]]:

        assembly_instr: list[AssemblyInstructionsData] = []
        phi_instr: list[PhiData] = []

        for block in self.cfg.blocks():
            for idx, instr in enumerate(block.instructions):

                if instr.opcode == 'phi':
                    phi_instr.append(
                        self._create_phi_data(block, idx,
                                              cast(PhiInstruction, instr)))

                elif instr.opcode in ['alloca', 'load', 'store']:
                    assembly_instr.append(
                        self._create_assembly_data(
                            block, idx, cast(AssemblyInstruction, instr)))

        return assembly_instr, phi_instr

    @staticmethod
    def _create_phi_data(block: BasicBlock, instruction_index: int,
                         phi_instruction: PhiInstruction) -> PhiData:
        return PhiData(block=block.label,
                       index=instruction_index,
                       return_reg=phi_instruction['ret_reg'],
                       incoming_values=list(
                           map(lambda x: tuple(x.values()),
                               phi_instruction['incoming'])))

    @staticmethod
    def _create_assembly_data(
            block: BasicBlock, instruction_index: int,
            assembly_instruction: AssemblyInstruction
    ) -> AssemblyInstructionsData:
        return AssemblyInstructionsData(block=block.label,
                                        index=instruction_index,
                                        instruction=assembly_instruction)

    def _transform_to_monadic_form(
            self, nodes: list[AssemblyInstructionsData]) -> None:
        state_counter = count()

        def new_state() -> str:
            return f"s{next(state_counter)}"

        curr_state = new_state()

        for node in nodes:
            instruction = node['instruction']
            next_state = new_state()

            new_instruction = self._create_instruction({
                **(instruction.to_dict()), 'input_state':
                curr_state,
                'output_state':
                next_state
            })

            block = self.cfg.get_block(node['block'])
            block.replace_instruction(node['index'], new_instruction)
            curr_state = next_state

    def _transform_phi_nodes(self, phi_nodes: list[PhiData]) -> None:

        loop_entries = {x.entry for x in self._loops}

        for phi_node in phi_nodes:
            if phi_node['block'] in loop_entries:

                init_value, loop_value = self._get_mu_values(
                    phi_node['block'], phi_node['incoming_values'])
                new_instruction = self._create_instruction({
                    'opcode': 'mu',
                    'ret_reg': phi_node['return_reg'],
                    'initial_value': init_value,
                    'loop_value': loop_value,
                })

            else:
                branch_instr = self._get_gamma_condition(phi_node['block'])
                true_value, false_value = self._get_gamma_values(
                    [branch_instr['if_true'], branch_instr['if_false']],
                    phi_node['incoming_values'])

                new_instruction = self._create_instruction({
                    'opcode': 'gamma',
                    'ret_reg': phi_node['return_reg'],
                    'condition': branch_instr['condition'],
                    'true_value': true_value,
                    'false_value': false_value,
                })

            block = self.cfg.get_block(phi_node['block'])
            block.replace_instruction(phi_node['index'], new_instruction)

    def _get_mu_values(
            self, block: Label,
            incoming_values: list[tuple[str, str]]) -> tuple[str, str]:
        init_value: str
        loop_value: str
        loop_nodes = next(filter(lambda x: x.entry == block,
                                 self._loops)).loop_nodes

        for val, pred_block in incoming_values:
            if pred_block not in loop_nodes:
                init_value = val
            else:
                loop_value = val

        return init_value, loop_value

    def _get_gamma_condition(self, block: Label) -> ConditionalBranch:
        # Using immediate dominators may fail in some cases
        # may need to change to use the CDG or branch scanning
        controller = self.cfg.get_block(self._idoms[block])
        branch_instr = controller.get_branch_instruction()

        if branch_instr is None or 'condition' not in branch_instr:
            raise ValueError(f"No branch instruction found for {block}")

        return branch_instr

    @staticmethod
    def _get_gamma_values(
            branches: list[str],
            incoming_values: list[tuple[str, str]]) -> tuple[str, str]:
        """
        Retrieve the true and false values for a Gamma instruction
        based on the incoming values and the branches.
        """
        true_block, false_block = branches
        lookup_dict = {
            pred_block: value
            for value, pred_block in incoming_values
        }

        return (lookup_dict[true_block], lookup_dict[false_block])

    def _place_eta_nodes(self) -> None:

        for entry, cond, nodes in self._loops:
            entry_block = self.cfg.get_block(entry)

            exit_block = self._get_loop_exit_block(nodes)

            if not exit_block:
                raise ValueError("No exit label found for loop entry {entry}")

            mu_regs = self._get_mu_return_registers(entry_block)

            self._insert_eta_instructions(exit_block, mu_regs, cond)

    def _get_loop_exit_block(self, loop_blocks: set[Label]) -> set[BasicBlock]:
        exits: set[BasicBlock] = set()

        def labels_to_blocks(labels: set[Label]):
            return map(self.cfg.get_block, labels)

        for block in labels_to_blocks(loop_blocks):
            exits.update(
                labels_to_blocks(
                    filter(lambda succ: succ not in loop_blocks, block.succs)))

        return exits

    @staticmethod
    def _get_mu_return_registers(block: BasicBlock) -> list[str]:
        mu_indexes = block.get_instructions_indexes('mu')
        return [block.instructions[idx]['ret_reg'] for idx in mu_indexes]

    @staticmethod
    def _insert_eta_instructions(blocks: set[BasicBlock], mu_registers: list[str],
                                 condition: str) -> None:
        for block in blocks:
            for reg in mu_registers:
                instr_to_change = block.get_instructions_with_reg(reg)
                eta_reg = f"{reg}_eta"

                if instr_to_change:
                    eta_instruction = MGSATransformer._create_instruction({
                        'opcode': 'eta',
                        'ret_reg': eta_reg,
                        'condition': condition,
                        'value': reg,
                    })
                    block.instructions.insert(0, eta_instruction)

                    for instr in instr_to_change:
                        instr.replace_register(reg, eta_reg)

    @staticmethod
    def _create_instruction(
            instruction_data: dict[str, str]) -> Instruction[MGSAInstruction]:
        instructions: dict[str, type[MGSAInstruction]] = {
            'gamma': GammaInstruction,
            'mu': MuInstruction,
            'eta': EtaInstruction,
            'alloca': MonadicAlloca,
            'load': MonadicLoad,
            'store': MonadicStore
        }

        cls = instructions.get(instruction_data['opcode'])

        if not cls:
            raise ValueError(
                f"Unknown instruction opcode: {instruction_data['opcode']}")

        return Instruction(cls(**instruction_data))


if __name__ == "__main__":
    # Load complex.json and run transform_to_gsa
    import json

    with open('complex.json', 'r', encoding='utf-8') as f:
        test_data = json.load(f)

    # Get the first function from the loaded data
    function_data = test_data['functions'][0]

    # Create CFG from the function data
    cfg_test = CFG(function_data)

    # Transform the CFG to GSA form
    transformer = MGSATransformer(cfg_test)
    transformer.transform()

    print(f"Transformed CFG for function: {cfg_test.name}")
    for block_test in cfg_test.blocks():
        print(f"Block {block_test.label}:")
        print("Instructions: ")
        # Print instructions, with format: \t* {instruction}
        for test_instruction in block_test.instructions:
            print(f"\t* {test_instruction}")
        print("-" * 50)
