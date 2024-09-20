import tree_sitter_c as CLanguage
from tree_sitter import *

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
        
        return q.captures(self.__tree.root_node)

    def __goto_parent__(self, node: Node) -> TreeCursor:
        cursor: TreeCursor = self.__tree.root_node.walk()

        while cursor.goto_first_child_for_byte(node.start_byte):
            pass
        
        cursor.goto_parent()

        return cursor
    
    def get_nodes_between(self, node1: Node, node2: Node) -> list[Node]:
        sbyte: int = node1.end_byte
        ebyte: int = node2.start_byte  

        traveler: TreeCursor = self.__goto_parent__(node1)

        nodes_between: list[Node] = []

        def is_in_between(target: Node) -> bool:
            return target.start_byte > sbyte and target.end_byte < ebyte

        if traveler.goto_first_child():
            curr_node: Node = traveler.node         #type: ignore # 'goto_first_child()' returns true only if a node exists.
                                                                  # Therefore traveler.node cannot be None
            if is_in_between(curr_node):
                nodes_between.append(curr_node)

            while traveler.goto_next_sibling():
                curr_node = traveler.node           #type: ignore # Same reason as of line 46

                if is_in_between(curr_node):
                    nodes_between.append(curr_node)

        return nodes_between