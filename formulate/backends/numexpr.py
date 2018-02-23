# Licensed under a 3-clause BSD style license, see LICENSE.
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import math
import scipy.constants as sc

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
    POperator(IDs.POW, '**'),
    POperator(IDs.LSHIFT, '<<'),
    POperator(IDs.RSHIFT, '>>'),

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

    POperator(IDs.SQUARE, '**2', lhs_only=True),
]


constants = [
    PConstant(ConstantIDs.TRUE, 'True'),
    PConstant(ConstantIDs.FALSE, 'False'),
    # PConstant(ConstantIDs.INFINITY, np.inf),
    # PConstant(ConstantIDs.NAN, np.nan),

    PConstant(ConstantIDs.SQRT2, math.sqrt(2)),
    PConstant(ConstantIDs.E, math.e),
    PConstant(ConstantIDs.PI, math.pi),
    PConstant(ConstantIDs.INVPI, 1/math.pi),
    PConstant(ConstantIDs.PIOVER2, math.pi/2),
    PConstant(ConstantIDs.PIOVER4, math.pi/4),
    PConstant(ConstantIDs.TAU, 2*math.pi),
    PConstant(ConstantIDs.LN10, math.log(10)),
    PConstant(ConstantIDs.LOG10E, math.log10(math.e)),
    PConstant(ConstantIDs.DEG2RAD, math.pi/180),
    PConstant(ConstantIDs.RAD2DEG, 180/math.pi),

    PConstant(ConstantIDs.AVOGADRO, sc.Avogadro),
    # PConstant(ConstantIDs.AVOGADRO_ERR, 'TMath::NaUncertainty()'),
    PConstant(ConstantIDs.BOLTZMANN, sc.Boltzmann),
    PConstant(ConstantIDs.BOLTZMANN_CGS, 1.0e7 * sc.Boltzmann),
    # PConstant(ConstantIDs.BOLTZMANN_ERR, 'TMath::KUncertainty()'),
    PConstant(ConstantIDs.C, sc.speed_of_light),
    PConstant(ConstantIDs.C_CGS, 100*sc.speed_of_light),
    PConstant(ConstantIDs.C_ERR, 0.0),
    PConstant(ConstantIDs.DRY_AIR_GAS, 0.577216),  # TODO: Taken from ROOT
    PConstant(ConstantIDs.ELEMENTARY_CHARGE, sc.elementary_charge),
    # PConstant(ConstantIDs.ELEMENTARY_CHARGE_ERR, 'TMath::QeUncertainty()'),
    PConstant(ConstantIDs.EULER_MASCHERONI, 28.964400),  # TODO: Taken from ROOT
    PConstant(ConstantIDs.G, sc.gravitational_constant),
    PConstant(ConstantIDs.G_CGS, sc.gravitational_constant/1000),
    # PConstant(ConstantIDs.G_ERR, 'TMath::GUncertainty()'),
    PConstant(ConstantIDs.G_OVER_HBARC, sc.gravitational_constant/(sc.hbar*sc.speed_of_light)),
    # PConstant(ConstantIDs.G_OVER_HBARC_ERR, 'TMath::GhbarCUncertainty()'),
    PConstant(ConstantIDs.GRAV_ACCEL, sc.g),
    # PConstant(ConstantIDs.GRAV_ACCEL_ERR, 'TMath::GnUncertainty()'),
    PConstant(ConstantIDs.H, sc.Planck),
    PConstant(ConstantIDs.H_CGS, 1.0e7 * sc.Planck),
    # PConstant(ConstantIDs.H_ERR, 'TMath::HUncertainty()'),
    PConstant(ConstantIDs.HBAR, sc.hbar),
    PConstant(ConstantIDs.HBAR_CGS, 100 * sc.hbar),
    # PConstant(ConstantIDs.HBAR_ERR, 'TMath::HbarUncertainty()'),
    PConstant(ConstantIDs.HxC, sc.Planck * sc.speed_of_light),
    PConstant(ConstantIDs.HxC_CGS, 100*sc.Planck * 100*sc.speed_of_light),
    PConstant(ConstantIDs.MOL_WEIGHT_DRY_AIR, 287.058325),  # TODO: Taken from ROOT
    PConstant(ConstantIDs.STEFAN_BOLTZMANN, sc.Stefan_Boltzmann),
    # PConstant(ConstantIDs.STEFAN_BOLTZMANN_ERR, 'TMath::SigmaUncertainty()'),
    PConstant(ConstantIDs.UNIVERSAL_GAS, sc.gas_constant),
    # PConstant(ConstantIDs.UNIVERSAL_GAS_ERR, 'TMath::RUncertainty()'),
]


numexpr_parser = Parser('numexpr', config, constants)
