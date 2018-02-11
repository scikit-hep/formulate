# Licensed under a 3-clause BSD style license, see LICENSE.
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

from aenum import Enum, auto


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
    MOD = auto()

    LSHIFT = auto()
    RSHIFT = auto()

    AND = auto()
    OR = auto()
    NOT = auto()

    EQ = auto()
    NEQ = auto()
    GT = auto()
    GTEQ = auto()
    LT = auto()
    LTEQ = auto()

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


# Based on http://en.cppreference.com/w/cpp/language/operator_precedence
order_of_operations = [
    # 3
    [IDs.MINUS, IDs.PLUS],
    [IDs.NOT],
    # 5
    [IDs.MUL, IDs.DIV, IDs.MOD],
    # 6
    [IDs.ADD, IDs.SUB],
    # 7
    [IDs.LSHIFT, IDs.RSHIFT],
    # 9
    [IDs.LT, IDs.LTEQ],
    [IDs.GT, IDs.GTEQ],
    # 10
    [IDs.EQ, IDs.NEQ],
    # 14
    [IDs.AND],
    # 15
    [IDs.OR],
]
