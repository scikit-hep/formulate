# Licensed under a 3-clause BSD style license, see LICENSE.

from abc import ABCMeta, abstractmethod
from dataclasses import dataclass
from typing import Any

from ordered_set import OrderedSet

from .identifiers import (
    CONSTANTS,
    NUMEXPR_CONSTANTS,
    NUMEXPR_FUNCTIONS,
    NUMEXPR_OPERATOR_SYMBOLS,
    PYTHON_CONSTANTS,
    PYTHON_FUNCTIONS,
    PYTHON_OPERATOR_SYMBOLS,
    ROOT_CONSTANTS,
    ROOT_FUNCTIONS,
    ROOT_OPERATOR_SYMBOLS,
)


@dataclass
class _Backend:
    name: str
    operator_symbols: dict[str, str]
    functions: dict[str, Any]
    constants: dict[str, Any]
    function_prefix: str = ""
    pow_as_operator: bool = False
    unparenthesized_ops: frozenset[str] = frozenset()
    index_format: str | None = (
        "python"  # None = forbidden, "root" = [x][y], "python" = [x,y]
    )


_NUMEXPR = _Backend(
    name="NumExpr",
    operator_symbols=NUMEXPR_OPERATOR_SYMBOLS,
    functions=NUMEXPR_FUNCTIONS,
    constants=NUMEXPR_CONSTANTS,
    pow_as_operator=True,
    index_format=None,
)

_ROOT = _Backend(
    name="ROOT",
    operator_symbols=ROOT_OPERATOR_SYMBOLS,
    functions=ROOT_FUNCTIONS,
    constants=ROOT_CONSTANTS,
    unparenthesized_ops=frozenset({":"}),
    index_format="root",
)

_PYTHON = _Backend(
    name="Python",
    operator_symbols=PYTHON_OPERATOR_SYMBOLS,
    functions=PYTHON_FUNCTIONS,
    constants=PYTHON_CONSTANTS,
    function_prefix="np.",
    unparenthesized_ops=frozenset({","}),
)


class AST(metaclass=ABCMeta):
    @abstractmethod
    def __str__(self) -> str: ...

    @abstractmethod
    def _to_backend(self, backend: _Backend) -> str: ...

    def to_numexpr(self) -> str:
        return self._to_backend(_NUMEXPR)

    def to_root(self) -> str:
        return self._to_backend(_ROOT)

    def to_python(self) -> str:
        return self._to_backend(_PYTHON)

    @property
    @abstractmethod
    def variables(self) -> OrderedSet[str]: ...

    @property
    @abstractmethod
    def named_constants(self) -> OrderedSet[str]: ...

    @property
    @abstractmethod
    def unnamed_constants(self) -> OrderedSet[str]: ...


@dataclass
class Literal(AST):  # Literal: value that appears in the program text
    value: int | float

    def __str__(self) -> str:
        return str(self.value)

    def _to_backend(self, _backend: _Backend) -> str:
        return repr(self.value)

    @property
    def variables(self) -> OrderedSet[str]:
        return OrderedSet()

    @property
    def named_constants(self) -> OrderedSet[str]:
        return OrderedSet()

    @property
    def unnamed_constants(self) -> OrderedSet[str]:
        return OrderedSet([self.value])


@dataclass
class Symbol(AST):  # Symbol: value referenced by name
    name: str

    def __str__(self) -> str:
        return self.name

    def _to_backend(self, backend: _Backend) -> str:
        if self.name in CONSTANTS:
            const = backend.constants.get(self.name)
            if const is None:
                msg = f'Constant "{self.name}" is not supported in {backend.name}.'
                raise ValueError(msg)
            return str(const)
        return self.name

    @property
    def variables(self) -> OrderedSet[str]:
        return OrderedSet() if self.name in CONSTANTS else OrderedSet([self.name])

    @property
    def named_constants(self) -> OrderedSet[str]:
        return OrderedSet() if self.name not in CONSTANTS else OrderedSet([self.name])

    @property
    def unnamed_constants(self) -> OrderedSet[str]:
        return OrderedSet()


