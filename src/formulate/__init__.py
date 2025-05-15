# -*- coding: utf-8 -*-
# Licensed under a 3-clause BSD style license, see LICENSE.

from __future__ import annotations

from . import ttreeformula_parser, numexpr_parser  # noqa  # noqa

from . import convert_ptree

from . import AST

from . import toast

from ._version import __version__


def from_root(exp : str, **kwargs) -> AST :
    """Evaluate ttreformula expressions."""
    # Preprocess the expression to handle multiple occurrences of the same binary operator
    # This should be fixed in the actual parser, generated from Lark. Somehow, this only fails for
    # root parsing
    exp = _preprocess_expression(exp)
    parser = ttreeformula_parser.Lark_StandAlone()
    ptree = parser.parse(exp)
    convert_ptree.convert_ptree(ptree)
    return toast.toast(ptree, nxp=False)

def _preprocess_expression(exp: str) -> str:
    """Preprocess the expression to handle multiple occurrences of the same operator.

    This function adds parentheses to group operators correctly.
    For example, "a||b||c" becomes "((a||b)||c)".
    """
    import re

    def _add_parentheses_for_operator(exp: str, operator: str) -> str:
        """Add parentheses for a specific operator to ensure correct precedence.

        Args:
            exp: The expression to process
            operator: The operator to handle ('||', '&&', '|', or '&')
        """
        import re
        # Escape special regex characters in the operator
        escaped_op = re.escape(operator)
        # Create the regex pattern for this operator
        pattern = fr'([a-zA-Z0-9_]+{escaped_op}[a-zA-Z0-9_]+)({escaped_op}[a-zA-Z0-9_]+)+'

        matches = re.finditer(pattern, exp)
        for match in matches:
            original = match.group(0)
            parts = original.split(operator)
            # Create a new expression with parentheses
            new_expr = parts[0]
            for part in parts[1:]:
                new_expr = f"({new_expr}{operator}{part})"
            exp = exp.replace(original, new_expr)

        return exp

    # Process each operator
    for operator in ['||', '&&', '|', '&']:
        exp = _add_parentheses_for_operator(exp, operator)

    return exp

def from_numexpr(exp : str, **kwargs) -> AST :
    """Evaluate numexpr expressions."""
    parser = numexpr_parser.Lark_StandAlone()
    ptree = parser.parse(exp)
    convert_ptree.convert_ptree(ptree)
    return toast.toast(ptree, nxp=True)
