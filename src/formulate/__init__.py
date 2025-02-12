# Licensed under a 3-clause BSD style license, see LICENSE.

from __future__ import annotations

from . import ttreeformula_parser, numexpr_parser  # noqa  # noqa

from . import convert_ptree

from . import AST

from . import toast

from ._version import __version__


def from_root(exp : str, **kwargs) -> AST :
    """Evaluate ttreformula expressions."""
    parser = ttreeformula_parser.Lark_StandAlone()
    ptree = parser.parse(exp)
    convert_ptree.convert_ptree(ptree)
    return toast.toast(ptree, nxp=False)

def from_numexpr(exp : str, **kwargs) -> AST :
    """Evaluate numexpr expressions."""
    parser = numexpr_parser.Lark_StandAlone()
    ptree = parser.parse(exp)
    convert_ptree.convert_ptree(ptree)
    return toast.toast(ptree, nxp=True)
