# Licensed under a 3-clause BSD style license, see LICENSE.

"""Conversion of a lark parse tree into the backend-neutral AST.

This is where a language's surface syntax stops mattering: namespaces
(``TMath::``), the trailing ``$`` on ROOT's array functions, and the function
and constant aliases are all resolved here, so what comes out is written purely
in the canonical names of :mod:`formulate.identifiers`. A name that resolves to
nothing raises here rather than later.
"""

import functools
from ast import literal_eval
from collections.abc import Callable, Sequence
from keyword import iskeyword
from typing import Any

import lark

from . import AST
from ._traversal import fold
from .identifiers import (
    BINARY_OPERATORS,
    CONSTANTS,
    CONSTANTS_ALIASES,
    CONSTANTS_FUNCTION_ALIASES,
    FUNCTION_ALIASES,
    FUNCTIONS,
    NAMESPACES,
    UNARY_OPERATORS,
)


def _get_var_name(node: lark.Tree | lark.Token) -> str:
    while isinstance(node, lark.Tree):
        node = node.children[0]
    var_name = str(node)
    return CONSTANTS_ALIASES.get(var_name, var_name)


def _get_raw_function_name(node: lark.Tree) -> list[str]:
    parts = []
    while True:
        parts.append(str(node.children[0]))
        if len(node.children) == 1:
            break
        node = node.children[1]
    return parts


def _get_function_name(node: lark.Tree) -> str:
    pieces = []
    for part in _get_raw_function_name(node):
        pieces.extend(part.replace(".", "::").split("::"))
    if len(pieces) == 1:
        name = pieces[0]
    elif len(pieces) == 2:
        namespace = pieces[0].lower()
        if namespace not in NAMESPACES:
            msg = f'Unknown namespace "{pieces[0]}"'
            raise ValueError(msg)
        # Build a namespace-qualified identifier for functions that have both
        # a namespaced scalar form (TMath::Min) and a bare array form (Min$).
        func_lower = pieces[1].lower().removesuffix("$")
        qualified = f"{namespace}_{func_lower}"
        if qualified in FUNCTIONS:
            return qualified
        name = pieces[1]
    else:
        full_name = "::".join(pieces)
        msg = f'Unknown function or constant "{full_name}"'
        raise ValueError(msg)
    # Now we normalize the name and make sure it is supported
    name = name.lower().removesuffix("$")  # strip $ from ROOT keywords
    name = FUNCTION_ALIASES.get(name, name)
    name = CONSTANTS_FUNCTION_ALIASES.get(name, name)
    name = CONSTANTS_ALIASES.get(name, name)
    if name not in FUNCTIONS and name not in CONSTANTS:
        msg = f'Unknown function or constant "{name}"'
        raise ValueError(msg)
    return name


def _constant(node: AST.AST) -> Callable[[], AST.AST]:
    """Builder for a parse-tree node that needs no children converted."""
    return lambda: node


def _expand(ptnode: lark.Tree) -> tuple[Sequence[Any], Callable[..., AST.AST]]:
    """Decompose one parse-tree node for `fold`.

    Returns the child parse-tree nodes that still need converting, together
    with a builder that assembles the AST node once they have been converted.
    Anything that does not depend on the children — name resolution and the
    errors it raises — happens here, before they are visited.
    """
    match ptnode:
        case lark.Tree(operator, (left, right)) if operator in BINARY_OPERATORS:
            return (left, right), functools.partial(AST.BinaryOperator, operator)

        case lark.Tree(operator, operand) if operator in UNARY_OPERATORS:
            return (operand[0],), functools.partial(AST.UnaryOperator, operator)

        case lark.Tree("matr", (array, *indices)):
            children = [array, *(elem.children[0] for elem in indices)]
            return children, lambda mat, *ind: AST.Matrix(mat, ind)

        case lark.Tree("func", (func_name, trailer)):
            func_name = _get_function_name(func_name)

            # In case the function is actually a constant
            if func_name in CONSTANTS:
                if (
                    trailer.children[0] is not None
                    and len(trailer.children[0].children) != 0
                ):
                    msg = f'The constant "{func_name}" should not have arguments.'
                    raise SyntaxError(msg)
                return (), _constant(AST.Symbol(func_name))

            arg_list = trailer.children[0]
            arguments = () if arg_list is None else tuple(arg_list.children)
            return arguments, lambda *args: AST.Call(func_name, args)

        case lark.Tree("symbol", children):
            var_name = _get_var_name(children[0])
            if var_name in ("True", "False"):
                var_name = var_name.lower()  # This makes it not a keyword
            # Bare ROOT $ functions (e.g. Length$, Sum$) used without parens
            if var_name.endswith("$"):
                func_name = var_name.removesuffix("$").lower()
                if func_name in FUNCTIONS:
                    return (), _constant(AST.Call(func_name, ()))
            if any(
                not part.isidentifier() or iskeyword(part)
                for part in var_name.split(".")
            ):
                msg = f'The symbol "{var_name}" is not a valid symbol.'
                raise SyntaxError(msg)
            return (), _constant(AST.Symbol(var_name))

        case lark.Tree("literal", children):
            return (), _constant(AST.Literal(literal_eval(children[0])))

        case lark.Tree(_, (child,)):
            return (child,), lambda child_exp: child_exp

        case _:  # pragma: no cover
            msg = f'Unknown Node Type: "{ptnode!r}".'
            raise TypeError(msg)


def toast(ptnode: lark.Tree) -> AST.AST:
    """Convert a lark parse tree into the backend-neutral AST."""
    return fold(ptnode, _expand)
