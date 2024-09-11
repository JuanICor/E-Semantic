"""
Auxiliary File for defining differents types
used in pycparser. Most of them taken from a stub file
from "https://gist.github.com/simonlindholm/a08dabc8afe58af985015183ef425fa1.js"
"""
from pycparser.c_ast import *
from typing import Union as Union_

Expression: type[object] = Union_[
    ArrayRef,
    Assignment,
    BinaryOp,
    Cast,
    CompoundLiteral,
    Constant,
    ExprList,
    FuncCall,
    ID,
    StructRef,
    TernaryOp,
    UnaryOp,
]

Statement: type[object] = Union_[
    Expression,
    Break,
    Case,
    Compound,
    Continue,
    Decl,
    Default,
    DoWhile,
    EmptyStatement,
    For,
    Goto,
    If,
    Label,
    Return,
    Switch,
    Typedef,
    While,
    Pragma,
]