"""
Copyright (c) 2023 Aryan Roy. All rights reserved.

formulate:  Easy conversions between different styles of expressions
"""
from __future__ import annotations

from dataclasses import dataclass
from typing import Union
import re


class AST:  # only three types (and a superclass to set them up)
    _fields = ()


@dataclass
class Literal(AST):  # Literal: value that appears in the program text
    value: float
    index: int = None

    def __str__(self):
        return str(self.value)

    def to_python(self):
        return repr(self.value)


@dataclass
class Symbol(AST):  # Symbol: value referenced by name
    symbol: str
    index: int = None

    def __str__(self):
        return self.symbol

    def check_CNAME(self):
        regex = "((\.)\2{2,})"
        x = re.search(regex, self.symbol)
        print(x)
        return x

    def to_python(self):
        return self.symbol


@dataclass
class UnaryOperator(AST):  # Unary Operator: Operation with one operand
    sign: Symbol
    operand: Literal
    index: int = None

    def __str__(self):
        return "{0}({1})".format(str(self.sign), self.operand)

    def to_python(self):
        pycode = "(" + str(self.sign.to_python()) + str(self.operand.to_python()) + ")"
        return pycode


@dataclass
class BinaryOperator(AST):  # Binary Operator: Operation with two operands
    sign: Symbol
    left: AST
    right: AST
    index: int = None

    def __str__(self):
        return "{0}({1},{2})".format(str(self.sign), self.left, self.right)

    def pysignconvert(self, sign):
        sign_mapping = {"+": "ak.add"}
        return sign_mapping[sign]

    def to_python(self):
        pycode = (
            "("
            + str(self.left.to_python())
            + str(self.sign.to_python())
            + str(self.right.to_python())
            + ")"
        )
        return pycode


@dataclass
class Matrix(AST):  # Matrix: A matrix call
    var: Symbol
    paren: list[AST]
    index: int = None

    def __str__(self):
        return "{0}[{1}]".format(str(self.var), ",".join(str(x) for x in self.paren))

    def to_python(self):
        slices = ""
        for elem in self.paren:
            slices += "[" + elem.to_python() + "]"
        pycode = "(" + str(self.var.to_python()) + slices + ")"
        return pycode


@dataclass
class Slice(AST):  # Slice: The slice for matrix
    slices: AST
    index: int = None

    def __str__(self):
        return "{0}".format(self.slices)

    def to_python(self):
        return self.slices.to_python()


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
