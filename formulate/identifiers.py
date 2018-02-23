# Licensed under a 3-clause BSD style license, see LICENSE.
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

try:
    from enum import Enum, auto
except ImportError:
    from aenum import Enum, auto


__all__ = [
    'IDs',
    'order_of_operations',
]


class IDs(Enum):
    FIXED = auto()  # Something which can't change such as: constants, numbers and variables

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
    XOR = auto()
    NOT = auto()

    EQ = auto()
    NEQ = auto()
    GT = auto()
    GTEQ = auto()
    LT = auto()
    LTEQ = auto()

    SQRT = auto()
    ABS = auto()
    POW = auto()
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

    # One argument functions in ROOT
    BESSELI0 = auto()
    BESSELI1 = auto()
    BESSELJ0 = auto()
    BESSELJ1 = auto()
    BESSELK0 = auto()
    BESSELK1 = auto()
    BESSELY0 = auto()
    BESSELY1 = auto()
    CEIL = auto()
    CEILNINT = auto()
    DILOG = auto()
    ERF = auto()
    ERFC = auto()
    ERFCINVERSE = auto()
    ERFINVERSE = auto()
    EVEN = auto()
    FACTORIAL = auto()
    FLOOR = auto()
    FLOORNINT = auto()
    FREQ = auto()
    KOLMOGOROVPROB = auto()
    LANDAUI = auto()
    LNGAMMA = auto()
    NEXTPRIME = auto()
    NORMQUANTILE = auto()
    ODD = auto()
    SQUARE = auto()
    STRUVEH0 = auto()
    STRUVEH1 = auto()
    STRUVEL0 = auto()
    STRUVEL1 = auto()

    # Two argument functions in ROOT
    BESSELI = auto()
    BESSELK = auto()
    BETA = auto()
    BINOMIAL = auto()
    CHISQUAREQUANTILE = auto()
    LDEXP = auto()
    PERMUTE = auto()
    POISSON = auto()
    POISSONI = auto()
    PROB = auto()
    STUDENT = auto()
    STUDENTI = auto()

    # Three argument functions in ROOT
    AREEQUALABS = auto()
    AREEQUALREL = auto()
    BETACF = auto()
    BETADIST = auto()
    BETADISTI = auto()
    BETAINCOMPLETE = auto()
    BINOMIALI = auto()
    BUBBLEHIGH = auto()
    BUBBLELOW = auto()
    FDIST = auto()
    FDISTI = auto()
    VAVILOV = auto()
    VAVILOVI = auto()

    # 4+ argument functions in ROOT
    ROOTSCUBIC = auto()
    QUANTILES = auto()


# Based on http://en.cppreference.com/w/cpp/language/operator_precedence
order_of_operations = [
    # 3
    [IDs.MINUS, IDs.PLUS],
    [IDs.NOT],
    # Extra
    [IDs.POW, IDs.SQUARE],
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
    # 11
    [IDs.AND],
    # 12
    [IDs.XOR],
    # 13
    [IDs.OR],
]


class ConstantIDs(Enum):
    """Identifiers for constants

     - CGS => Use cm, g & s for units
     - ERR => Uncertainty on quantity
    """
    TRUE = auto()
    FALSE = auto()
    INFINITY = auto()
    NAN = auto()

    SQRT2 = auto()
    E = auto()
    PI = auto()
    INVPI = auto()
    PIOVER2 = auto()
    PIOVER4 = auto()
    TAU = auto()
    LN10 = auto()
    LOG10E = auto()
    DEG2RAD = auto()
    RAD2DEG = auto()

    AVOGADRO = auto()
    AVOGADRO_ERR = auto()
    BOLTZMANN = auto()
    BOLTZMANN_CGS = auto()
    BOLTZMANN_ERR = auto()
    C = auto()
    C_CGS = auto()
    C_ERR = auto()
    DRY_AIR_GAS = auto()
    ELEMENTARY_CHARGE = auto()
    ELEMENTARY_CHARGE_ERR = auto()
    EULER_MASCHERONI = auto()
    G = auto()
    G_CGS = auto()
    G_ERR = auto()
    G_OVER_HBARC = auto()
    G_OVER_HBARC_ERR = auto()
    GRAV_ACCEL = auto()
    GRAV_ACCEL_ERR = auto()
    H = auto()
    H_CGS = auto()
    H_ERR = auto()
    HBAR = auto()
    HBAR_CGS = auto()
    HBAR_ERR = auto()
    HxC = auto()
    HxC_CGS = auto()
    MOL_WEIGHT_DRY_AIR = auto()
    STEFAN_BOLTZMANN = auto()
    STEFAN_BOLTZMANN_ERR = auto()
    UNIVERSAL_GAS = auto()
    UNIVERSAL_GAS_ERR = auto()
