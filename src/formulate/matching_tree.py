# Licensed under a 3-clause BSD style license, see LICENSE.
from __future__ import annotations

from . import numexpr_parser, root_parser


class ptnode(numexpr_parser.Tree, root_parser.Tree):
    __match_args__ = ("data", "children")
