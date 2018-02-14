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
    # 11
    [IDs.AND],
    # 12
    [IDs.XOR],
    # 13
    [IDs.OR],
]


class ConstantIDs(Enum):
    TRUE = auto()
    FALSE = auto()

    SQRT2 = auto()
    E = auto()
    PI = auto()
    INVPI = auto()
    PIOVER2 = auto()
    PIOVER4 = auto()
    TAU = auto()
    LN10 = auto()
    LOG10E = auto()

    C = auto()
    H = auto()
    HBAR = auto()
    K = auto()
    R = auto()
    G = auto()

    DEG2RAD = auto()
    RAD2DEG = auto()


# C('sqrt2'): C(math.sqrt(2)),
# C('e'): C(math.e),
# C('pi'): C(math.pi),
# C('ln10'): C(math.log(10)),
# F('TMath::C()'): C(sc.speed_of_light),
# F('TMath::Ccgs()'): C(100 * sc.speed_of_light),
# F('TMath::DegToRad()'): C(math.pi/180),
# F('TMath::E()'): C(math.e),
# F('TMath::G()'): C(sc.gravitational_constant),
# F('TMath::H()'): C(sc.Planck),
# F('TMath::HC()'): C(sc.Planck * sc.speed_of_light),
# F('TMath::HCcgs()'): C(100*sc.Planck * 100*sc.speed_of_light),
# F('TMath::Hbar()'): C(sc.Planck/(2*math.pi)),
# F('TMath::Hbarcgs()'): C(100 * sc.Planck/(2*math.pi)),
# F('TMath::Hcgs()'): C(1.0e7 * sc.Planck),
# F('TMath::InvPi()'): C(1/math.pi),
# F('TMath::K()'): C(sc.Boltzmann),
# F('TMath::Kcgs()'): C(1.0e7 * sc.Boltzmann),
# F('TMath::Ln10()'): C(math.log(10)),
# F('TMath::LogE()'): C(math.log10(math.e)),
# F('TMath::Na()'): C(sc.Avogadro),
# F('TMath::Pi()'): C(math.pi),
# F('TMath::PiOver2()'): C(math.pi/2),
# F('TMath::PiOver4()'): C(math.pi/4),
# F('TMath::Qe()'): C(sc.elementary_charge),
# F('TMath::R()'): C(sc.gas_constant),
# F('TMath::RadToDeg()'): C(180/math.pi),
# F('TMath::Sqrt2()'): C(math.sqrt(2)),
# F('TMath::TwoPi()'): C(2*math.pi),
# # Uncertainties
# F('TMath::CUncertainty()'): C(0),
# F('TMath::GUncertainty()'): None,
# F('TMath::GhbarCUncertainty()'): None,
# F('TMath::GnUncertainty()'): C(0),
# F('TMath::HUncertainty()'): None,
# F('TMath::HbarUncertainty()'): None,
# F('TMath::KUncertainty()'): None,
# F('TMath::NaUncertainty()'): None,
# F('TMath::QeUncertainty()'): None,
# F('TMath::RUncertainty()'): None,
# F('TMath::SigmaUncertainty()'): None,
