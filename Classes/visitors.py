from pycparser.c_ast import *

class FunctionBodyVisitor(NodeVisitor):
    func_body: Compound

    def __init__(self, func_name: str) -> None:
        self.func_name: str = func_name
        
    def visit_FuncDef(self, node: FuncDef) -> None:
        if node.decl.name == self.func_name:
            self.func_body = node.body
        
class AssignmentVisitor(NodeVisitor):
    def __init__(self) -> None:
        self.assignments: list[Assignment] = []
    
    def visit_Assignment(self, node: Assignment) -> None:
        self.assignments.append(node)

class BinaryOpsVisitor(NodeVisitor):
    def __init__(self) -> None:
        self.bin_ops: list[BinaryOp] = []
    
    def visit_BinaryOp(self, node: BinaryOp) -> None:
        self.bin_ops.append(node)
