# Licensed under a 3-clause BSD style license, see LICENSE.

from abc import ABCMeta, abstractmethod
from collections.abc import Callable, Iterator, Sequence
from dataclasses import dataclass, field
from typing import Any

from ordered_set import OrderedSet

from ._traversal import fold
from .identifiers import (
    CONSTANTS,
    NUMEXPR_CONSTANTS,
    NUMEXPR_FUNCTIONS,
    NUMEXPR_OPERATOR_SYMBOLS,
    PYTHON_CONSTANTS,
    PYTHON_FUNCTIONS,
    PYTHON_OPERATOR_SYMBOLS,
    PYTHON_UNARY_FUNCTIONS,
    ROOT_CONSTANTS,
    ROOT_FUNCTIONS,
    ROOT_OPERATOR_SYMBOLS,
)


@dataclass(frozen=True, slots=True)
class _Backend:
    name: str
    operator_symbols: dict[str, str]
    functions: dict[str, Any]
    constants: dict[str, Any]
    function_prefix: str = ""
    pow_as_operator: bool = False
    unparenthesized_ops: frozenset[str] = frozenset()
    # Unary operators written as a function call instead of a symbol, mapped to
    # the function name. Takes precedence over operator_symbols.
    unary_functions: dict[str, str] = field(default_factory=dict)
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
    unary_functions=PYTHON_UNARY_FUNCTIONS,
)


class AST(metaclass=ABCMeta):
    @abstractmethod
    def _children(self) -> Sequence["AST"]: ...  # pragma: no cover

    @abstractmethod
    def _format(self, *parts: str) -> str: ...  # pragma: no cover

    @abstractmethod
    def _serializer(
        self, backend: _Backend
    ) -> Callable[..., str]: ...  # pragma: no cover

    def _walk(self) -> Iterator["AST"]:
        """Yield every node in the tree, parents first and left to right.

        Leaves therefore come out in the order they appear in the expression,
        which is the order the `variables` family reports them in.
        """
        stack: list[AST] = [self]
        while stack:
            node = stack.pop()
            yield node
            stack.extend(reversed(node._children()))

    def __str__(self) -> str:
        return fold(self, lambda node: (node._children(), node._format))

    def _to_backend(self, backend: _Backend) -> str:
        return fold(self, lambda node: (node._children(), node._serializer(backend)))

    def to_numexpr(self) -> str:
        return self._to_backend(_NUMEXPR)

    def to_root(self) -> str:
        return self._to_backend(_ROOT)

    def to_python(self) -> str:
        return self._to_backend(_PYTHON)

    @property
    def variables(self) -> OrderedSet[str]:
        return OrderedSet(
            node.name
            for node in self._walk()
            if isinstance(node, Symbol) and node.name not in CONSTANTS
        )

    @property
    def named_constants(self) -> OrderedSet[str]:
        return OrderedSet(
            node.name
            for node in self._walk()
            if isinstance(node, Symbol) and node.name in CONSTANTS
        )

    @property
    def unnamed_constants(self) -> OrderedSet[int | float]:
        return OrderedSet(
            node.value for node in self._walk() if isinstance(node, Literal)
        )


@dataclass(frozen=True, slots=True)
class Literal(AST):  # Literal: value that appears in the program text
    value: int | float

    def _children(self) -> Sequence[AST]:
        return ()

    def _format(self, *_parts: str) -> str:
        return str(self.value)

    def _serializer(self, _backend: _Backend) -> Callable[..., str]:
        text = repr(self.value)
        return lambda: text


@dataclass(frozen=True, slots=True)
class Symbol(AST):  # Symbol: value referenced by name
    name: str

    def _children(self) -> Sequence[AST]:
        return ()

    def _format(self, *_parts: str) -> str:
        return self.name

    def _serializer(self, backend: _Backend) -> Callable[..., str]:
        text = self.name
        if self.name in CONSTANTS:
            const = backend.constants.get(self.name)
            if const is None:
                msg = f'Constant "{self.name}" is not supported in {backend.name}.'
                raise ValueError(msg)
            text = str(const)
        return lambda: text


@dataclass(frozen=True, slots=True)
class UnaryOperator(AST):  # Unary Operator: Operation with one operand
    operator: str
    operand: AST

    def _children(self) -> Sequence[AST]:
        return (self.operand,)

    def _format(self, *parts: str) -> str:
        return f"{self.operator}({parts[0]})"

    def _serializer(self, backend: _Backend) -> Callable[..., str]:
        if (function := backend.unary_functions.get(self.operator)) is not None:
            name = f"{backend.function_prefix}{function}"
            return lambda operand: f"{name}({operand})"
        symbol = backend.operator_symbols.get(self.operator)
        if symbol is None:
            msg = f'Operator "{self.operator}" is not supported in {backend.name}.'
            raise ValueError(msg)
        return lambda operand: f"({symbol}{operand})"


@dataclass(frozen=True, slots=True)
class BinaryOperator(AST):  # Binary Operator: Operation with two operands
    operator: str
    left: AST
    right: AST

    def _children(self) -> Sequence[AST]:
        return (self.left, self.right)

    def _format(self, *parts: str) -> str:
        return f"{self.operator}({parts[0]}, {parts[1]})"

    def _serializer(self, backend: _Backend) -> Callable[..., str]:
        symbol = backend.operator_symbols.get(self.operator)
        if symbol is None:
            msg = f'Operator "{self.operator}" is not supported in {backend.name}.'
            raise ValueError(msg)
        parenthesize = symbol not in backend.unparenthesized_ops

        def build(left: str, right: str) -> str:
            out = f"{left} {symbol} {right}"
            return f"({out})" if parenthesize else out

        return build


@dataclass(frozen=True, slots=True)
class Matrix(AST):  # Matrix: A matrix call
    var: AST
    indices: list[AST]

    def _children(self) -> Sequence[AST]:
        return (self.var, *self.indices)

    def _format(self, *parts: str) -> str:
        var_str, *indices = parts
        return "{}[{}]".format(var_str, ", ".join(indices))

    def _serializer(self, backend: _Backend) -> Callable[..., str]:
        if backend.index_format is None:
            msg = f"Matrix operations are forbidden in {backend.name}."
            raise ValueError(msg)
        root_style = backend.index_format == "root"

        def build(var_str: str, *indices: str) -> str:
            if root_style:
                return var_str + "".join(f"[{elem}]" for elem in indices)
            return var_str + "[" + ", ".join(indices) + "]"

        return build


@dataclass(frozen=True, slots=True)
class Call(AST):  # Call: evaluate a function on arguments
    function: str
    arguments: list[AST]

    def _children(self) -> Sequence[AST]:
        return self.arguments

    def _format(self, *parts: str) -> str:
        return f"{self.function}({', '.join(parts)})"

    def _serializer(self, backend: _Backend) -> Callable[..., str]:
        if backend.pow_as_operator and self.function == "pow":
            # The backend has no pow() to fall back on: it is spelled as the
            # binary ** operator, so any other arity has nothing to render to.
            if len(self.arguments) != 2:
                msg = (
                    f'Function "pow" is written as the ** operator in '
                    f"{backend.name}, so it takes exactly two arguments, not "
                    f"{len(self.arguments)}."
                )
                raise ValueError(msg)
            return lambda base, exponent: f"({base} ** {exponent})"
        function_str = backend.functions.get(self.function)
        if function_str is None:
            msg = f'Function "{self.function}" is not supported in {backend.name}.'
            raise ValueError(msg)
        name = f"{backend.function_prefix}{function_str}"
        return lambda *args: f"{name}({', '.join(args)})"
