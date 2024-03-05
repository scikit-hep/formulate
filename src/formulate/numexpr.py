"""
Copyright (c) 2023 Aryan Roy. All rights reserved.

formulate:  Easy conversions between different styles of expressions
"""
from __future__ import annotations

import lark

from . import matching_tree

expression_grammar = r'''
start: disjunction
disjunction: conjunction | conjunction "||" conjunction -> lor
conjunction: inversion | inversion "&&" inversion -> land
inversion: comparison | "!" inversion -> linv
comparison: bitwise_or | comparison ">" bitwise_or -> gt
            | comparison ">=" bitwise_or -> gte
            | comparison "<" bitwise_or -> lt
            | comparison "<=" bitwise_or -> lte
            | comparison ("!=" ) bitwise_or -> neq
            | comparison "==" bitwise_or -> eq
bitwise_or: bitwise_xor | bitwise_or "|" bitwise_xor -> bor
bitwise_xor: bitwise_and | bitwise_xor "^" bitwise_and -> bxor
bitwise_and: bitwise_inversion
            | bitwise_and "&" bitwise_inversion -> band
bitwise_inversion: shift_expr | "~" bitwise_inversion -> binv
shift_expr: sum | shift_expr "<<" sum -> lshift | shift_expr ">>" sum -> rshift
sum:   term   | term "+" sum  -> add | term "-" sum  -> sub
term:    factor | factor "*" term -> mul
                | factor "/" term     -> div
                | factor "%" term -> mod
factor:  pow  | factor  matpos+ -> matr
                | "+" factor  -> pos
                | "-" factor          -> neg
pow:     CNAME | CNAME "**" factor -> pow
matpos: "[" [sum] "]"
%import common.CNAME
%import common.NUMBER
%import common.WS
%ignore WS
'''


def exp_to_ptree(exp: str):
    parser = lark.Lark(
        expression_grammar, parser="lalr", tree_class=matching_tree.ptnode
    )
    print(parser.parse(exp).pretty())
    return parser.parse(exp)