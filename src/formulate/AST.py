"""
Copyright (c) 2023 Aryan Roy. All rights reserved.

formulate:  Easy conversions between different styles of expressions
"""
from __future__ import annotations
from dataclasses import dataclass
from typing import Union

import lark


class AST:  # only three types (and a superclass to set them up)
    _fields = ()


@dataclass
class Literal(AST):  # Literal: value that appears in the program text
    value: float
    index: int = None

    def __str__(self):
        return str(self.value)


@dataclass
class Symbol(AST):  # Symbol: value referenced by name
    symbol: str
    index: int = None

    def __str__(self):
        return self.symbol


@dataclass
class UnaryOperator(AST):  # Unary Operator: Operation with one operand
    sign: Symbol
    operand: Literal
    index: int = None

    def __str__(self):
        return "{0}({1})".format(str(self.sign), self.operand)


@dataclass
class BinaryOperator(AST):  # Binary Operator: Operation with two operands
    sign: Symbol
    left: Literal
    right: Literal
    index: int = None

    def __str__(self):
        return "{0}({1},{2})".format(str(self.sign), self.left, self.right)


@dataclass
class Matrix(AST):  # Matrix: A matrix call
    var: Symbol
    paren: list[AST]
    index: int = None

    def __str__(self):
        return "{0}[{1}]".format(str(self.var), ",".join(str(x) for x in self.paren))


@dataclass
class Slice(AST):  # Slice: The slice for matrix
    slices: AST
    index: int = None

    def __str__(self):
        return "{0}".format(self.slices)


@dataclass
class Empty(AST):  # Slice: The slice for matrix
    index: int = None

    def __str__(self):
        return ""


@dataclass
class Call(AST):  # Call: evaluate a function on arguments
    function: Union[list[Symbol], Symbol]
    arguments: list[AST]
    index: int = None

    def __str__(self):
        return "{0}({1})".format(
            self.function,
            ", ".join(str(x) for x in self.arguments),
        )


# come-up with a shared notation for functions
# make a  to_python function
