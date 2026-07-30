# Licensed under a 3-clause BSD style license, see LICENSE.

"""Parse failures, and the hints attached to them.

The parsers report a syntax error as a :class:`ParseError` whose message shows
where parsing stopped and, where a common mistake is recognisable, how to fix
it. The hints are heuristics over the source text, so they can suggest
something that is not the actual problem; the underlying lark error is always
included as well, and kept on the exception as
:attr:`ParseError.lark_error`.
"""

import re

import lark


class ParseError(Exception):
    """Raised when an expression cannot be parsed.

    :param message: the human-readable report: where parsing stopped, any
        suggestions, and the underlying lark message.
    :param lark_error: the error raised by lark, kept for programmatic access
        to details such as the line and column.
    """

    def __init__(self, message: str, lark_error: lark.LarkError):
        super().__init__(message)
        self.lark_error = lark_error


def _build_parse_error(
    exp: str, error: lark.LarkError, suggestions: list[str]
) -> ParseError:
    msg = ""
    if isinstance(error, lark.UnexpectedInput):
        msg += "There was an error parsing the expression at or near this location\n"
        msg += error.get_context(exp)
    if suggestions:
        msg += "\nHere are some suggestions for how to fix the error:\n"
        msg += "\n".join(suggestions)
        msg += "\n"
    else:
        msg += "\nNo suggestions available.\n"
    msg += "\nHere is the Lark error message:\n"
    msg += str(error)
    return ParseError(msg, error)


def debug_root(exp: str, error: lark.LarkError) -> ParseError:
    """Turn a lark failure on a ROOT expression into a :class:`ParseError`.

    Suggests the ROOT spelling of the logical operators when the expression
    contains the NumExpr one.

    :param exp: the expression that failed to parse.
    :param error: the error lark raised for it.
    """
    suggestions = []
    if re.search(r"(?<!&)&(?!&)", exp):
        suggestions.append("- Use '&&' instead of '&'.")
    if re.search(r"(?<!\|)\|(?!\|)", exp):
        suggestions.append("- Use '||' instead of '|'.")
    if "~" in exp:
        suggestions.append("- Use '!' instead of '~'.")
    return _build_parse_error(exp, error, suggestions)


def debug_numexpr(exp: str, error: lark.LarkError) -> ParseError:
    """Turn a lark failure on a NumExpr expression into a :class:`ParseError`.

    Suggests the NumExpr spelling of the logical operators when the expression
    contains the ROOT or Python one, and points out chained comparisons, which
    NumExpr does not support.

    :param exp: the expression that failed to parse.
    :param error: the error lark raised for it.
    """
    suggestions = []
    if "&&" in exp or " and " in exp:
        suggestions.append("- Use '&' instead of '&&' or 'and'.")
    if "||" in exp or " or " in exp:
        suggestions.append("- Use '|' instead of '||' or 'or'.")
    if re.search(r"!(?!\=)", exp):
        suggestions.append("- Use '~' instead of '!'.")
    if any(comp in exp for comp in ["<", ">", "<=", ">=", "==", "!="]):
        suggestions.append(
            "- Make sure you don't have chained comparisons "
            "(e.g., 'a < b < c'), as these are not supported."
        )
    return _build_parse_error(exp, error, suggestions)
