from Classes.parse_file import ParseFile
from typing import Final
from pycparser.c_ast import *
from egraph import *

operations: dict[str, Callable[[Arithmetics, Arithmetics], Arithmetics]] = {
    '+': sum,
    '*': mult
}

def construct_expressions(node: Node) -> Arithmetics:
    
    if isinstance(node, ID):
        return Arithmetics.var(node.name)
    
    elif isinstance(node, Constant) and node.type == 'int':
        return Arithmetics(int(node.value))
    
    elif isinstance(node, BinaryOp):
        op: Callable[[Arithmetics, Arithmetics], Arithmetics] = operations.get(node.op)

        if op is None:
            raise ValueError

        return op(
            construct_expressions(node.left),
            construct_expressions(node.right)
        )

    elif isinstance(node, Assignment):
        ops: list[str] = operations.keys()
        op: Callable[[Arithmetics, Arithmetics], Arithmetics] = None

        for operation in ops:
            if operation in node.op:
                op = operations.get(operation)
        
        if op is not None:
            return assign(
                construct_expressions(node.lvalue),
                op(
                    construct_expressions(node.lvalue),
                    construct_expressions(node.rvalue)
                    )
            )

        else:
            return assign(
                construct_expressions(node.lvalue),
                construct_expressions(node.rvalue)
            )


if __name__ == '__main__':
    PATH: Final = "./Samples/eqClass"

    parser1: ParseFile = ParseFile(PATH + '00/op_sum_sample01.c')
    parser2: ParseFile = ParseFile(PATH + '00/op_sum_sample04.c')

    assigns1: list[Assignment] = parser1.get_assignments()
    assigns2: list[Assignment] = parser2.get_assignments()

    expr1: Expr = egraph.let("expr1", construct_expressions(assigns1[0]))
    expr2: Expr = egraph.let("expr2", construct_expressions(assigns2[0]))

    egraph.run(10)

    try:
        egraph.check(eq(expr1).to(expr2))
        print("Expressions are equal.")
    
    except Exception:
        print("Expression are not equal.")