"""
Copyright (c) 2023 Aryan Roy. All rights reserved.

formulate:  Easy conversions between different styles of expressions
"""

from __future__ import annotations

from . import ttreeformula_parser, numexpr_parser  # noqa  # noqa

from . import convert_ptree

from . import AST

from . import toast

from ._version import __version__

# print("======================")
# print(__version__.__repr__())
# print("======================")

# __all__ = ("__version__",)



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
