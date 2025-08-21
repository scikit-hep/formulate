# Licensed under a 3-clause BSD style license, see LICENSE.

from __future__ import annotations

from abc import ABCMeta, abstractmethod
from dataclasses import dataclass

from .identifiers import (
    CONSTANTS,
    NUMEXPR_FUNCTIONS,
    NUMEXPR_OPERATOR_SYMBOLS,
    ROOT_FUNCTIONS,
    ROOT_OPERATOR_SYMBOLS,
)


class AST(metaclass=ABCMeta):
    @abstractmethod
    def __str__(self) -> str:
        msg = "__str__() not implemented, subclass must implement it"
        raise NotImplementedError(msg)

    @abstractmethod
    def to_numexpr(self) -> str:
        msg = "to_numexpr() not implemented, subclass must implement it"
        raise NotImplementedError(msg)

    @abstractmethod
    def to_root(self) -> str:
        msg = "to_root() not implemented, subclass must implement it"
        raise NotImplementedError(msg)

    # TODO: is it worth having a to_python() method?
    def to_python(self) -> str:
        return self.to_numexpr()

    @property
    @abstractmethod
    def variables(self) -> frozenset[str]:
        msg = "variables() not implemented, subclass must implement it"
        raise NotImplementedError(msg)


@dataclass
class Literal(AST):  # Literal: value that appears in the program text
    value: int | float

    def __str__(self) -> str:
        return str(self.value)

    def to_numexpr(self) -> str:
        return repr(self.value)

    def to_root(self) -> str:
        return repr(self.value)

    @property
    def variables(self) -> frozenset[str]:
        return frozenset()


@dataclass
class Symbol(AST):  # Symbol: value referenced by name
    name: str

    def __str__(self) -> str:
        return self.name

    def to_numexpr(self) -> str:
        return self.name

    def to_root(self) -> str:
        return self.name

    @property
    def variables(self) -> frozenset[str]:
        return frozenset() if self.name in CONSTANTS else frozenset((self.name,))


@dataclass
class UnaryOperator(AST):  # Unary Operator: Operation with one operand
    operator: str
    operand: AST

    def __str__(self) -> str:
        return f"{self.operator}({self.operand})"

    def to_numexpr(self) -> str:
        symbol = NUMEXPR_OPERATOR_SYMBOLS.get(self.operator, None)
        if symbol is None:
            msg = f'Operator "{self.operator}" is not supported in NumExpr.'
            raise ValueError(msg)
        return f"({symbol}{self.operand.to_numexpr()})"

    def to_root(self) -> str:
        symbol = ROOT_OPERATOR_SYMBOLS.get(self.operator, None)
        if symbol is None:
            msg = f'Operator "{self.operator}" is not supported in ROOT.'
            raise ValueError(msg)
        return f"({symbol}{self.operand.to_root()})"

    @property
    def variables(self) -> frozenset[str]:
        return self.operand.variables


@dataclass
class BinaryOperator(AST):  # Binary Operator: Operation with two operands
    operator: str
    left: AST
    right: AST

    def __str__(self) -> str:
        return f"{self.operator}({self.left}, {self.right})"

    def to_numexpr(self) -> str:
        symbol = NUMEXPR_OPERATOR_SYMBOLS.get(self.operator, None)
        if symbol is None:
            msg = f'Operator "{self.operator}" is not supported in NumExpr.'
            raise ValueError(msg)
        return f"({self.left.to_numexpr()} {symbol} {self.right.to_numexpr()})"

    def to_root(self) -> str:
        symbol = ROOT_OPERATOR_SYMBOLS.get(self.operator, None)
        if symbol is None:
            msg = f'Operator "{self.operator}" is not supported in ROOT.'
            raise ValueError(msg)
        return f"({self.left.to_root()} {symbol} {self.right.to_root()})"

    @property
    def variables(self) -> frozenset[str]:
        return self.left.variables | self.right.variables


@dataclass
class Matrix(AST):  # Matrix: A matrix call
    var: Symbol
    paren: list[AST]

    def __str__(self) -> str:
        return "{}[{}]".format(str(self.var), ",".join(str(x) for x in self.paren))

    def to_numexpr(self) -> str:
        msg = "Matrix operations are forbidden in Numexpr."
        raise ValueError(msg)

    def to_root(self) -> str:
        index = ""
        for elem in self.paren:
            index += "[" + str(elem.to_root()) + "]"
        return self.var.to_root() + index

    @property
    def variables(self) -> frozenset[str]:
        return frozenset()


@dataclass
class Slice(AST):  # Slice: The slice for matrix
    slices: AST

    def __str__(self) -> str:
        return f"{self.slices}"

    def to_numexpr(self) -> str:
        msg = "Matrix operations are forbidden in Numexpr."
        raise ValueError(msg)

    def to_root(self) -> str:
        return self.slices.to_root()

    @property
    def variables(self) -> frozenset[str]:
        return frozenset()


@dataclass
class Empty(AST):  # Slice: The slice for matrix
    def __str__(self) -> str:
        return ""

    def to_numexpr(self) -> str:
        return ""

    def to_root(self) -> str:
        return ""

    @property
    def variables(self) -> frozenset[str]:
        return frozenset()


@dataclass
class Call(AST):  # Call: evaluate a function on arguments
    function: str
    arguments: list[AST]

    def __str__(self) -> str:
        return f"{self.function}({', '.join(str(x) for x in self.arguments)})"

    def to_numexpr(self) -> str:
        function_str = NUMEXPR_FUNCTIONS.get(self.function, None)
        if function_str is None:
            msg = f'Function "{self.function}" is not supported in NumExpr.'
            raise ValueError(msg)
        arguments = ", ".join(arg.to_numexpr() for arg in self.arguments)
        return f"{function_str}({arguments})"

    def to_root(self) -> str:
        function_str = ROOT_FUNCTIONS.get(self.function, None)
        if function_str is None:
            msg = f'Function "{self.function}" is not supported in ROOT.'
            raise ValueError(msg)
        arguments = ", ".join(arg.to_root() for arg in self.arguments)
        return f"{function_str}({arguments})"

    @property
    def variables(self) -> frozenset[str]:
        return frozenset.union(*[arg.variables for arg in self.arguments])
