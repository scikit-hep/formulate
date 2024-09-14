"""
Copyright (c) 2023 Aryan Roy. All rights reserved.

formulate:  Easy conversions between different styles of expressions
"""


from . import numexpr_parser
from . import ttreeformula_parser


class ptnode(numexpr_parser.Tree, ttreeformula_parser.Tree):
    __match_args__ = ("data", "children")
