"""
Copyright (c) 2023 Aryan Roy. All rights reserved.

formulate:  Easy conversions between different styles of expressions
"""
from __future__ import annotations

import lark
from . import AST
from . import matching_tree

# from AST import Literal
# from AST import BinaryOperator
# from AST import UnaryOperator
# from AST import Call
# from AST import Symbol
# from AST import Matrix


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
}


# def toast(ptnode):
#     if ptnode.data in BINARY_OP and len(ptnode.children) == 2:
#         arguments = [toast(x) for x in ptnode.children]
#         return AST.BinaryOperator(
#             AST.Symbol(val_to_sign[str(ptnode.data)], line=arguments[0].line),
#             arguments[0],
#             arguments[1],
#         )
#     elif ptnode.data == "pow" and len(ptnode.children) == 2:
#         print("aefef")
#         arguments = [toast(ptnode.children[0]), toast(ptnode.children[1])]
#         return AST.Call(AST.Symbol("pow", line=arguments[0].line), arguments)
#     elif ptnode.data == "call" and len(ptnode.children) == 2:
#         return AST.Call(toast(ptnode.children[0]), toast(ptnode.children[1]))
#     elif ptnode.data == "symbol":
#         return AST.Symbol(str(ptnode.children[0]), line=ptnode.children[0].line)
#     elif ptnode.data == "literal":
#         return AST.Literal(float(ptnode.children[0]), line=ptnode.children[0].line)
#     elif ptnode.data == "arglist":
#         return [toast(x) for x in ptnode.children]
#     else:
#         return toast(
#             ptnode.children[0]
#         )  # many other cases, all of them simple pass-throughs


# def toast(ptnode):
#     data = ptnode.data
#     match data:
#         case "add":
#             print("efef")
#             arguments = [toast(ptnode.children[0]), toast(ptnode.children[1])]
#             return AST.BinaryOperator(
#                 AST.Symbol("+", line=arguments[0].line), arguments[0], arguments[1]
#             )

#         case "sub":
#             arguments = [toast(ptnode.children[0]), toast(ptnode.children[1])]
#             return AST.BinaryOperator(
#                 AST.Symbol("-", line=arguments[0].line), arguments[0], arguments[1]
#             )

#         case "pow" if len(ptnode.children) == 2:
#             arguments = [toast(ptnode.children[0]), toast(ptnode.children[1])]
#             return AST.BinaryOperator(
#                 AST.Symbol("**", line=arguments[0].line), arguments[0], arguments[1]
#             )

#         case "matr":
#             children = ptnode.children
#             var = toast(children[0])
#             paren = []
#             children = children[1:]
#             for elem in children:
#                 paren.append(toast(elem))
#             return AST.Matrix(var, paren)

#         case "symbol":
#             return AST.Symbol(str(ptnode.children[0]), line=ptnode.children[0].line)

#         case "literal":
#             return AST.Literal(float(ptnode.children[0]), line=ptnode.children[0].line)

#         case _:
#             return toast(ptnode.children[0])


def _get_func_names(func_names):
    children = []
    if len(func_names.children) > 1:
        children.extend(_get_func_names(func_names.children[1]))
    children.append(func_names.children[0])
    return children


def toast(ptnode):
    match ptnode:
        # case matching_tree.ptnode("add", children):
        #     print("efef")
        #     arguments = [toast(ptnode.children[0]), toast(ptnode.children[1])]
        #     return AST.BinaryOperator(
        #         AST.Symbol("+", line=arguments[0].line), arguments[0], arguments[1]
        #     )

        # case matching_tree.ptnode("sub", children):
        #     arguments = [toast(ptnode.children[0]), toast(ptnode.children[1])]
        #     return AST.BinaryOperator(
        #         AST.Symbol("-", line=arguments[0].line), arguments[0], arguments[1]
        #     )

        case matching_tree.ptnode(operator, (left, right)) if operator in BINARY_OP:
            arguments = [toast(left), toast(right)]
            return AST.BinaryOperator(
                AST.Symbol(val_to_sign[operator], line=arguments[0].line),
                arguments[0],
                arguments[1],
            )

        case matching_tree.ptnode(operator, operand) if operator in UNARY_OP:
            argument = toast(operand[0])
            return AST.UnaryOperator(
                AST.Symbol(val_to_sign[operator], line=argument.line), argument
            )

        case matching_tree.ptnode("matr", (array, *slice)):
            var = toast(array)
            paren = []
            for elem in slice:
                paren.append(toast(elem))
            return AST.Matrix(var, paren, line=var.line)

        case matching_tree.ptnode("matpos", child):
            if child[0] is None:
                return AST.Empty()
            slice = toast(child[0])
            return AST.Slice(slice, line=slice.line)

        case matching_tree.ptnode("func", (func_name, trailer)):
            func_names = _get_func_names(func_name)

            funcs = [AST.Symbol(str(elem), line=elem.line) for elem in func_names][::-1]

            func_arguments = []

            if trailer.children[0] is None:
                return AST.Call(funcs, func_arguments, line=funcs[0].line)

            func_arguments = [toast(elem) for elem in trailer.children[0].children]

            return AST.Call(funcs, func_arguments, line=funcs[0].line)

        case matching_tree.ptnode("symbol", children):
            return AST.Symbol(str(children[0]), line=children[0].column)

        case matching_tree.ptnode("literal", children):
            return AST.Literal(float(children[0]), line=children[0].column)

        case matching_tree.ptnode(_, (child,)):
            return toast(child)

        case _:
            raise TypeError(f"Unknown Node Type: {ptnode!r}.")
