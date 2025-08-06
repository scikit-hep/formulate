# Licensed under a 3-clause BSD style license, see LICENSE.
from __future__ import annotations

try:
    from lark.tree import Tree as Lark_Tree
except ImportError:
    # This is a bit hacky, but we can improve it later.
    Lark_Tree = type("Lark_Tree", (), {})
from . import numexpr_parser, ttreeformula_parser


class ptnode(numexpr_parser.Tree, ttreeformula_parser.Tree, Lark_Tree):
    __match_args__ = ("data", "children")
