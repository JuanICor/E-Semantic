import os
import sys
from subprocess import CompletedProcess, run as Srun
from llvmlite import binding as llvm
from llvmlite.binding import ModuleRef, ValueRef

from typing import TypeAlias, Final, cast

StrPath: TypeAlias = str
FunctionName: TypeAlias = str
Instructions: TypeAlias = list[ValueRef]
Labels: TypeAlias = int

LL_PATH: Final[StrPath] = os.getcwd()


class GenerateSSA():
    file_path: Final[StrPath]

    def __init__(self, file_path: StrPath) -> None:
        self.file_path = file_path

    @staticmethod
    def _change_file_extension(file_path: StrPath, new_ext: str) -> StrPath:
        base, _ = os.path.splitext(file_path)

        return base + "." + new_ext

    @staticmethod
    def _init_llvm() -> None:
        llvm.initialize()
        llvm.initialize_native_target()
        llvm.initialize_native_asmprinter()
    
    @staticmethod
    def shutdown() -> None:
        llvm.shutdown()

    def _compile_file(self) -> StrPath:
        llvm_file: StrPath = self._change_file_extension(
            os.path.basename(self.file_path), "ll")

        llvm_path: StrPath = os.path.join(LL_PATH, llvm_file)

        result: CompletedProcess[str] = Srun([
            "clang", "-O0", "-S", "-emit-llvm", self.file_path, "-o", llvm_path
        ],
                                             capture_output=True,
                                             text=True)

        if result.returncode != 0:
            raise FileNotFoundError(f"\nError generating LLVM IR: \n{result.stderr}")

        return llvm_path

    def _parse_llvm(self, llvm_path: StrPath) -> ModuleRef:
        with open(llvm_path, "r") as file:
            llvm_ir: str = file.read()

        self._init_llvm()

        module: ModuleRef = llvm.parse_assembly(llvm_ir)

        module.verify()

        os.remove(llvm_path)

        return module

    def generate_ssa(self) -> ModuleRef:
        llvm: StrPath = self._compile_file()

        return self._parse_llvm(llvm)


class ProcessFile():
    _file_module: Final[ModuleRef]
    binary_ops: Final[list[str]] = ["sub"]

    def __init__(self, file: StrPath) -> None:
        generator: GenerateSSA = GenerateSSA(file)

        self._file_module = generator.generate_ssa()

    def get_functions(self) -> dict[FunctionName, ValueRef]:
        functions: dict[FunctionName, ValueRef] = {}

        for function in self._file_module.functions:
            functions[function.name] = function

        return functions

    @staticmethod
    def _get_block_label(block: ValueRef) -> Labels:
        block_inst: list[str] = str(block).strip().split("/n")

        return int(block_inst[0].split(":")[0])

    def _parse_block(self, block: ValueRef) -> list[ValueRef]:
        block_instructions: list[ValueRef] = []

        for instruction in block.instructions:
            block_instructions.append(instruction)

        return block_instructions

    def get_function_blocks(
            self, function: FunctionName) -> dict[Labels, Instructions] | None:
        blocks: dict[Labels, Instructions] = {}
        function_module: ValueRef = self._file_module.get_function(function)

        try:
            blocks_iter = function_module.blocks
            blocks[0] = self._parse_block(next(blocks_iter))
        except StopIteration:
            print(f"Function {function} has no blocks.", file=sys.stderr)
            return None

        for block in blocks_iter:
            label: Labels = self._get_block_label(block)
            blocks[label] = self._parse_block(block)

        return blocks

    def get_instruction_info(self, instruction: ValueRef) -> tuple[str | int, ...] | None:
        inst_opcode: str = cast(str, instruction.opcode)
        operands: list[str]
        instr_list: list[str] = str(instruction).strip().split()

        match inst_opcode:
            case "alloca":
                return None
            case _ if inst_opcode in self.binary_ops:
                operands = self._handle_bin_ops(instr_list)
            case "load":
                operands = self._handle_loads(instr_list)
            case "store":
                operands = self._handle_stores(instr_list)
            case "call":
                operands = self._handle_calls(instruction)
            case _:
                operands = []

        return (inst_opcode, *operands)
    
    @staticmethod
    def _handle_registers(reg: str) -> str | int:
        if '%' not in reg:
            return int(reg)
    
        return reg

    @staticmethod
    def _handle_bin_ops(instr_parts: list[str]) -> list[str]:
        res = instr_parts[0]
        arg1 = ProcessFile._handle_registers(instr_parts[5][:-1])
        arg2 = ProcessFile._handle_registers(instr_parts[6])

        return [res, arg1, arg2]

    @staticmethod
    def _handle_loads(instr_parts: list[str]) -> list[str]:
        res = instr_parts[0]
        load_from = ProcessFile._handle_registers(instr_parts[5][:-1])

        return [res, load_from]

    @staticmethod
    def _handle_stores(instr_parts: list[str]) -> list[str]:
        store_reg = instr_parts[4][:-1]
        value_to_store = ProcessFile._handle_registers(instr_parts[2][:-1])

        return [store_reg, value_to_store]


    def _handle_calls(self, instruction: ValueRef) -> list[str]:
        idx_func_name: int = str(instruction).find("@")
        words_before_func = len(str(instruction)[:idx_func_name-1].strip().split())
        instr_parts = str(instruction).strip().split(maxsplit=words_before_func)
        ret_type = instr_parts[instr_parts.index("call") + 1]
        res: str | None = None

        if ret_type != "void":
            res = instr_parts[0]
        
        start_args_idx = instr_parts[-1].find('(')
        end_args_idx = instr_parts[-1].rfind(')')

        func_name = instr_parts[-1][1:start_args_idx]
        arguments: list[str] = instr_parts[-1][start_args_idx+1:end_args_idx]

        return [res, ret_type, func_name, arguments]
