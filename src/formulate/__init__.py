# Licensed under a 3-clause BSD style license, see LICENSE.

from __future__ import annotations

from . import (
    AST,
    convert_ptree,
    exceptions,
    numexpr_parser,
    toast,
    ttreeformula_parser,
)
from ._version import __version__

__all__ = ["__version__", "exceptions", "from_numexpr", "from_root"]


def from_root(exp: str, *, standalone: bool = True, **kwargs) -> AST:
    """Evaluate ttreeformula expressions."""
    if standalone:
        parser = ttreeformula_parser.Lark_StandAlone()
    else:
        # TODO: Is there a better way to do this?
        try:
            import lark
        except ImportError as err:
            msg = "lark needs to be installed for non-standalone parsing"
            raise ImportError(msg) from err
        from pathlib import Path

        module_path = Path(__file__).parent
        grammar_path = module_path / "ttreeformula_grammar.lark"
        with grammar_path.open("r") as f:
            grammar = f.read()
        parser = lark.Lark(grammar, parser="lalr")
    ptree = parser.parse(exp)
    convert_ptree.convert_ptree(ptree)
    return toast.toast(ptree, nxp=False)


def from_numexpr(exp: str, *, standalone: bool = True, **kwargs) -> AST:
    """Evaluate numexpr expressions."""
    if standalone:
        parser = numexpr_parser.Lark_StandAlone()
    else:
        # TODO: Is there a better way to do this?
        try:
            import lark
        except ImportError as err:
            msg = "lark needs to be installed for non-standalone parsing"
            raise ImportError(msg) from err
        from pathlib import Path

        module_path = Path(__file__).parent
        grammar_path = module_path / "numexpr_grammar.lark"
        with grammar_path.open("r") as f:
            grammar = f.read()
        parser = lark.Lark(grammar, parser="lalr")
    ptree = parser.parse(exp)
    convert_ptree.convert_ptree(ptree, standalone)
    return toast.toast(ptree, nxp=True)
