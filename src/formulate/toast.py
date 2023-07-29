"""
Copyright (c) 2023 Aryan Roy. All rights reserved.

formulate:  Easy conversions between different styles of expressions
"""
from __future__ import annotations

from . import AST, matching_tree


UNARY_OP = {"pos", "neg", "binv", "linv"}
with_sign = {}
BINARY_OP = {
    "add",
    "sub",
    "div",
    "mul",
    "lt",
    "gt",
    "lte",
    "gte",
    "eq",
    "neq",
    "band",
    "bor",
    "bxor",
    "linv",
    "land",
    "lor",
    "pow",
    "mod",
}
val_to_sign = {
    "add": "+",
    "sub": "-",
    "div": "/",
    "mul": "*",
    "lt": "<",
    "gt": ">",
    "lte": "<=",
    "gte": ">=",
    "eq": "==",
    "neq": "!=",
    "band": "&",
    "bor": "|",
    "bxor": "^",
    "linv": "!",
    "land": "&&",
    "lor": "||",
    "neg": "-",
    "pos": "+",
    "binv": "~",
    "linv": "!",
    "pow": "**",
    "mod": "%",
    "multi_out": ":",
}

FUNC_MAPPING = {
    "MATH::PI": "pi",
    "LENGTH$": "no_of_entries",
    "ITERATION$": "current_iteration",
    "SUM$": "sum",
    "MIN$": "min",
    "MAX$": "max",
    "MINIF$": "min_if",
    "MAXIF$": "max_if",
    "ALT$": "alternate",
}


def _get_func_names(func_names):
    children = []
    if len(func_names.children) > 1:
        children.extend(_get_func_names(func_names.children[1]))
    children.append(func_names.children[0])
    return children


def toast(ptnode: matching_tree.ptnode):
    match ptnode:
        case matching_tree.ptnode(operator, (left, right)) if operator in BINARY_OP:
            arguments = [toast(left), toast(right)]
            return AST.BinaryOperator(
                AST.Symbol(val_to_sign[operator], index=arguments[1].index),
                arguments[0],
                arguments[1],
                index=arguments[0].index,
            )

        case matching_tree.ptnode(operator, operand) if operator in UNARY_OP:
            argument = toast(operand[0])
            return AST.UnaryOperator(
                AST.Symbol(val_to_sign[operator], index=argument.index), argument
            )

        case matching_tree.ptnode("multi_out", (out1, out2)):
            var1 = toast(out1)
            var2 = toast(out2)
            args = [var1, var2]
            return AST.Call(val_to_sign["multi_out"], args, index=var1.index)

        case matching_tree.ptnode("matr", (array, *slice)):
            var = toast(array)
            paren = [toast(elem) for elem in slice]
            return AST.Matrix(var, paren, index=var.index)

        case matching_tree.ptnode("matpos", child):
            if child[0] is None:
                return AST.Empty()
            slice = toast(child[0])
            return AST.Slice(slice, index=slice.index)

        case matching_tree.ptnode("func", (func_name, trailer)):
            func_names = _get_func_names(func_name)[::-1]
            func_arguments = []

            try:
                fname = FUNC_MAPPING["::".join(func_names).upper()]
            except KeyError:
                fname = "::".join(func_names)

            if trailer.children[0] is None:
                return AST.Call(
                    fname,
                    func_arguments,
                    index=func_names[0].start_pos,
                )

            func_arguments = [toast(elem) for elem in trailer.children[0].children]

            funcs = root_to_common(func_names, func_names[0].start_pos)

            return AST.Call(funcs, func_arguments, index=func_names[0].start_pos)

        case matching_tree.ptnode("symbol", children):
            return AST.Symbol(str(children[0]), index=children[0].start_pos)

        case matching_tree.ptnode("literal", children):
            return AST.Literal(float(children[0]), index=children[0].start_pos)

        case matching_tree.ptnode(_, (child,)):
            return toast(child)

        case _:
            raise TypeError(f"Unknown Node Type: {ptnode!r}.")


def root_to_common(funcs: list, index: int):
    str_funcs = [str(elem) for elem in funcs]

    try:
        string_rep = FUNC_MAPPING["::".join(str_funcs).upper()]
    except KeyError:
        string_rep = "::".join(str_funcs)

    return AST.Symbol(string_rep, index=index)
