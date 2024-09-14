"""
Copyright (c) 2023 Aryan Roy. All rights reserved.

formulate:  Easy conversions between different styles of expressions
"""

from . import matching_tree
from . import numexpr_parser
from . import ttreeformula_parser

def convert_ptree(raw_ptree):

    if isinstance(raw_ptree, numexpr_parser.Token) or isinstance(raw_ptree, ttreeformula_parser.Token):
        return

    raw_ptree.__class__ = matching_tree.ptnode

    for x in raw_ptree.children:
        convert_ptree(x)

    return
