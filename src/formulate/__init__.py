# Licensed under a 3-clause BSD style license, see LICENSE.

"""Conversions between ROOT, NumExpr and Python expression syntax.

Parse an expression with :func:`from_root` or :func:`from_numexpr`, then render
it with :meth:`~formulate.AST.AST.to_root`,
:meth:`~formulate.AST.AST.to_numexpr` or :meth:`~formulate.AST.AST.to_python`:

.. code-block:: pycon

    >>> import formulate
    >>> formulate.from_root("TMath::Sqrt(x**2 + y**2) > 10").to_numexpr()
    '(sqrt(((x ** 2) + (y ** 2))) > 10)'

The parsed expression also reports what it refers to, through
:attr:`~formulate.AST.AST.variables`,
:attr:`~formulate.AST.AST.named_constants` and
:attr:`~formulate.AST.AST.unnamed_constants`.
"""

import functools
import importlib.resources
from typing import Literal

import lark

from . import AST, exceptions, toast
from ._version import __version__
from .exceptions import ParseError

# Ordered by prominence rather than alphabetically: the two parsing functions
# are the entry points, and everything else is reached through what they return.
__all__ = ["from_numexpr", "from_root", "ParseError", "__version__"]  # noqa: RUF022


@functools.cache
def _get_parser(parser_type: Literal["root", "numexpr"]) -> lark.Lark:
    grammar = (
        importlib.resources.files(__package__)
        / "resources"
        / f"{parser_type}_grammar.lark"
    ).read_text()
    return lark.Lark(grammar, parser="lalr")


def from_root(exp: str) -> AST.AST:
    """Parse a ROOT ``TTreeFormula`` expression.

    The expression is parsed with C++ precedence, so ``&&`` and ``||`` bind
    looser than a comparison, ``^`` is exponentiation rather than XOR, and
    ``!`` is logical NOT.

    :param exp: the expression to parse.
    :returns: the parsed expression, ready to be rendered to any backend.
    :raises ParseError: if `exp` is not valid ROOT syntax. The message points
        at the offending location and suggests fixes for the mistakes people
        make most often, such as writing ``&`` where ROOT wants ``&&``.
    :raises SyntaxError: if `exp` parses but names something that cannot be a
        symbol, or passes arguments to a constant.
    :raises ValueError: if `exp` uses an unknown function, constant, or
        namespace.

    .. code-block:: pycon

        >>> import formulate
        >>> formulate.from_root("TMath::Abs(x) < 2.5").to_numexpr()
        '(abs(x) < 2.5)'
    """
    try:
        ptree = _get_parser("root").parse(exp)
    except lark.LarkError as e:
        new_e = exceptions.debug_root(exp, e)
        raise new_e from e
    return toast.toast(ptree)


def from_numexpr(exp: str) -> AST.AST:
    """Parse a NumExpr expression.

    The expression is parsed with Python precedence, so ``&`` and ``|`` bind
    *tighter* than a comparison, ``^`` is XOR, and ``~`` is NOT. Chained
    comparisons such as ``a < b < c`` are rejected, as NumExpr does not
    support them.

    :param exp: the expression to parse.
    :returns: the parsed expression, ready to be rendered to any backend.
    :raises ParseError: if `exp` is not valid NumExpr syntax. The message
        points at the offending location and suggests fixes for the mistakes
        people make most often, such as writing ``&&`` where NumExpr wants
        ``&``.
    :raises SyntaxError: if `exp` parses but names something that cannot be a
        symbol, or passes arguments to a constant.
    :raises ValueError: if `exp` uses an unknown function or constant.

    .. code-block:: pycon

        >>> import formulate
        >>> formulate.from_numexpr("abs(x) < 2.5").to_root()
        '(TMath::Abs(x) < 2.5)'
    """
    try:
        ptree = _get_parser("numexpr").parse(exp)
    except lark.LarkError as e:
        new_e = exceptions.debug_numexpr(exp, e)
        raise new_e from e
    return toast.toast(ptree)
