from pycparser import parse_file
import pycparser_fake_libc  #type: ignore

from aux_types import *
from typing import TypeGuard

class ParseFile():
    def __init__(self, filename: str) -> None:
        fake_libc_arg: str = "-I" + pycparser_fake_libc.directory
        
        self.__ast = parse_file(filename, use_cpp=True,
                                        cpp_path='gcc',
                                        cpp_args=['-E', fake_libc_arg])
        
    def __get_funcions_defs(self) -> list[FuncDef]:

        def is_func_def(x: Union_[FuncDecl, Decl, Typedef, Pragma]) -> TypeGuard[FuncDef]:
            return isinstance(x, FuncDef)

        return list(filter(is_func_def, self.__ast.ext))
        
    def __get_sentences(self) -> list[Statement | None]:
        function_definitions: list[FuncDef] = self.__get_funcions_defs()
        return function_definitions[-1].body.block_items
    
    def get_assigments(self) -> list[Assignment]:
        sentences: list[Statement] = self.__get_sentences()

        def is_assignment(x: Statement) -> TypeGuard[Assignment]:
            return isinstance(x, Assignment)

        return list(filter(is_assignment, sentences))
