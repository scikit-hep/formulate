# Licensed under a 3-clause BSD style license, see LICENSE.

from __future__ import annotations

from typing import Any

import lark

from . import AST, toast
from ._version import __version__

__all__ = ["__version__", "from_numexpr", "from_root"]


def _get_parser(parser_type: str) -> lark.lark.Lark:
    import importlib.resources

    grammar = (
        importlib.resources.files(__package__)
        / "resources"
        / f"{parser_type}_grammar.lark"
    ).read_text()
    return lark.Lark(grammar, parser="lalr")


_numexpr_parser = _get_parser("numexpr")
_root_parser = _get_parser("root")


def from_root(exp: str, **kwargs: dict[str, Any]) -> AST.AST:
    """Evaluate ROOT expressions."""
    ptree = _root_parser.parse(exp)
    return toast.toast(ptree)  # type: ignore[no-any-return]


def from_numexpr(exp: str, **kwargs: dict[str, Any]) -> AST.AST:
    """Evaluate numexpr expressions."""
    ptree = _numexpr_parser.parse(exp)
    return toast.toast(ptree)  # type: ignore[no-any-return]


# This was added to Lark in https://github.com/lark-parser/lark/pull/1521
# Remove when there is a new release
lark.Tree.__match_args__ = ("data", "children")  # type: ignore[misc]
