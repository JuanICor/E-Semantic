from pathlib import Path
from tempfile import TemporaryDirectory

from llvm_parser import Compiler, LlvmData, Parser
from llvm_parser.llvm_semantics import LlvmCFG


class FileProcessor:
    """
    A class to process files by compiling and parsing them using the specified tools.
    """

    @staticmethod
    def _get_absolute_path(file: str) -> Path:
        return Path(file).resolve()

    @staticmethod
    def _compile_file(filepath: Path,
                      output_dir: TemporaryDirectory[str]) -> Path:
        compiler = Compiler(output_dir)
        return compiler.compile_file(filepath)

    def get_file_llvm_data(self, file: str) -> LlvmData:
        parser = Parser(LlvmCFG)
        abs_filepath = self._get_absolute_path(file)

        with TemporaryDirectory(ignore_cleanup_errors=True) as temp_dir:
            compiled_filepath = self._compile_file(abs_filepath, temp_dir)

            return parser.parse_file(compiled_filepath)
