# Licensed under a 3-clause BSD style license, see LICENSE.
from __future__ import annotations

import argparse
import sys

from . import from_numexpr, from_root


def parse_args(args: list[str]) -> str:
    parser = argparse.ArgumentParser(
        description="Convert between different types of formulae"
    )

    from_group = parser.add_mutually_exclusive_group(required=True)
    from_group.add_argument("--from-root")
    from_group.add_argument("--from-numexpr")

    to_group = parser.add_mutually_exclusive_group(required=True)
    to_group.add_argument("--to-root", action="store_true")
    to_group.add_argument("--to-numexpr", action="store_true")
    to_group.add_argument("--to-python", action="store_true")
    to_group.add_argument("--variables", action="store_true")
    to_group.add_argument("--named-constants", action="store_true")
    to_group.add_argument("--unnamed-constants", action="store_true")

    parsed_args = parser.parse_args(args)
    if parsed_args.from_root is not None:
        expression = from_root(parsed_args.from_root)
    elif parsed_args.from_numexpr is not None:
        expression = from_numexpr(parsed_args.from_numexpr)
    else:
        msg = "This should never happen. Please report this issue to the Formulate developers."
        raise NotImplementedError(msg)

    if parsed_args.to_root:
        result = expression.to_root()
    elif parsed_args.to_numexpr:
        result = expression.to_numexpr()
    elif parsed_args.to_python:
        result = expression.to_python()
    elif parsed_args.variables:
        result = "\n".join(sorted(expression.variables))
    elif parsed_args.named_constants:
        result = "\n".join(sorted(expression.named_constants))
    elif parsed_args.unnamed_constants:
        result = "\n".join(sorted(expression.unnamed_constants))
    else:
        msg = "This should never happen. Please report this issue to the Formulate developers."
        raise NotImplementedError(msg)

    return result


def main() -> None:
    sys.stdout.write(parse_args(sys.argv[1:]))
    sys.stdout.write("\n")


if __name__ == "__main__":
    main()
