import lark


expression_grammar = """
start: expression
expression: arith
arith:   term   | term "+" arith  -> add | term "-" arith      -> sub | term ">" arith -> gt | \\
term "<" arith -> lt | term "<=" arith -> lte | term ">=" arith -> gte | term "==" arith -> et \\
| term "||" arith -> bor | term "&&" arith -> band | term "&" arith -> and | term "|" arith -> or
term:    factor | factor "*" term -> mul | factor "/" term     -> div
factor:  pow  | factor  matpos* -> matr | "+" factor      -> pos | "-" factor          -> neg | pow ">>" factor -> rshift | pow "<<" factor -> lshift
pow:     atom | atom "**" factor
matpos: "[" [arith] "]"
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
    return print(parser.parse(exp).pretty())
