# Licensed under a 3-clause BSD style license, see LICENSE.

from __future__ import annotations

import re

import lark


class ParseError(Exception):
    def __init__(self, message: str, lark_error: lark.LarkError):
        super().__init__(message)
        self.lark_error = lark_error


def debug_root(exp: str, error: lark.LarkError) -> ParseError:
    msg = ""
    if isinstance(error, lark.UnexpectedInput):
        msg += "There was an error parsing the expression at or near this location\n"
        msg += error.get_context(exp)
    suggestions = []
    if " & " in exp:
        suggestions.append("- Use '&&' instead of '&'.")
    if " | " in exp:
        suggestions.append("- Use '||' instead of '|'.")
    if "~" in exp:
        suggestions.append("- Use '!' instead of '~'.")
    if len(suggestions) > 0:
        msg += "\nHere are some suggestions for how to fix the error:\n"
        msg += "\n".join(suggestions)
        msg += "\n"
    else:
        msg += "\nNo suggestions available.\n"
    msg += "\nHere is the Lark error message:\n"
    msg += str(error)
    return ParseError(msg, error)


def debug_numexpr(exp: str, error: lark.LarkError) -> ParseError:
    msg = ""
    if isinstance(error, lark.UnexpectedInput):
        msg += "There was an error parsing the expression at or near this location\n"
        msg += error.get_context(exp)
    suggestions = []
    if "&&" in exp or " and " in exp:
        suggestions.append("- Use '&' instead of '&&' or 'and'.")
    if "||" in exp or " or " in exp:
        suggestions.append("- Use '|' instead of '||' or 'or'.")
    if re.search(r"!(?!\=)", exp):
        suggestions.append("- Use '~' instead of '!'.")
    if any(comp in exp for comp in ["<", ">", "<=", ">=", "==", "!="]):
        suggestions.append(
            "- Make sure you don't have chained comparisons (e.g., 'a < b < c'), as these are not supported."
        )
    if len(suggestions) > 0:
        msg += "\nHere are some suggestions for how to fix the error:\n"
        msg += "\n".join(suggestions)
        msg += "\n"
    else:
        msg += "\nNo suggestions available.\n"
    msg += "\nHere is the Lark error message:\n"
    msg += str(error)
    return ParseError(msg, error)
