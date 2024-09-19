from pycparser import parse_file
from pycparser.c_ast import *
import pycparser_fake_libc          # type: ignore
from Classes.visitors import AssignmentVisitor, FunctionBodyVisitor

class ParseFile():
    def __init__(self, filename: str) -> None:
        fake_libc_arg: str = "-I" + pycparser_fake_libc.directory
        
        self.ast: FileAST = parse_file(filename, use_cpp=True,
                                        cpp_path='gcc',
                                        cpp_args=['-E', fake_libc_arg])
        
    def get_assignments(self) -> list[Assignment]:
        main_visitor: FunctionBodyVisitor = FunctionBodyVisitor('main')
        visitor: AssignmentVisitor = AssignmentVisitor()

        main_visitor.visit(self.ast)
        visitor.visit(main_visitor.func_body)

        return visitor.assignments