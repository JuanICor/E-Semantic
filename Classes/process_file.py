import re
from collections.abc import Iterable
from pathlib import Path
from typing import TypeAlias, Final

from llvm_parser import Compiler, Parser, ParseResult

MatchedTuple: TypeAlias = tuple[str, str]
VarMap: TypeAlias = dict[str, str]


class FileProcessor:

    def __init__(self, file_to_process: str) -> None:
        self.file = Path(file_to_process)
        self.compiler = Compiler()

    def process_file(self) -> ParseResult:

        if self.compiler.compiled_file_exists():
            compiled_llvm = self.compiler.strip_debug()
        else:
            compiled_llvm = self.compiler.compile_file(self.file)

        parse_result = Parser().parse_file(compiled_llvm)

        self.compiler.rm_compiled_file()

        return parse_result


    def create_var_map(self) -> VarMap:
        compiled_file = self.compiler.compile_file(self.file, debug=True)

        AMI_PATTERN: Final = r"@[\w\.]+\(metadata.*?(%\d+), metadata.*?(!\d+),.*\)"  # Assigned Metadata Instruction
        MN_PATTERN: Final = r"(!\d+).+?!DILocalVariable\(name: \"(\S+)\".*?\)"  # Metadata Node

        file_content = compiled_file.read_text(encoding='utf-8')

        registers_metadata = re.findall(AMI_PATTERN, file_content)
        variables_metadata = re.findall(MN_PATTERN, file_content)

        joined_values = self._inner_join(
            variables_metadata, map(lambda x: x[::-1], registers_metadata))

        cured_regs = map(lambda t: (t[0], t[1]), joined_values)

        return dict(cured_regs)

    @staticmethod
    def _inner_join(iter_a: Iterable[MatchedTuple],
                    iter_b: Iterable[MatchedTuple]) -> Iterable:
        temp_dict: dict[str, MatchedTuple] = {}

        for item in iter_b:
            temp_dict[item[0]] = item

        for item in iter_a:
            matched_items = temp_dict.get(item[0])
            if matched_items is not None:
                yield item[1:] + matched_items[1:]
