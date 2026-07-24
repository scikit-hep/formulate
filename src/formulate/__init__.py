# Licensed under a 3-clause BSD style license, see LICENSE.

import functools
import importlib.resources

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


def from_root(exp: str) -> AST.AST:
    """Parse a ROOT expression and return an AST."""
    try:
        ptree = _get_parser("root").parse(exp)
    except lark.LarkError as e:
        new_e = exceptions.debug_root(exp, e)
        raise new_e from e
    return toast.toast(ptree)


def from_numexpr(exp: str) -> AST.AST:
    """Parse a numexpr expression and return an AST."""
    try:
        ptree = _get_parser("numexpr").parse(exp)
    except lark.LarkError as e:
        new_e = exceptions.debug_numexpr(exp, e)
        raise new_e from e
    return toast.toast(ptree)
