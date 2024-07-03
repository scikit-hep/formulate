"""
Copyright (c) 2023 Aryan Roy. All rights reserved.

formulate:  Easy conversions between different styles of expressions
"""


from __future__ import annotations

from . import ttreeformula, numexpr  # noqa  # noqa

from . import AST

from . import toast

__version__ = "0.1.0"

__all__ = ("__version__",)



def from_root(exp : str, **kwargs) -> AST :
    parser = ttreeformula.Lark_StandAlone()
    ptree = parser.parse(exp)
    return toast.toast(ptree, nxp=False)

def from_numexpr(exp : str, **kwargs) -> AST :
    parser = numexpr.Lark_StandAlone()
    ptree = parser.parse(exp)
    return toast.toast(ptree, nxp=True)
