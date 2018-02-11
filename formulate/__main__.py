# Licensed under a 3-clause BSD style license, see LICENSE.
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import argparse

from formulate import from_root, from_numexpr
from formulate import to_root, to_numexpr


def parse_args():
    parser = argparse.ArgumentParser(description='Convert between different types of formulae')

    from_group = parser.add_mutually_exclusive_group(required=True)
    from_group.add_argument('--from-root')
    from_group.add_argument('--from-numexpr')

    to_group = parser.add_mutually_exclusive_group(required=True)
    to_group.add_argument('--to-root', action='store_true')
    to_group.add_argument('--to-numexpr', action='store_true')

    args = parser.parse_args()
    if args.from_root is not None:
        expression = from_root(args.from_root)
    elif args.from_numexpr is not None:
        expression = from_numexpr(args.from_numexpr)

    if args.to_root:
        result = to_root(expression)
    elif args.to_numexpr:
        result = to_numexpr(expression)

    print(result)


if __name__ == '__main__':
    parse_args()
