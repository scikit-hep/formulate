# Licensed under a 3-clause BSD style license, see LICENSE.

from . import numexpr_parser
from . import ttreeformula_parser


class ptnode(numexpr_parser.Tree, ttreeformula_parser.Tree):
    __match_args__ = ("data", "children")
