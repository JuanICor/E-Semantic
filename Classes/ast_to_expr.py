from __future__ import annotations
import sys

sys.path.append("../E-Semantic")

from behemoth import ArithmeticFun, NodeHandler, ASTNode
from egraph import *
from Classes.tree_parser import ENCODING

from typing import Optional, Union

class ASTExpresion():
    def __init__(self) -> None:
        self.__node_handler: NodeHandler = {
            "identifier" : self.identifier_to_expr,
            "number_literal": self.interger_to_expr,
            "binary_expression": self.binary_to_expr,
            "assignment_expression": self.assignment_to_expr
        }

        self.__operations: dict[str, ArithmeticFun] = {
            '+' : sum,
            '*' : mult,
            '<<': lshift
        }
    

    def __get_operation__(self, op: str) -> ArithmeticFun:
        return self.__operations[op]


    def __find_operation__(self, node_type: str) -> Optional[ArithmeticFun]:
        for op in self.__operations.keys():
            if op in node_type:
                return self.__operations.get(op)
        
        return None


    def expression_construct(self, node: Optional[ASTNode]) -> Union[Arithmetics, Unit]:
        if node is None:
            return self.default_expr()
        
        handler = self.__node_handler.get(node.type, self.default_expr)

        return handler(node)
    

    def identifier_to_expr(self, node: ASTNode) -> Arithmetics:
        return Arithmetics.var(node.text.decode(ENCODING))          #type: ignore  # 'node' cannot be None as that case is handled by 'expression_construct'
    

    def interger_to_expr(self, node: ASTNode) -> Arithmetics:
        return Arithmetics(int(node.text.decode(ENCODING)))         #type: ignore  # 'node' cannot be None as that case is handled by 'expression_construct'
    

    def binary_to_expr(self, node: ASTNode) -> Arithmetics:
        operation: ArithmeticFun = self.__get_operation__(node.child(1).type)       #type: ignore  
                                                                                    #'node' cannot be None as that case is handled by 'expression_construct'
        return operation(
            self.expression_construct(node.child(0)),
            self.expression_construct(node.child(2))
        )


    def assignment_to_expr(self, node: ASTNode) -> Unit:
        operation: Optional[ArithmeticFun] = self.__find_operation__(node.child(1).type)  #type: ignore  # 'node' cannot be None as that case is handled by 'expression_construct'
        variable: bytes = node.child(0).text                                              #type: ignore  # 'node' cannot be None as that case is handled by 'expression_construct'
        var: Arithmetics = Arithmetics.var(variable.decode(ENCODING))

        if operation is None:
            return assignment(
                var,
                self.expression_construct(node.child(2))
            )
        else:
            return assignment(
                var,
                operation(
                    self.expression_construct(node.child(0)),
                    self.expression_construct(node.child(2))
                )
            )


    def default_expr(self, node: Optional[ASTNode] = None) -> Arithmetics:
        return Arithmetics(0)