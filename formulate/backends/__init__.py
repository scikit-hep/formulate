# Licensed under a 3-clause BSD style license, see LICENSE.
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import re

from ..parser import ParsingException
from .numexpr import numexpr_parser
from .ROOT import root_parser


__all__ = [
    'from_auto',
    'from_numexpr',
    'to_numexpr',
    'from_root',
    'to_root',
]


from_numexpr = numexpr_parser.to_expression
to_numexpr = numexpr_parser.to_string

from_root = root_parser.to_expression
to_root = root_parser.to_string


def from_auto(string):
    # Intelligently detect which kind of string is passed
    if any(x in string for x in ['&&', '||', 'TMath::', 'true', 'false']):
        return from_root(string)
    elif (re.findall(r'([^\&]\&[^\&])|([^\|]\|[^\|])', string) or
          'True' in string or 'False' in string):
        return from_numexpr(string)

    # Intelligently detecting failed so fall back to brute force
    try:
        return from_root(string)
    except ParsingException:
        pass

    try:
        return from_numexpr(string)
    except ParsingException:
        pass

    raise ParsingException('No available backend which can parse: '+string)
