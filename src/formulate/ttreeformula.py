"""
Copyright (c) 2023 Aryan Roy. All rights reserved.

formulate:  Easy conversions between different styles of expressions
"""

import lark


expression_grammar = """
start: expression
expression: disjunction
disjunction: conjunction | conjunction ("|" conjunction )*
conjunction: inversion | inversion ("&" inversion )*
inversion: comparison | "~" inversion
comparison:  bitwise_or compare_op_bitwise_or_pair* | bitwise_or
compare_op_bitwise_or_pair: eq_bitwise_or | noteq_bitwise_or | lte_bitwise_or | lt_bitwise_or | gte_bitwise_or | gt_bitwise_or
eq_bitwise_or: "==" bitwise_or
noteq_bitwise_or: ("!=" ) bitwise_or
lte_bitwise_or: "<=" bitwise_or
lt_bitwise_or: "<" bitwise_or
gte_bitwise_or: ">=" bitwise_or
gt_bitwise_or: ">" bitwise_or
bitwise_or: bitwise_xor | bitwise_or "||" bitwise_xor -> bor
bitwise_xor: bitwise_and | bitwise_xor "^" bitwise_and -> bxor
bitwise_and: bitwise_inversion | bitwise_and "&&" bitwise_inversion -> band
bitwise_inversion: shift_expr | "!" bitwise_inversion -> binversion
shift_expr: sum | shift_expr "<<" sum -> lshift | shift_expr ">>" sum -> rshift
sum:   term   | term "+" sum  -> add | term "-" sum  -> sub 
term:    factor | factor "*" term -> mul | factor "/" term     -> div
factor:  pow  | factor  matpos* -> matr | "+" factor      -> pos | "-" factor          -> neg
pow:     atom | atom "**" factor
matpos: "[" [sum] "]"
atom:    "(" expression ")" | CNAME -> symbol | NUMBER -> literal  | func_name trailer  -> func
func_name: CNAME | CNAME "::" func_name
trailer: "(" [arglist] ")"
arglist: expression ("," expression)* [","]

%import common.CNAME
%import common.NUMBER
%import common.WS
%ignore WS
"""


def from_ROOT(exp: str):
    parser = lark.Lark(expression_grammar)
    print(parser.parse(exp).pretty())
    return parser.parse(exp)
