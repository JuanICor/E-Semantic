from __future__ import annotations
from typing import Callable, TypeAlias, Union, TYPE_CHECKING

if TYPE_CHECKING:
    from egraph import Arithmetics, Unit
    from tree_sitter import Node, Query, Language

FileNames: TypeAlias = str
QueryString: TypeAlias = str
Tag: TypeAlias = str
PatternIndex: TypeAlias = int

ASTNode: TypeAlias = 'Node'
TSQuery: TypeAlias = 'Query'
TreeLanguage: TypeAlias = 'Language'

CapturedNodes: TypeAlias = dict[Tag, list[ASTNode]]
MatchedNodes: TypeAlias = list[tuple[PatternIndex, CapturedNodes]]

ArithmeticParameter: TypeAlias = Union['Arithmetics', 'Unit']

NodeHandler: TypeAlias = dict[str, Callable[[ASTNode], ArithmeticParameter]]

ArithmeticFun : TypeAlias = Callable[[ArithmeticParameter, ArithmeticParameter], 'Arithmetics']
ArithmeticsRelation: TypeAlias = Callable[[ArithmeticParameter, ArithmeticParameter], 'Unit']
