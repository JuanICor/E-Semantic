import os
import sys
import re
from subprocess import CalledProcessError, run as Srun
from llvmlite import binding as llvm
from llvmlite.binding import ModuleRef, ValueRef

from typing import TypeAlias, Final, cast, NamedTuple, Optional

FilePath: TypeAlias = str
FileName: TypeAlias = str
FunctionName: TypeAlias = str
Instructions: TypeAlias = list[ValueRef]
Labels: TypeAlias = int


class InstrInfo(NamedTuple):
    opcode: str
    res_reg: Optional[str] = None
    arg1: Optional[str] = None
    arg2: Optional[str] = None
    function_name: Optional[str] = None
    function_args: Optional[str] = None


LL_PATH: Final[FilePath] = os.getcwd()


class GenerateSSA():
    CFLAGS: Final = ["-O0", "-S", "-emit-llvm"]

    def __init__(self, file_path: FilePath) -> None:
        self.file_path: Final = file_path

    @staticmethod
    def _change_file_extension(file_path: FileName, new_ext: str) -> FileName:
        base, _ = os.path.splitext(file_path)

        return base + "." + new_ext

    def _create_llvm_path(self) -> FilePath:
        llvm_file = self._change_file_extension(
            os.path.basename(self.file_path), "ll")

        return os.path.join(LL_PATH, llvm_file)

    @staticmethod
    def _init_llvm() -> None:
        llvm.initialize()
        llvm.initialize_native_target()
        llvm.initialize_native_asmprinter()

    @staticmethod
    def shutdown() -> None:
        llvm.shutdown()

    def compile_file(self,
                     compilation_flags: list[str] | None = None) -> FilePath:
        if compilation_flags is None:
            compilation_flags = self.CFLAGS

        llvm_path = self._create_llvm_path()

        try:
            Srun(
                ["clang", *compilation_flags, self.file_path, "-o", llvm_path],
                capture_output=True,
                text=True,
                check=True)
        except CalledProcessError as e:
            print(f"Compilation failed with return code: {e.returncode}")

        return llvm_path

    def _parse_llvm(self, llvm_path: FilePath) -> ModuleRef:
        self._init_llvm()

        with open(llvm_path, "r", encoding="utf-8") as llvm_file:
            module: ModuleRef = llvm.parse_assembly(llvm_file.read())

        module.verify()

        os.remove(llvm_path)

        return module

    def generate_ssa(self) -> ModuleRef:
        llvm_path: FilePath = self.compile_file()

        return self._parse_llvm(llvm_path)


