# Licensed under a 3-clause BSD style license, see LICENSE.
from __future__ import annotations

try:
    from lark.lexer import Token as Lark_Token
except ImportError:
    # This is a bit hacky, but we can improve it later.
    Lark_Token = type("Lark_Token", (), {})
from . import matching_tree, numexpr_parser, ttreeformula_parser


def convert_ptree(raw_ptree, standalone=True):
    if isinstance(
        raw_ptree, numexpr_parser.Token | ttreeformula_parser.Token | Lark_Token
    ):
        return

    raw_ptree.__class__ = matching_tree.ptnode

    for x in raw_ptree.children:
        convert_ptree(x, standalone)
