# Licensed under a 3-clause BSD style license, see LICENSE.

"""The ``formulate`` command-line interface.

One input option says what to parse and one output option says what to print,
for example::

    formulate --from-root '(A && B) || TMath::Sqrt(A)' --to-numexpr
"""

import argparse
import sys

from . import from_numexpr, from_root
from ._version import __version__

_EPILOG = """\
examples:
  formulate --from-root '(A && B) || TMath::Sqrt(A)' --to-numexpr
  formulate --from-numexpr '(A & B) | sqrt(A)' --to-root
  formulate --from-root 'TMath::Sqrt(x) > 5*pi' --variables
"""


def parse_args(args: list[str]) -> str:
    """Run one conversion and return what the command should print.

    :param args: the command-line arguments, without the program name.
    :returns: the converted expression, or the requested names one per line.
    :raises SystemExit: if `args` are not a valid combination, or ask for
        ``--help`` or ``--version``.
    """
    parser = argparse.ArgumentParser(
        description="Convert between different styles of expressions.",
        epilog=_EPILOG,
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    parser.add_argument(
        "--version", action="version", version=f"%(prog)s {__version__}"
    )

    from_group = parser.add_mutually_exclusive_group(required=True)
    from_group.add_argument(
        "--from-root", metavar="EXPRESSION", help="parse a ROOT TTreeFormula expression"
    )
    from_group.add_argument(
        "--from-numexpr", metavar="EXPRESSION", help="parse a NumExpr expression"
    )

    to_group = parser.add_mutually_exclusive_group(required=True)
    to_group.add_argument(
        "--to-root", action="store_true", help="print it as a ROOT expression"
    )
    to_group.add_argument(
        "--to-numexpr", action="store_true", help="print it as a NumExpr expression"
    )
    to_group.add_argument(
        "--to-python",
        action="store_true",
        help="print it as Python, using NumPy functions",
    )
    to_group.add_argument(
        "--variables",
        action="store_true",
        help="print the variables it reads, one per line",
    )
    to_group.add_argument(
        "--named-constants",
        action="store_true",
        help="print the named constants it uses, one per line",
    )
    to_group.add_argument(
        "--unnamed-constants",
        action="store_true",
        help="print the numeric literals it contains, one per line",
    )

    parsed_args = parser.parse_args(args)
    if parsed_args.from_root is not None:
        expression = from_root(parsed_args.from_root)
    elif parsed_args.from_numexpr is not None:
        expression = from_numexpr(parsed_args.from_numexpr)
    else:  # pragma: no cover
        msg = (
            "This should never happen. "
            "Please report this issue to the Formulate developers."
        )
        raise NotImplementedError(msg)

    if parsed_args.to_root:
        result = expression.to_root()
    elif parsed_args.to_numexpr:
        result = expression.to_numexpr()
    elif parsed_args.to_python:
        result = expression.to_python()
    elif parsed_args.variables:
        result = "\n".join(expression.variables)
    elif parsed_args.named_constants:
        result = "\n".join(expression.named_constants)
    elif parsed_args.unnamed_constants:
        result = "\n".join(map(str, expression.unnamed_constants))
    else:  # pragma: no cover
        msg = (
            "This should never happen. "
            "Please report this issue to the Formulate developers."
        )
        raise NotImplementedError(msg)

    return result


def main() -> None:
    """Entry point of the ``formulate`` command."""
    sys.stdout.write(parse_args(sys.argv[1:]))
    sys.stdout.write("\n")
