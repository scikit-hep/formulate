# Licensed under a 3-clause BSD style license, see LICENSE.

from __future__ import annotations

from abc import ABCMeta, abstractmethod
from dataclasses import dataclass

from .identifiers import (
    NUMEXPR_FUNCTIONS,
    NUMEXPR_OPERATOR_SYMBOLS,
    ROOT_FUNCTIONS,
    ROOT_OPERATOR_SYMBOLS,
)


class AST(metaclass=ABCMeta):
    @abstractmethod
    def __str__(self):
        msg = "__str__() not implemented, subclass must implement it"
        raise NotImplementedError(msg)

    @abstractmethod
    def to_numexpr(self):
        msg = "to_numexpr() not implemented, subclass must implement it"
        raise NotImplementedError(msg)

    @abstractmethod
    def to_root(self):
        msg = "to_root() not implemented, subclass must implement it"
        raise NotImplementedError(msg)

    # TODO: is it worth having a to_python() method?
    def to_python(self):
        return self.to_numexpr()


@dataclass
class Literal(AST):  # Literal: value that appears in the program text
    value: int | float

    def __str__(self):
        return str(self.value)

    def to_numexpr(self):
        return repr(self.value)

    def to_root(self):
        return repr(self.value)


@dataclass
class Symbol(AST):  # Symbol: value referenced by name
    name: str

    def __str__(self):
        return self.name

    def to_numexpr(self):
        return self.name

    def to_root(self):
        return self.name


@dataclass
class UnaryOperator(AST):  # Unary Operator: Operation with one operand
    operator: str
    operand: Literal

    def __str__(self):
        return f"{self.operator}({self.operand})"

    def to_numexpr(self):
        # logical operators need to be converted to bitwise operators
        operator = "binv" if self.operator == "linv" else self.operator
        symbol = NUMEXPR_OPERATOR_SYMBOLS.get(operator, None)
        if symbol is None:
            msg = f'Operator "{operator}" is not supported in NumExpr.'
            raise ValueError(msg)
        return f"({symbol}{self.operand.to_numexpr()})"

    def to_root(self):
        # bitwise operators need to be converted to logical operators
        operator = "linv" if self.operator == "binv" else self.operator
        symbol = ROOT_OPERATOR_SYMBOLS.get(operator, None)
        if symbol is None:
            msg = f'Operator "{operator}" is not supported in ROOT.'
            raise ValueError(msg)
        return f"({symbol}{self.operand.to_root()})"


@dataclass
class BinaryOperator(AST):  # Binary Operator: Operation with two operands
    operator: str
    left: AST
    right: AST

    def __str__(self):
        return f"{self.operator}({self.left}, {self.right})"

    def to_numexpr(self):
        # logical operators need to be converted to bitwise operators
        operator = (
            self.operator
            if self.operator not in ("land", "lor")
            else f"b{self.operator[1:]}"
        )
        symbol = NUMEXPR_OPERATOR_SYMBOLS.get(operator, None)
        if symbol is None:
            msg = f'Operator "{operator}" is not supported in NumExpr.'
            raise ValueError(msg)
        return f"({self.left.to_numexpr()} {symbol} {self.right.to_numexpr()})"

    def to_root(self):
        # bitwise operators need to be converted to logical operators
        operator = (
            self.operator
            if self.operator not in ("band", "bor")
            else f"l{self.operator[1:]}"
        )
        symbol = ROOT_OPERATOR_SYMBOLS.get(operator, None)
        if symbol is None:
            msg = f'Operator "{operator}" is not supported in ROOT.'
            raise ValueError(msg)
        return f"({self.left.to_numexpr()} {symbol} {self.right.to_numexpr()})"


@dataclass
class Matrix(AST):  # Matrix: A matrix call
    var: Symbol
    paren: list[AST]

    def __str__(self):
        return "{}[{}]".format(str(self.var), ",".join(str(x) for x in self.paren))

    def to_numexpr(self):
        msg = "Matrix operations are forbidden in Numexpr."
        raise ValueError(msg)

    def to_root(self):
        index = ""
        for elem in self.paren:
            index += "[" + str(elem.to_root()) + "]"
        return self.var.to_root() + index


@dataclass
class Slice(AST):  # Slice: The slice for matrix
    slices: AST

    def __str__(self):
        return f"{self.slices}"

    def to_numexpr(self):
        msg = "Matrix operations are forbidden in Numexpr."
        raise ValueError(msg)

    def to_root(self):
        return self.slices.to_root()


@dataclass
class Empty(AST):  # Slice: The slice for matrix
    def __str__(self):
        return ""

    def to_numexpr(self):
        return ""

    def to_root(self):
        return ""


@dataclass
class Call(AST):  # Call: evaluate a function on arguments
    function: str
    arguments: list[AST]

    def __str__(self):
        return f"{self.function}({', '.join(str(x) for x in self.arguments)})"

    def to_numexpr(self):
        function_str = NUMEXPR_FUNCTIONS.get(self.function, None)
        if function_str is None:
            msg = f'Function "{self.function}" is not supported in NumExpr.'
            raise ValueError(msg)
        arguments = ", ".join(arg.to_numexpr() for arg in self.arguments)
        return f"{function_str}({arguments})"

    def to_root(self):
        function_str = ROOT_FUNCTIONS.get(self.function, None)
        if function_str is None:
            msg = f'Function "{self.function}" is not supported in ROOT.'
            raise ValueError(msg)
        arguments = ", ".join(arg.to_root() for arg in self.arguments)
        return f"{function_str}({arguments})"
