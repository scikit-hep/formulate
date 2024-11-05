# Licensed under a 3-clause BSD style license, see LICENSE.

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
