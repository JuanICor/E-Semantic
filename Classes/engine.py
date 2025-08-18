from typing import cast

from llvm_parser import LlvmData
from llvm_parser.types import CFGFunction, GlobalValues

from Classes.process_file import FileProcessor


class Engine:
    """
    Class that implements the logic between modules.
    """

    def upload_user_files(self, files: list[str]):

        for file in files:
            self.upload_file(file)

    def upload_file(self, filepath: str):
        file_data = self._get_file_data(filepath)
        prog_functions = cast(list[CFGFunction], file_data['functions'])
        prog_gvars = cast(list[GlobalValues], file_data['global_variables'])

        for func in prog_functions:
            self._convert_function_to_gsa(func)

        self._upload_to_egraph(prog_gvars, prog_functions)

    def _get_file_data(self, filepath: str) -> LlvmData:

        processor = FileProcessor()

        file_data = processor.get_file_llvm_data(filepath)

        return file_data

    def _convert_function_to_gsa(self, function: CFGFunction):
        # Implement the conversion logic here
        pass

    def _upload_to_egraph(self, global_variables: list[GlobalValues], _):
        # Implement the upload logic here
        pass
