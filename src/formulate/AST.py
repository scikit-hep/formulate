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

    # def check_CNAME(self):
    #     regex = "((\.)\2{2,})"
    #     x = re.search(regex, self.symbol)
    #     print(x)
    #     return x

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
            case "inf":
                return "np.inf"
            case "nan":
                return "np.nan"
            case "sqrt2":
                return "np.sqrt(2)"
            case "piby2":
                return "(np.pi/2)" 
            case "piby4":
                return "(np.pi/4)"            
            case "2pi":
                return "(np.pi*2.0)"
            case "ln10":
                return f"np.log(10)"
            case "loge":
                return f"np.log10(np.exp(1))"
            case "log":
                return f"np.log10({self.arguments[0]})"
            case "log2":
                return f"(np.log({self.arguments[0]})/log(2))"
            case "degtorad":
                return f"np.radians({self.arguments[0]})"
            case "radtodeg":
                return f"np.degrees({self.arguments[0]})"
            case "exp":
                return f"np.exp({self.arguments[0]})"
            case "sin":
                return f"np.sin({self.arguments[0]})"
            case "asin":
                return f"np.arcsin({self.arguments[0]})"
            case "sinh":
                return f"np.sinh({self.arguments[0]})"
            case "asinh":
                return f"np.arcsinh({self.arguments[0]})"
            case "cos":
                return f"np.cos({self.arguments[0]})"
            case "arccos":
                return f"np.arccos({self.arguments[0]})"
            case "cosh":
                return f"np.cosh({self.arguments[0]})"    
            case "acosh":
                return f"np.arccosh({self.arguments[0]})"
            case "tan":
                return f"np.tan({self.arguments[0]})"
            case "arctan":
                return f"np.arctan({self.arguments[0]})"
            case "tanh":
                return f"np.tanh({self.arguments[0]})"
            case "atanh":
                return f"np.arctanh({self.arguments[0]})"
            case "Math::sqrt":
                return f"np.sqrt({self.arguments[0]})"
            case "ceil":
                return f"np.ceil({self.arguments[0]})"
            case "abs":
                return f"np.abs({self.arguments[0]})"
            case "even":
                return f"! ({self.arguments[0]} % 2)"
            case "factorial":
                return f"np.math.factorial({self.arguments[0]})"
            case "floor":
                return f"! np.floor({self.arguments[0]})"
            case "abs":
                return f"np.abs({self.arguments[0]})"
            case "max":
                return f"root_max({self.arguments[0]})"
            case "min":
                return f"root_min({self.arguments[0]})"
            case "sum":
                return f"root_sum({self.arguments[0]})"
            case "no_of_entries":
                return f"root_length({self.arguments[0]})"
            case "min_if":
                return f"root_min_if({self.arguments[0]}, {self.arguments[1]})"
            case "max_if":
                return f"root_max_if({self.arguments[0]}, {self.arguments[1]})"
            case _ :
                raise ValueError("Not a valid function!")