@dataclass
class UnaryOperator(AST):  # Unary Operator: Operation with one operand
    operator: str
    operand: AST

    def __str__(self) -> str:
        return f"{self.operator}({self.operand})"

    def _to_backend(self, backend: _Backend) -> str:
        symbol = backend.operator_symbols.get(self.operator)
        if symbol is None:
            msg = f'Operator "{self.operator}" is not supported in {backend.name}.'
            raise ValueError(msg)
        return f"({symbol}{self.operand._to_backend(backend)})"

    @property
    def variables(self) -> OrderedSet[str]:
        return self.operand.variables

    @property
    def named_constants(self) -> OrderedSet[str]:
        return self.operand.named_constants

    @property
    def unnamed_constants(self) -> OrderedSet[str]:
        return self.operand.unnamed_constants


@dataclass
class BinaryOperator(AST):  # Binary Operator: Operation with two operands
    operator: str
    left: AST
    right: AST

    def __str__(self) -> str:
        return f"{self.operator}({self.left}, {self.right})"

    def _to_backend(self, backend: _Backend) -> str:
        symbol = backend.operator_symbols.get(self.operator)
        if symbol is None:
            msg = f'Operator "{self.operator}" is not supported in {backend.name}.'
            raise ValueError(msg)
        out = f"{self.left._to_backend(backend)} {symbol} {self.right._to_backend(backend)}"
        if symbol not in backend.unparenthesized_ops:
            out = f"({out})"
        return out

    @property
    def variables(self) -> OrderedSet[str]:
        return self.left.variables | self.right.variables

    @property
    def named_constants(self) -> OrderedSet[str]:
        return self.left.named_constants | self.right.named_constants

    @property
    def unnamed_constants(self) -> OrderedSet[str]:
        return self.left.unnamed_constants | self.right.unnamed_constants


@dataclass
class Matrix(AST):  # Matrix: A matrix call
    var: AST
    indices: list[AST]

    def __str__(self) -> str:
        return "{}[{}]".format(str(self.var), ", ".join(str(x) for x in self.indices))

    def _to_backend(self, backend: _Backend) -> str:
        if backend.index_format is None:
            msg = f"Matrix operations are forbidden in {backend.name}."
            raise ValueError(msg)
        var_str = self.var._to_backend(backend)
        if backend.index_format == "root":
            index = "".join(f"[{elem._to_backend(backend)}]" for elem in self.indices)
        else:
            index = (
                "["
                + ", ".join(elem._to_backend(backend) for elem in self.indices)
                + "]"
            )
        return var_str + index

    @property
    def variables(self) -> OrderedSet[str]:
        return OrderedSet.union(
            self.var.variables, *[ind.variables for ind in self.indices]
        )

    @property
    def named_constants(self) -> OrderedSet[str]:
        return OrderedSet.union(
            self.var.named_constants, *[ind.named_constants for ind in self.indices]
        )

    @property
    def unnamed_constants(self) -> OrderedSet[str]:
        return OrderedSet.union(
            self.var.unnamed_constants, *[ind.unnamed_constants for ind in self.indices]
        )


@dataclass
class Call(AST):  # Call: evaluate a function on arguments
    function: str
    arguments: list[AST]

    def __str__(self) -> str:
        return f"{self.function}({', '.join(str(x) for x in self.arguments)})"

    def _to_backend(self, backend: _Backend) -> str:
        if backend.pow_as_operator and self.function == "pow":
            return f"({self.arguments[0]._to_backend(backend)} ** {self.arguments[1]._to_backend(backend)})"
        function_str = backend.functions.get(self.function)
        if function_str is None:
            msg = f'Function "{self.function}" is not supported in {backend.name}.'
            raise ValueError(msg)
        arguments = ", ".join(arg._to_backend(backend) for arg in self.arguments)
        return f"{backend.function_prefix}{function_str}({arguments})"

    @property
    def variables(self) -> OrderedSet[str]:
        return OrderedSet.union(
            OrderedSet(), *[arg.variables for arg in self.arguments]
        )

    @property
    def named_constants(self) -> OrderedSet[str]:
        return OrderedSet.union(
            OrderedSet(), *[arg.named_constants for arg in self.arguments]
        )

    @property
    def unnamed_constants(self) -> OrderedSet[str]:
        return OrderedSet.union(
            OrderedSet(), *[arg.unnamed_constants for arg in self.arguments]
        )
