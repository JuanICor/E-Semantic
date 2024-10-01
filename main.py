from Classes.tree_parser import TreeParser
from Classes.ast_to_expr import ASTExpresion
from egraph import *
from behemoth import *

from typing import Final, Optional

PATH: Final = "./Samples/eqClass"

queries: list[QueryString] = [
    """
    (assignment_expression
        left: (identifier)
        right: (binary_expression
                    left: (identifier) @unknown
                    right: (number_literal)
                )
    ) @target
    """,
    """
    (assignment_expression
        left: (identifier) @unknown
        right: (number_literal)
    ) @target
    """
]

files: list[FileNames] = [
    "op_mult_sample01.c",
    "op_mult_sample02.c"
]

eq_Class: list[str] = [
    "00"
]

query_for_file: dict[FileNames, QueryString] = dict(zip(files, queries))

def print_nodes(d: CapturedNodes) -> None:
    for l in d.values():
        for node in l:
            print(node)
    

def get_code_between_comments(parser: TreeParser) -> list[ASTNode]:
    query: str = '''
                (comment) @comments
                '''

    matches: dict[str, list[ASTNode]] = parser.get_matches(query)
    nodes: list[ASTNode] = matches['comments']
    
    return parser.get_nodes_between(nodes[0], nodes[1])

def main() -> None:
    interpreter: ASTExpresion = ASTExpresion()
    file1: Final = files[0]
    file2: Final = files[1]

    sample01: TreeParser = TreeParser(PATH + eq_Class[0] + "/" + file1)
    sample02: TreeParser = TreeParser(PATH + eq_Class[0] + "/" + file2)
 
    s01_nodes: CapturedNodes = sample01.capture_nodes(query_for_file[file1])
    s02_nodes: CapturedNodes = sample02.capture_nodes(query_for_file[file2])

    s01_target: ASTNode = s01_nodes["target"][0]
    s02_target: ASTNode = s02_nodes["target"][0]

    expr1: Expr = egraph.let("expr1", interpreter.expression_construct(s01_target))
    expr2: Expr = egraph.let("expr2", interpreter.expression_construct(s02_target))

    s01_unknown: ASTNode = s01_nodes["unknown"][0]
    s02_unknown: ASTNode = s02_nodes["unknown"][0]

    s01_var: Optional[ASTNode] = sample01.get_previous_assignment_to(s01_target, s01_unknown.text.decode('utf-8'))
    s02_var: Optional[ASTNode] = sample02.get_previous_assignment_to(s02_target, s02_unknown.text.decode('utf-8'))

    if s01_var is None:
        expr1a: Expr = egraph.let("expr1a", assignment(Arithmetics.var(s01_unknown.text.decode('utf-8')), Arithmetics(1)))
    else:
        expr1a: Expr = egraph.let("expr1a", interpreter.expression_construct(s01_var))

    if s02_var is None:
        expr2a: Expr = egraph.let("expr2a", assignment(Arithmetics.var(s02_unknown.text.decode('utf-8')), Arithmetics(1)))
    else:
        expr2a: Expr = egraph.let("expr2a", interpreter.expression_construct(s02_var))

    egraph.run(10)

    try:
        egraph.check(eq(expr1).to(expr2))
        print("The Expressions are equal.")
    except Exception:
        print("The Expression are not equal.")

if __name__ == "__main__":
    main()