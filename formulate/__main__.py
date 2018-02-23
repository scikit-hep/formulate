# Licensed under a 3-clause BSD style license, see LICENSE.
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import argparse
import sys

from formulate import from_root, from_numexpr
from formulate import to_root, to_numexpr


def parse_args(args):
    parser = argparse.ArgumentParser(description='Convert between different types of formulae')

    from_group = parser.add_mutually_exclusive_group(required=True)
    from_group.add_argument('--from-root')
    from_group.add_argument('--from-numexpr')

    to_group = parser.add_mutually_exclusive_group(required=True)
    to_group.add_argument('--to-root', action='store_true')
    to_group.add_argument('--to-numexpr', action='store_true')
    to_group.add_argument('--variables', action='store_true')
    to_group.add_argument('--named-constants', action='store_true')
    to_group.add_argument('--unnamed-constants', action='store_true')

    args = parser.parse_args(args)
    if args.from_root is not None:
        expression = from_root(args.from_root)
    elif args.from_numexpr is not None:
        expression = from_numexpr(args.from_numexpr)
    else:
        raise NotImplementedError()

    if args.to_root:
        result = to_root(expression)
    elif args.to_numexpr:
        result = to_numexpr(expression)
    elif args.variables:
        result = '\n'.join(sorted(expression.variables))
    elif args.named_constants:
        result = '\n'.join(sorted(expression.named_constants))
    elif args.unnamed_constants:
        result = '\n'.join(sorted(expression.unnamed_constants))
    else:
        raise NotImplementedError()

    return result


if __name__ == '__main__':
    print(parse_args(sys.argv[1:]))
