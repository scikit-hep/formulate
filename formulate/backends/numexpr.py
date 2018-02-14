# Licensed under a 3-clause BSD style license, see LICENSE.
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import math

from ..identifiers import IDs, ConstantIDs
from ..parser import POperator, PFunction, Parser, PConstant


__all__ = [
    'numexpr_parser',
]


config = [
    POperator(IDs.MINUS, '-', rhs_only=True),
    POperator(IDs.PLUS, '+', rhs_only=True),
    POperator(IDs.ADD, '+'),
    POperator(IDs.SUB, '-'),
    POperator(IDs.MUL, '*'),
    POperator(IDs.DIV, '/'),
    POperator(IDs.MOD, '%'),

    POperator(IDs.EQ, '=='),
    POperator(IDs.NEQ, '!='),
    POperator(IDs.GT, '>'),
    POperator(IDs.GTEQ, '>='),
    POperator(IDs.LT, '<'),
    POperator(IDs.LTEQ, '<='),

    POperator(IDs.AND, '&'),
    POperator(IDs.OR, '|'),
    POperator(IDs.XOR, '^'),
    POperator(IDs.NOT, '~', rhs_only=True),

    PFunction(IDs.SQRT, 'sqrt'),
    PFunction(IDs.ABS, 'abs'),
    PFunction(IDs.WHERE, 'where', 3),

    PFunction(IDs.LOG, 'log'),
    PFunction(IDs.LOG10, 'log10'),
    PFunction(IDs.LOG1p, 'log1p'),

    PFunction(IDs.EXP, 'exp'),
    PFunction(IDs.EXPM1, 'expm1'),

    PFunction(IDs.SIN, 'sin'),
    PFunction(IDs.ASIN, 'arcsin'),
    PFunction(IDs.COS, 'cos'),
    PFunction(IDs.ACOS, 'arccos'),
    PFunction(IDs.TAN, 'tan'),
    PFunction(IDs.ATAN, 'arctan'),
    PFunction(IDs.ATAN2, 'arctan2', 2),

    PFunction(IDs.SINH, 'sinh'),
    PFunction(IDs.ASINH, 'arcsinh'),
    PFunction(IDs.COSH, 'cosh'),
    PFunction(IDs.ACOSH, 'arccosh'),
    PFunction(IDs.TANH, 'tanh'),
    PFunction(IDs.ATANH, 'arctanh'),
]


constants = [
    PConstant(ConstantIDs.TRUE, 'True'),
    PConstant(ConstantIDs.FALSE, 'False'),

    PConstant(ConstantIDs.SQRT2, math.sqrt(2)),
    PConstant(ConstantIDs.E, math.e),
    PConstant(ConstantIDs.PI, math.pi),
    PConstant(ConstantIDs.INVPI, 1/math.pi),
    PConstant(ConstantIDs.PIOVER2, math.pi/2),
    PConstant(ConstantIDs.PIOVER4, math.pi/4),
    PConstant(ConstantIDs.TAU, 2*math.pi),
    PConstant(ConstantIDs.LN10, math.log(10)),
    PConstant(ConstantIDs.LOG10E, math.log10(math.e)),
]


numexpr_parser = Parser('numexpr', config, constants)
