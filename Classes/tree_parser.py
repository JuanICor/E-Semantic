import sys

sys.path.append("../E-Semantic")

import tree_sitter_c as CLanguage   
from behemoth import *
from tree_sitter import *

from typing import Final, Optional, TypeGuard

ENCODING: Final = "utf8"

class TreeParser():
    
    __code: bytes
    __language: TreeLanguage
    tree: Tree

    def __init__(self, filename: str) -> None:
        self.__language = Language(CLanguage.language())
        
        with open(filename, "r") as file:
            self.__code = bytes(file.read(), ENCODING)

        parser: Parser = Parser(self.__language)
        self.tree = parser.parse(self.__code)
    

    def __goto_parent__(self, node: ASTNode) -> TreeCursor:
        cursor: TreeCursor = self.tree.root_node.walk()

        while cursor.goto_first_child_for_byte(node.start_byte):
            pass
        
        cursor.goto_parent()

        return cursor
    

    def __keep_nodes_before_byte__(self, byte: int, nodes: list[ASTNode]) -> list[ASTNode]:
        def filter_func(node: ASTNode) -> TypeGuard[ASTNode]:
            return node.end_byte < byte
        
        return list(filter(filter_func, nodes))
    

    def __get_max_end_node__(self, source: list[ASTNode]) -> Optional[ASTNode]:
        if len(source) == 0:
            return None

        target: ASTNode = source[0]

        for node in source:
            if node.end_byte > target.end_byte:
                target = node

        return target


    def capture_nodes(self, query: QueryString, start_node: Optional[ASTNode] = None)-> CapturedNodes:
        if start_node is None:
            start_node = self.tree.root_node
        
        q: TSQuery = self.__language.query(query)

        return q.captures(start_node)


    def get_matches(self, query: QueryString, start_node: Optional[ASTNode] = None) -> MatchedNodes:
        if start_node is None:
            start_node = self.tree.root_node
        
        q : TSQuery = self.__language.query(query)
        
        return q.matches(start_node)


    def get_previous_assignment_to(self, target_node: Optional[ASTNode], target: str) -> Optional[ASTNode]:
        if target_node == self.tree.root_node or target_node is None:
            return None

        query: QueryString = f"""
                                (assignment_expression
                                    left: (identifier)  @lhs
                                    right: (_)
                                    (#eq? @lhs {target})
                                ) @assignment
                              """
        
        var_scope: TreeCursor = self.__goto_parent__(target_node)
        captures: CapturedNodes = self.capture_nodes(query, var_scope.node)
        possible_nodes: list[ASTNode] = self.__keep_nodes_before_byte__(target_node.start_byte, captures['assignment'])

        ret_node: Optional[ASTNode] = self.__get_max_end_node__(possible_nodes)

        if ret_node is None:
            return self.get_previous_assignment_to(target_node.parent, target)
        else:
            return ret_node

    
    def get_nodes_between(self, node1: ASTNode, node2: ASTNode) -> list[ASTNode]:
        sbyte: int = node1.end_byte
        ebyte: int = node2.start_byte  

        traveler: TreeCursor = self.__goto_parent__(node1)

        child_nodes: list[ASTNode] = []

        def is_in_between(target: Node) -> TypeGuard[ASTNode]:
            return target.start_byte > sbyte and target.end_byte < ebyte

        if traveler.goto_first_child():
            child_nodes.append(traveler.node)           #type: ignore # 'goto_first_child()' verifies that there exists a child.
                                                                      # Therefore traveler.node is never None
            while traveler.goto_next_sibling():
                child_nodes.append(traveler.node)       #type: ignore # Same reason as line before

        return list(filter(is_in_between, child_nodes))