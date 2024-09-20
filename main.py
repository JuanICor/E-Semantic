from Classes.tree_parser import TreeParser
from egraph import *
from tree_sitter import Node as ASTNode

from typing import Final, Callable

PATH: Final = "./Samples/eqClass"

ArithmeticFun : type = Callable[[Arithmetics, Arithmetics], Arithmetics]

operations: dict[str, ArithmeticFun] = {'+' : sum, '*': mult, '<<': lshift}

def get_code_between_comments(parser: TreeParser) -> list[ASTNode]:
    query: str = '''
                (comment) @comments
                '''

    matches: dict[str, list[ASTNode]] = parser.get_matches(query)
    nodes: list[ASTNode] = matches['comments']
    
    return parser.get_nodes_between(nodes[0], nodes[1])

# Hacerlo una clase ('AST to Expression')
def expression_construct(n: ASTNode) -> Arithmetics:
    nodeType : str = n.type

    if nodeType == "identifier":
        return Arithmetics.var(n.text.decode("utf8"))

    elif nodeType == "number_literal":
        return Arithmetics(int(n.text))

    elif nodeType == "binary_expression":
        operation: ArithmeticFun = operations.get(n.child(1).type)
        return operation(expression_construct(n.child(0)),
                         expression_construct(n.child(2))
                        )

    elif nodeType == "assignment_expression":
        operators: set[str] = operations.keys()
        operation: ArithmeticFun = None

        for op in operators:
            if op in n.child(1).type:
                operation = operations.get(op)
                break

        temp_node: ASTNode = n.child(0)

        if operation is not None:
            return assign(Arithmetics.var(temp_node.text.decode("utf8")),
                              operation(expression_construct(n.child(0)),
                                        expression_construct(n.child(2))
                                       )
                         )
        else:
            return assign(Arithmetics.var(temp_node.text.decode("utf8")),
                              expression_construct(n.child(2))
                         )
    
    pass

if __name__ == "__main__":

    sample_nums: list[str] = ["00"]
    file1: Final = "op_mult_sample01.c"
    file2: Final = "op_mult_sample02.c"

    sample01: TreeParser = TreeParser(PATH + sample_nums[0] + "/" + file1)
    sample02: TreeParser = TreeParser(PATH + sample_nums[0] + "/" + file2)

    target_1: ASTNode = get_code_between_comments(sample01)[0]
    target_2: ASTNode = get_code_between_comments(sample02)[0]

    expr1 = egraph.let("expr1", expression_construct(target_1.child(0)))
    expr2 = egraph.let("expr2", expression_construct(target_2.child(0)))

    egraph.run(10)

    try:
        egraph.check(eq(expr1).to(expr2))
        print("The Expressions are equal.")
    except Exception:
        print("The Expression are not equal.")