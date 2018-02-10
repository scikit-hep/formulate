# Licensed under a 3-clause BSD style license, see LICENSE.
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

from enum import Enum, auto


__all__ = [
    'IDs',
    'order_of_operations',
]


class IDs(Enum):
    MINUS = auto()
    PLUS = auto()
    ADD = auto()
    SUB = auto()
    MUL = auto()
    DIV = auto()

    AND = auto()
    OR = auto()
    XOR = auto()

    SQRT = auto()
    ABS = auto()
    WHERE = auto()

    LOG = auto()
    LOG2 = auto()
    LOG10 = auto()
    LOG1p = auto()

    EXP = auto()
    EXPM1 = auto()

    SIN = auto()
    ASIN = auto()
    COS = auto()
    ACOS = auto()
    TAN = auto()
    ATAN = auto()
    ATAN2 = auto()

    SINH = auto()
    ASINH = auto()
    COSH = auto()
    ACOSH = auto()
    TANH = auto()
    ATANH = auto()


order_of_operations = [
    IDs.MINUS,
    IDs.PLUS,

    IDs.DIV,
    IDs.MUL,
    IDs.ADD,
    IDs.SUB,

    IDs.AND,
    IDs.OR,
    IDs.XOR,
]
