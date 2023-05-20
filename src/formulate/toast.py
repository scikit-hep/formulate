"""
Copyright (c) 2023 Aryan Roy. All rights reserved.

formulate:  Easy conversions between different styles of expressions
"""
from __future__ import annotations

import lark
from . import AST

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
#             AST.Symbol(val_to_sign[str(ptnode.data)], line=arguments[0].line), arguments[0], arguments[1]
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


def toast(ptnode):
    data = ptnode.data
    match data:
        case "add":
            arguments = [toast(ptnode.children[0]), toast(ptnode.children[1])]
            return AST.BinaryOperator(
                AST.Symbol("+", line=arguments[0].line), arguments[0], arguments[1]
            )

        case "sub":
            arguments = [toast(ptnode.children[0]), toast(ptnode.children[1])]
            return AST.BinaryOperator(
                AST.Symbol("-", line=arguments[0].line), arguments[0], arguments[1]
            )

        case "pow" if len(ptnode.children) == 2:
            arguments = [toast(ptnode.children[0]), toast(ptnode.children[1])]
            return AST.BinaryOperator(
                AST.Symbol("**", line=arguments[0].line), arguments[0], arguments[1]
            )

        case "matr":
            children = ptnode.children
            var = toast(children[0])
            paren = []
            children = children[1:]
            for elem in children:
                paren.append(toast(elem))
            return AST.Matrix(var, paren)

        case "symbol":
            return AST.Symbol(str(ptnode.children[0]), line=ptnode.children[0].line)

        case "literal":
            return AST.Literal(float(ptnode.children[0]), line=ptnode.children[0].line)

        case _:
            return toast(ptnode.children[0])
