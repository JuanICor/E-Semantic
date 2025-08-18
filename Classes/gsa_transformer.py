from typing import cast, TypedDict

from Classes.cfg import (CFG, BasicBlock, CDG, Instruction, GammaInstruction,
                         MuInstruction, EtaInstruction)
from llvm_parser.types import PhiInstruction


class PhiData(TypedDict):
    index: int
    return_reg: str
    incoming_values: list[tuple[str, str]]


class GSATransformer:

    def transform_to_gsa(self, cfg: CFG) -> None:
        cdg = cfg.control_dependency_graph()
        loops = dict(cfg.get_loops())

        for block in cfg.blocks():
            phi_data = self._get_phi_node_data(block)

            if not phi_data:
                continue

            self._place_gamma_or_mu_node(block, phi_data, cdg, loops)

    @staticmethod
    def _get_phi_node_data(block: BasicBlock) -> list[PhiData]:
        data: list[PhiData] = []
        for idx in block.phi_instructions_indexes():
            phi_instruction = cast(PhiInstruction, block.instructions[idx])
            incoming_values = phi_instruction['incoming']

            data.append(
                PhiData(index=idx,
                        return_reg=phi_instruction['reg'],
                        incoming_values=[
                            (value, label) for value, label in map(
                                lambda x: x.values(), incoming_values)
                        ]))

        return data

    def _place_gamma_or_mu_node(self, block: BasicBlock, data: list[PhiData],
                                cdg: CDG, loops: dict[str, set[str]]) -> None:
        for phi_node in data:
            if block.label in loops:
                new_instruction = self._create_mu_instruction(
                    phi_node['return_reg'], phi_node['incoming_values'],
                    loops[block.label])
            else:
                new_instruction = self._create_gamma_instruction()

            block.replace_instruction(phi_node['index'], new_instruction)

    @staticmethod
    def _create_mu_instruction(
            ret_reg: str, incoming: list[tuple[str, str]],
            loop_nodes: set[str]) -> Instruction[MuInstruction]:
        init_value: str
        loop_value: str

        for val, pred_block in incoming:
            if pred_block in loop_nodes:
                loop_nodes = val
            else:
                init_value = val

        return Instruction(
            MuInstruction(opcode="mu",
                          ret_reg=ret_reg,
                          initial_value=init_value,
                          loop_value=loop_value))

    @staticmethod
    def _create_gamma_instruction() -> Instruction[GammaInstruction]:
        ...
