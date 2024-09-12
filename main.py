from Classes.arithmetics_graph import *
from Classes.tree_parser import TreeParser

def get_code_between_comments(parser: TreeParser) -> str:
    query: str = '''
                (comment) @comments
                '''

    matches: dict[str, list[Node]] = parser.get_matches(query)
    nodes = matches['comments']
    