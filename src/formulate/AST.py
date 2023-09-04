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

    def unary_to_ufunc(self, sign):
        signmap = {"~": "np.invert", "!": "np.logical_not"}
        return signmap[str(sign)]

    def to_python(self):
        if str(self.sign) in {"~", "!"}:
            pycode = (
                self.unary_to_ufunc(self.sign)
                + "("
                + str(self.operand.to_python())
                + ")"
            )
        else:
            pycode = (
                "(" + str(self.sign.to_python()) + str(self.operand.to_python()) + ")"
            )
        return pycode


@dataclass
class BinaryOperator(AST):  # Binary Operator: Operation with two operands
    sign: Symbol
    left: AST
    right: AST
    index: int = None

    def __str__(self):
        return "{0}({1},{2})".format(str(self.sign), self.left, self.right)

    def binary_to_ufunc(self, sign):
        sign_mapping = {
            "&": "np.bitwise_and",
            "|": "np.bitwise_or",
            "&&": "and",
            "||": "or",
        }
        return sign_mapping[str(sign)]

    def to_python(self):
        if str(self.sign) in {
            "&",
            "|",
        }:
            pycode = (
                self.binary_to_ufunc(self.sign)
                + "("
                + self.left.to_python()
                + ","
                + self.right.to_python()
                + ")"
            )
        elif str(self.sign) in {
            "&&",
            "||",
        }:
            pycode = (
                "("
                + self.left.to_python()
                + " "
                + self.binary_to_ufunc(self.sign)
                + " "
                + self.right.to_python()
                + ")"
            )
        else:
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
        temp_str = [ "," + elem.to_python() for elem in self.paren]
        return "(" + str(self.var.to_python()) + "[:" + "".join(temp_str)+"]" + ")"


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

    def to_python(self):
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
    
    def to_python(self):
        print(str(self.function))
        match str(self.function):
            case "pi":
                return "np.pi"
            case "e":
                return "np.exp(1)"
            case _ :
                raise ValueError("Not a valid function!")

# come-up with a shared notation for functions
# make a  to_python function
