# Licensed under a 3-clause BSD style license, see LICENSE.

from __future__ import annotations

import functools
import importlib.resources
from typing import Any

import lark

from . import AST, exceptions, toast
from ._version import __version__
from .exceptions import ParseError

__all__ = ["ParseError", "__version__", "from_numexpr", "from_root"]


@functools.cache
def _get_parser(parser_type: str) -> lark.lark.Lark:
    grammar = (
        importlib.resources.files(__package__)
        / "resources"
        / f"{parser_type}_grammar.lark"
    ).read_text()
    return lark.Lark(grammar, parser="lalr")


def from_root(exp: str, **kwargs: dict[str, Any]) -> AST.AST:
    """Evaluate ROOT expressions."""
    try:
        ptree = _get_parser("root").parse(exp)
    except lark.LarkError as e:
        new_e = exceptions.debug_root(exp, e)
        raise new_e from e
    return toast.toast(ptree)


def from_numexpr(exp: str, **kwargs: dict[str, Any]) -> AST.AST:
    """Evaluate numexpr expressions."""
    try:
        ptree = _get_parser("numexpr").parse(exp)
    except lark.LarkError as e:
        new_e = exceptions.debug_numexpr(exp, e)
        raise new_e from e
    return toast.toast(ptree)
