# Licensed under a 3-clause BSD style license, see LICENSE.
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

from ..identifiers import IDs
from ..parser import Operator, Function, Parser


__all__ = [
    'numexpr_parser',
]


config = [
    Operator(IDs.MINUS, '-', rhs_only=True),
    Operator(IDs.PLUS, '+', rhs_only=True),
    Operator(IDs.ADD, '+'),
    Operator(IDs.SUB, '-'),
    Operator(IDs.MUL, '*'),
    Operator(IDs.DIV, '/'),

    Function(IDs.SQRT, 'sqrt'),
    Function(IDs.ABS, 'abs'),
    Function(IDs.WHERE, 'where', 3),

    Function(IDs.LOG, 'log'),
    Function(IDs.LOG10, 'log10'),
    Function(IDs.LOG1p, 'log1p'),

    Function(IDs.EXP, 'exp'),
    Function(IDs.EXPM1, 'expm1'),

    Function(IDs.SIN, 'sin'),
    Function(IDs.ASIN, 'arcsin'),
    Function(IDs.COS, 'cos'),
    Function(IDs.ACOS, 'arccos'),
    Function(IDs.TAN, 'tan'),
    Function(IDs.ATAN, 'arctan'),
    Function(IDs.ATAN2, 'arctan2', 2),

    Function(IDs.SINH, 'sinh'),
    Function(IDs.ASINH, 'arcsinh'),
    Function(IDs.COSH, 'cosh'),
    Function(IDs.ACOSH, 'arccosh'),
    Function(IDs.TANH, 'tanh'),
    Function(IDs.ATANH, 'arctanh'),
]


numexpr_parser = Parser('numexpr', config)
