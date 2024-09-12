import tree_sitter_c as CLanguage
from tree_sitter import Language, Parser, Tree, Query, Node, TreeCursor

from typing import Final

ENCODING: Final = "utf8"

class TreeParser():
    
    def __init__(self, filename: str) -> None:
        self.__language: Language = Language(CLanguage.language())
        
        with open(filename, "r") as file:
            self.__code: bytes = bytes(file.read(), ENCODING)

        parser: Parser = Parser(self.__language)
        self.__tree: Tree = parser.parse(self.__code)
    
    def get_matches(self, query: str) -> dict[str, list[Node]]:
        q : Query = self.__language.query(query)
        
        return query.captures(self.__tree.root_node)

    def get_nodes_between(self, node1: Node, node2: Node):
        sbyte: int = node1.end_byte
        ebyte: int = node2.start_byte

        traveler: TreeCursor = self.__tree.root_node.walk()
        traveler.goto_first_child_for_byte(sbyte)

        nodes_between: list[Node] = []

        def is_in_between(target: Node, start_pos: int, end_pos: int) -> bool:
            return target.start_byte > start_pos and target.end_byte < end_pos

        if traveler.goto_first_child():
            curr_node: Node = traveler.node

            if is_in_between(curr_node, sbyte, ebyte):
                nodes_between.append(curr_node)

            while traveler.goto_next_sibling():
                curr_node: Node = traveler.node

                if is_in_between(curr_node, sbyte, ebyte):
                    nodes_between.append(curr_node)
        
        return nodes_between