class ProcessFile():
    BINARY_OPS: Final[list[str]] = ["sub", "add"]
    COMPARATIVE_OPS: Final[list[str]] = ["icmp"]
    IGNORE_OPS: Final[list[str]] = ["alloca", "ret"]

    def __init__(self, file: FilePath) -> None:
        generator: GenerateSSA = GenerateSSA(file)

        self._file_module: Final[ModuleRef] = generator.generate_ssa()

    def get_functions(self) -> dict[FunctionName, ValueRef]:
        functions: dict[FunctionName, ValueRef] = {}

        for function in self._file_module.functions:
            functions[function.name] = function

        return functions

    @staticmethod
    def _get_block_label(block: ValueRef) -> Labels:
        block_inst: list[str] = str(block).strip().split("/n")

        return int(block_inst[0].split(":")[0])

    @staticmethod
    def _parse_block(block: ValueRef) -> list[ValueRef]:
        block_instructions: list[ValueRef] = []

        for instruction in block.instructions:
            block_instructions.append(instruction)

        return block_instructions

    def get_function_blocks(
            self, function: FunctionName) -> dict[Labels, Instructions] | None:
        blocks: dict[Labels, Instructions] = {}
        function_module: ValueRef = self._file_module.get_function(function)
        len(list(function_module.arguments))

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

    def get_instruction_info(self, instruction: ValueRef) -> InstrInfo | None:
        inst_opcode: str = cast(str, instruction.opcode)
        operands: tuple[str, ...]
        instr_information: InstrInfo
        instruction_string = str(instruction).strip()

        match inst_opcode:
            case _ if inst_opcode in self.IGNORE_OPS:
                return None

            case _ if inst_opcode in self.BINARY_OPS:
                operands = self._handle_bin_ops(instruction_string)
                instr_information = InstrInfo(opcode=inst_opcode,
                                              res_reg=operands[0],
                                              arg1=operands[1],
                                              arg2=operands[2])

            case _ if inst_opcode in self.COMPARATIVE_OPS:
                operands = self._handle_comps(instruction_string)
                instr_information = InstrInfo(opcode=inst_opcode,
                                              res_reg=operands[0],
                                              arg1=operands[1],
                                              arg2=operands[2])
            case "load":
                operands = self._handle_loads(instruction_string)
                instr_information = InstrInfo(opcode=inst_opcode,
                                              res_reg=operands[0],
                                              arg1=operands[1])
            case "store":
                operands = self._handle_stores(instruction_string)
                instr_information = InstrInfo(opcode=inst_opcode,
                                              res_reg=operands[0],
                                              arg1=operands[1])

            case "call":
                if len(operands := self._handle_calls(instruction_string)) > 2:
                    instr_information = InstrInfo(opcode=inst_opcode,
                                                  res_reg=operands[0],
                                                  function_name=operands[1],
                                                  function_args=operands[2])
                else:
                    instr_information = InstrInfo(opcode=inst_opcode,
                                                  function_name=operands[0],
                                                  function_args=operands[1])

            case "br":
                operands = self._handle_breaks(instruction_string)

            case _:
                raise ValueError(
                    f"No implementation for instructions with {inst_opcode}")

        return instr_information

    @staticmethod
    def _get_match(pattern: str, instr: str) -> re.Match[str]:
        if (match := re.match(pattern, instr)) is None:
            raise ValueError(f"Couldn't find match in instrucction: {instr}")

        return match

    @staticmethod
    def _handle_bin_ops(instr: str) -> tuple[str, ...]:
        binary_ops_pattern: Final = r"^(%\d+) = .+? ((?:%|)\d+).*?((?:%|)\d+)"
        match = ProcessFile._get_match(binary_ops_pattern, instr)

        return match.groups()

    @staticmethod
    def _handle_comps(instr: str) -> tuple[str, ...]:
        comp_pattern: Final = r"^(%\d+) = \S+ (\w+)[^%]*((?:%|)\d+).*?((?:%|)\d+)"
        match = ProcessFile._get_match(comp_pattern, instr)

        return match.groups()

    @staticmethod
    def _handle_loads(instr: str) -> tuple[str, ...]:
        load_pattern: Final = r"^(%\d+) = .+? (%\d+), .+$"
        match = ProcessFile._get_match(load_pattern, instr)

        return match.groups()

    @staticmethod
    def _handle_stores(instr: str) -> tuple[str, ...]:
        store_pattern: Final = r"^store .+? ((?:%|)\d+), .+? (%\d+), .+?$"
        match = ProcessFile._get_match(store_pattern, instr)

        # We reverse it because the store operations have the register where the
        # result is stored second
        return match.groups()[::-1]

    @staticmethod
    def _handle_calls(instr: str) -> tuple[str, ...]:
        calls_patterns: Final = r"(?:(%\d+).*?)?call.*?@(\w+)\((.+)\)"
        match = ProcessFile._get_match(calls_patterns, instr)

        return match.groups()

    @staticmethod
    def _handle_breaks(instr: str) -> tuple[str, ...]:
        break_patterns: Final = r"br(?:.*?(%\d+),\s+label\s+(%\d+),)?\s+label\s+(%\d+)"
        match = ProcessFile._get_match(break_patterns, instr)

        return match.groups()


def create_vars_mapping(file: FilePath) -> dict[str, str]:
    llvm_path = GenerateSSA(file).compile_file(
        compilation_flags=GenerateSSA.CFLAGS + ["-g"])

    with open(llvm_path, "r", encoding="utf-8") as llvm_file:
        llvm_string = llvm_file.read()

    registers_metadata = re.findall(
        r"@[\w\.]+\(metadata.*?(%\d+), metadata.*?(!\d+),.*\)", llvm_string)
    variables_metadata = re.findall(
        r"(!\d+).+?!DILocalVariable\(name: \"(\S+)\".*?\)", llvm_string)

    joined_values = inner_join(variables_metadata,
                               map(lambda x: x[::-1], registers_metadata))

    cured_regs = map(lambda t: (t[0], t[1]), joined_values)

    return dict(cured_regs)


from collections.abc import Iterable

MatchedTuple: TypeAlias = tuple[str, str]


def inner_join(iter_a: Iterable[MatchedTuple],
               iter_b: Iterable[MatchedTuple]) -> Iterable:
    temp_dict: dict[str, MatchedTuple] = {}

    for item in iter_b:
        temp_dict[item[0]] = item

    for item in iter_a:
        matched_items = temp_dict.get(item[0])
        if matched_items is not None:
            yield item[1:] + matched_items[1:]
