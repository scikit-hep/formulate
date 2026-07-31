# Licensed under a 3-clause BSD style license, see LICENSE.

"""The backend-neutral expression tree and the serializers that render it.

:func:`formulate.from_root` and :func:`formulate.from_numexpr` both return an
:class:`AST`. Its node types (:class:`Literal`, :class:`Symbol`,
:class:`UnaryOperator`, :class:`BinaryOperator`, :class:`Matrix` and
:class:`Call`) are frozen dataclasses that hold *canonical* names rather than
any one language's spelling: the ROOT ``&&``, the NumExpr ``&`` and the Python
``&`` all parse to ``BinaryOperator(operator="and", ...)``.

Rendering that tree back out is the job of :meth:`AST.to_root`,
:meth:`AST.to_numexpr` and :meth:`AST.to_python`. Each looks its node up in the
tables in :mod:`formulate.identifiers`; a name that is missing from a table is
how "this construct has no faithful equivalent here" is expressed, and raises
``ValueError`` rather than emitting something subtly different.
"""

import re
from abc import ABCMeta, abstractmethod
from collections.abc import Callable, Iterator, Sequence
from dataclasses import dataclass, field
from typing import Any

from ordered_set import OrderedSet

from ._traversal import fold
from .identifiers import (
    CONSTANTS,
    FUNCTION_DISPLAY_NAMES,
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
    # Whether a name this backend cannot spell is hex-encoded rather than
    # emitted as written. See `_encode_name`.
    encode_invalid_names: bool = False


_NUMEXPR = _Backend(
    name="NumExpr",
    operator_symbols=NUMEXPR_OPERATOR_SYMBOLS,
    functions=NUMEXPR_FUNCTIONS,
    constants=NUMEXPR_CONSTANTS,
    pow_as_operator=True,
    index_format=None,
    encode_invalid_names=True,
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


# ROOT branch names are not always identifiers -- `branch.leaf` is one name with
# a dot in it, not an attribute access -- but NumExpr rejects any expression
# containing one ("forbidden control characters") and has no quoting syntax to
# get around it. Uproot has the same problem with C++ classnames and solves it
# by hex-encoding, so formulate spells names the same way uproot does: a run of
# characters that cannot appear in an identifier becomes those bytes in hex,
# wrapped in underscores, making `branch.leaf` into `branch_2e_leaf`.
#
# A dot is the only such character that can reach here: `toast` requires every
# dot-separated part of a symbol to be a Python identifier, so anything else is
# a parse error long before this. The pattern is still uproot's, so that names
# encode identically in both packages, which also means underscores are part of
# a run: `a.b_c` encodes to `a_2e_b_5f_c` rather than to an `a_2e_b_c` that a
# branch really called `a_2e_b_c` would collide with.
_ENCODE_RUN = re.compile(r"[^A-Za-z0-9]+")


def _encode_name(name: str) -> str:
    """Hex-encode the parts of `name` that cannot appear in an identifier."""
    return _ENCODE_RUN.sub(lambda run: f"_{run.group().encode().hex()}_", name)


class AST(metaclass=ABCMeta):
    """Base class of every expression node.

    Instances are produced by :func:`formulate.from_root` and
    :func:`formulate.from_numexpr`, not constructed directly, and are immutable
    and hashable: converting an expression never modifies it, so one parsed
    expression can be rendered to as many backends as needed.

    ``str(node)`` gives a language-independent view of the tree in canonical
    names (``add(x, pow(y, 2))``), which is useful when debugging a conversion;
    use the ``to_*`` methods to get something an engine will accept.
    """

    # The node types are all slotted dataclasses, but a slotted class inheriting
    # from an unslotted one still gets a __dict__, which would undo that for
    # every node in the tree.
    __slots__ = ()

    @abstractmethod
    def _children(self) -> Sequence["AST"]: ...  # pragma: no cover

    @abstractmethod
    def _key(self) -> tuple[Any, ...]: ...  # pragma: no cover

    @abstractmethod
    def _format(self, *parts: str) -> str: ...  # pragma: no cover

    @abstractmethod
    def _serializer(
        self, backend: _Backend
    ) -> Callable[..., str]: ...  # pragma: no cover

    def __eq__(self, other: object) -> bool:
        """Compare two trees structurally, without recursing.

        The dataclass-generated ``__eq__`` compares field tuples, and a field
        holding a child node makes that a recursive descent -- which blows the
        interpreter stack on trees the rest of this class handles fine.
        """
        if self is other:
            return True
        if not isinstance(other, AST):
            return NotImplemented
        stack: list[tuple[AST, AST]] = [(self, other)]
        while stack:
            left, right = stack.pop()
            if left is right:
                continue
            if type(left) is not type(right) or left._key() != right._key():
                return False
            left_children, right_children = left._children(), right._children()
            if len(left_children) != len(right_children):
                return False
            # Lengths were just checked, so strict= can never trip here; it is
            # there to keep that a stated invariant rather than a silent one.
            stack.extend(zip(left_children, right_children, strict=True))
        return True

    def __hash__(self) -> int:
        """Hash the tree bottom-up, for the same reason ``__eq__`` is iterative.

        Equal trees have equal types, keys and child structure, so they hash
        alike.
        """
        return fold(
            self,
            lambda node: (
                node._children(),
                lambda *children: hash((type(node), node._key(), children)),
            ),
        )

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
        """Render the expression as NumExpr source.

        Named constants have no NumExpr spelling and are substituted by their
        numeric value, so ``pi`` comes back as ``3.141592653589793``.

        :raises ValueError: if the expression uses a construct NumExpr has no
            equivalent for, such as array indexing, ``inf``, or the
            element-wise ``TMath::Min``/``TMath::Max``.

        .. code-block:: pycon

            >>> import formulate
            >>> formulate.from_root("TMath::Sqrt(x**2 + y**2)").to_numexpr()
            'sqrt(((x ** 2) + (y ** 2)))'
        """
        return self._to_backend(_NUMEXPR)

    def to_root(self) -> str:
        """Render the expression as a ROOT ``TTreeFormula`` string.

        :raises ValueError: if the expression uses a construct ROOT has no
            equivalent for, such as ``^`` used as XOR or NumExpr's ``where``.

        .. code-block:: pycon

            >>> import formulate
            >>> formulate.from_numexpr("sqrt(x**2 + y**2)").to_root()
            'TMath::Sqrt(((x ** 2) + (y ** 2)))'
        """
        return self._to_backend(_ROOT)

    def to_python(self) -> str:
        """Render the expression as plain Python, using NumPy for functions.

        Function and constant names are emitted with an ``np.`` prefix, so the
        result is meant to be evaluated somewhere NumPy is imported as ``np``.
        This backend is output-only: there is no ``from_python``.

        :raises ValueError: if the expression uses a construct with no NumPy
            equivalent that can be written as a single name, such as NumExpr's
            ``contains``.

        .. code-block:: pycon

            >>> import formulate
            >>> formulate.from_root("TMath::Sqrt(x**2 + y**2)").to_python()
            'np.sqrt(((x ** 2) + (y ** 2)))'
        """
        return self._to_backend(_PYTHON)

    @property
    def variables(self) -> OrderedSet[str]:
        """The names the expression reads, in order of first appearance.

        Named constants are excluded; see :attr:`named_constants`. For a
        ``TTree`` expression this is the set of branches that have to be read.

        .. code-block:: pycon

            >>> import formulate
            >>> list(formulate.from_root("x + TMath::Pi() * y").variables)
            ['x', 'y']
        """
        return OrderedSet(
            node.name
            for node in self._walk()
            if isinstance(node, Symbol) and node.name not in CONSTANTS
        )

    @property
    def named_constants(self) -> OrderedSet[str]:
        """The constants the expression names, in order of first appearance.

        Names are canonical rather than as written, so both ``TMath::E()`` and
        ``e_num`` report as ``exp1``.

        .. code-block:: pycon

            >>> import formulate
            >>> list(formulate.from_root("x + TMath::Pi() * y").named_constants)
            ['pi']
        """
        return OrderedSet(
            node.name
            for node in self._walk()
            if isinstance(node, Symbol) and node.name in CONSTANTS
        )

    @property
    def unnamed_constants(self) -> OrderedSet[int | float]:
        """The numeric literals in the expression, in order of first appearance.

        .. code-block:: pycon

            >>> import formulate
            >>> list(formulate.from_root("2 * x + 1.5").unnamed_constants)
            [2, 1.5]
        """
        return OrderedSet(
            node.value for node in self._walk() if isinstance(node, Literal)
        )


@dataclass(frozen=True, slots=True, eq=False)
class Literal(AST):
    """A number written out in the expression text, such as ``2`` or ``1.5``."""

    value: int | float

    def _children(self) -> Sequence[AST]:
        return ()

    def _key(self) -> tuple[Any, ...]:
        return (self.value,)

    def _format(self, *_parts: str) -> str:
        return str(self.value)

    def _serializer(self, _backend: _Backend) -> Callable[..., str]:
        text = repr(self.value)
        return lambda: text


@dataclass(frozen=True, slots=True, eq=False)
class Symbol(AST):
    """A value referred to by name: a variable, or a named constant.

    Constants are held under their canonical name (``pi``, ``exp1``) and are
    exactly those names that appear in
    :data:`formulate.identifiers.CONSTANTS`; every other name is a variable.
    """

    name: str

    def _children(self) -> Sequence[AST]:
        return ()

    def _key(self) -> tuple[Any, ...]:
        return (self.name,)

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
            if isinstance(const, (bool, int, float)) and const < 0:
                # A bare negative number is not an atom: ** binds tighter than
                # unary minus, so the sign would escape the exponent and
                # ``eminus ** 2`` would come out negative.
                text = f"({text})"
        elif backend.encode_invalid_names and "." in self.name:
            text = _encode_name(self.name)
        return lambda: text


@dataclass(frozen=True, slots=True, eq=False)
class UnaryOperator(AST):
    """An operation with a single operand.

    ``operator`` is one of the canonical names in
    :data:`formulate.identifiers.UNARY_OPERATORS`: ``"pos"``, ``"neg"``, or
    ``"inv"`` for the logical NOT written ``!`` in ROOT and ``~`` in NumExpr.
    """

    operator: str
    operand: AST

    def _children(self) -> Sequence[AST]:
        return (self.operand,)

    def _key(self) -> tuple[Any, ...]:
        return (self.operator,)

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


@dataclass(frozen=True, slots=True, eq=False)
class BinaryOperator(AST):
    """An operation with two operands.

    ``operator`` is one of the canonical names in
    :data:`formulate.identifiers.BINARY_OPERATORS` — ``"add"``, ``"lt"``,
    ``"and"`` and so on — never a backend's spelling of it.
    """

    operator: str
    left: AST
    right: AST

    def _children(self) -> Sequence[AST]:
        return (self.left, self.right)

    def _key(self) -> tuple[Any, ...]:
        return (self.operator,)

    def _format(self, *parts: str) -> str:
        return f"{self.operator}({parts[0]}, {parts[1]})"

    def _serializer(self, backend: _Backend) -> Callable[..., str]:
        symbol = backend.operator_symbols.get(self.operator)
        if symbol is None:
            msg = f'Operator "{self.operator}" is not supported in {backend.name}.'
            raise ValueError(msg)
        # A comma is punctuation rather than an operator: it hugs the operand on
        # its left, so it renders as ``x, y`` and not as ``x , y``.
        separator = f"{symbol} " if symbol == "," else f" {symbol} "
        if symbol in backend.unparenthesized_ops:
            return lambda left, right: f"{left}{separator}{right}"
        return lambda left, right: f"({left}{separator}{right})"


@dataclass(frozen=True, slots=True, eq=False)
class Matrix(AST):
    """An indexed access, ``var[i]`` or ``var[i][j]``.

    ROOT writes one bracket pair per index and Python writes a single
    comma-separated one, so the same node renders as ``arr[1][2]`` for ROOT and
    ``arr[1, 2]`` for Python. NumExpr has no indexing at all and rejects it.
    """

    var: AST
    indices: tuple[AST, ...]

    def _children(self) -> Sequence[AST]:
        return (self.var, *self.indices)

    def _key(self) -> tuple[Any, ...]:
        return ()

    def _format(self, *parts: str) -> str:
        var_str, *indices = parts
        return f"{var_str}[{', '.join(indices)}]"

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


@dataclass(frozen=True, slots=True, eq=False)
class Call(AST):
    """A function applied to zero or more arguments.

    ``function`` is a canonical name from
    :data:`formulate.identifiers.FUNCTIONS`, which is what makes
    ``TMath::ATan2``, ``atan2`` and ``arctan2`` the same node.
    """

    function: str
    arguments: tuple[AST, ...]

    def _children(self) -> Sequence[AST]:
        return self.arguments

    def _key(self) -> tuple[Any, ...]:
        return (self.function,)

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
            display = FUNCTION_DISPLAY_NAMES.get(self.function, self.function)
            msg = f'Function "{display}" is not supported in {backend.name}.'
            raise ValueError(msg)
        name = f"{backend.function_prefix}{function_str}"
        return lambda *args: f"{name}({', '.join(args)})"
