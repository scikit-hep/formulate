# Licensed under a 3-clause BSD style license, see LICENSE.

from __future__ import annotations

import typing
from ast import literal_eval
from keyword import iskeyword

import lark

from . import AST
from .identifiers import (
    BINARY_OPERATORS,
    CONSTANTS,
    FUNCTION_ALIASES,
    FUNCTIONS,
    NAMESPACES,
    UNARY_OPERATORS,
)


# TODO: This might drop important information
def _get_var_name(node: lark.Tree | lark.Token) -> str:
    if isinstance(node, lark.Tree):
        return _get_var_name(node.children[0])
    return str(node)


def _get_raw_function_name(func_names: lark.Tree, invert: bool = True) -> list[str]:
    children = []
    if len(func_names.children) > 1:
        children.extend(_get_raw_function_name(func_names.children[1], False))
    children.append(func_names.children[0])
    if invert:
        children.reverse()
    return children


def _get_function_name(node: lark.Tree) -> str:
    raw_name = _get_raw_function_name(node)
    full_name = "::".join(raw_name)
    pieces = full_name.replace(".", "::").split("::")
    if len(pieces) == 1:
        name = pieces[0]
    elif len(pieces) == 2:
        if pieces[0].lower() not in NAMESPACES:
            msg = f'Unknown namespace "{pieces[0]}"'
            raise ValueError(msg)
        name = pieces[1]
    else:
        msg = f'Unknown function "{pieces[0]}"'
        raise ValueError(msg)
    # Now we normalize the name and make sure it is supported
    name = name.lower()
    name = FUNCTION_ALIASES.get(name, name)
    if name not in FUNCTIONS and name not in CONSTANTS:
        msg = f'Unknown function or constant "{name}"'
        raise ValueError(msg)
    return name


@typing.no_type_check  # TODO: Figure out how to make mypy happy
def toast(ptnode: lark.Tree) -> AST.AST:
    match ptnode:
        case lark.Tree(operator, (left, right)) if operator in BINARY_OPERATORS:
            left_exp, right_exp = toast(left), toast(right)
            return AST.BinaryOperator(
                operator,
                left_exp,
                right_exp,
            )

        case lark.Tree(operator, operand) if operator in UNARY_OPERATORS:
            argument = toast(operand[0])
            return AST.UnaryOperator(operator, argument)

        case lark.Tree("matr", (array, *indices)):
            mat = toast(array)
            ind = [toast(elem.children[0]) for elem in indices]
            return AST.Matrix(mat, ind)

        case lark.Tree("func", (func_name, trailer)):
            func_name = _get_function_name(func_name)

            if func_name in CONSTANTS:
                if (
                    trailer.children[0] is not None
                    and len(trailer.children[0].children) != 0
                ):
                    msg = f'The constant "{func_name}" should not have arguments.'
                    raise SyntaxError(msg)
                return AST.Symbol(func_name)

            func_arguments = [toast(elem) for elem in trailer.children[0].children]
            return AST.Call(func_name, func_arguments)

        case lark.Tree("symbol", children):
            var_name = _get_var_name(children[0])
            # Strip $ from ROOT keywords
            if var_name.endswith("$"):
                var_name = var_name[:-1]
            if not var_name.isidentifier() or iskeyword(var_name):
                msg = f'The symbol "{var_name}" is not a valid symbol.'
                raise SyntaxError(msg)
            return AST.Symbol(var_name)

        case lark.Tree("literal", children):
            return AST.Literal(literal_eval(children[0]))

        case lark.Tree(_, (child,)):
            return toast(child)

        case _:
            msg = f'Unknown Node Type: "{ptnode!r}".'
            raise TypeError(msg)
