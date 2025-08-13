# Licensed under a 3-clause BSD style license, see LICENSE.

from __future__ import annotations

from . import (
    AST,
    convert_ptree,
    numexpr_parser,
    toast,
    ttreeformula_parser,
)
from ._version import __version__

__all__ = ["__version__", "from_numexpr", "from_root"]


def from_root(exp: str, **kwargs) -> AST:
    """Evaluate ttreeformula expressions."""
    parser = ttreeformula_parser.Lark_StandAlone()
    ptree = parser.parse(exp)
    convert_ptree.convert_ptree(ptree)
    return toast.toast(ptree, nxp=False)


def from_numexpr(exp: str, **kwargs) -> AST:
    """Evaluate numexpr expressions."""
    parser = numexpr_parser.Lark_StandAlone()
    ptree = parser.parse(exp)
    convert_ptree.convert_ptree(ptree)
    return toast.toast(ptree, nxp=True)
