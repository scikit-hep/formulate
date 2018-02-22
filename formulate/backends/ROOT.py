# Licensed under a 3-clause BSD style license, see LICENSE.
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

from ..identifiers import IDs, ConstantIDs
from ..parser import POperator, PFunction, Parser, PConstant


__all__ = [
    'root_parser',
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

    POperator(IDs.AND, '&&'),
    POperator(IDs.OR, '||'),
    POperator(IDs.NOT, '!', rhs_only=True),

    PFunction(IDs.SQRT, 'sqrt'),
    PFunction(IDs.SQRT, 'TMath::Sqrt'),
    PFunction(IDs.ABS, 'TMath::Abs'),

    PFunction(IDs.LOG, 'log'),
    PFunction(IDs.LOG, 'TMath::Log'),
    PFunction(IDs.LOG2, 'log2'),
    PFunction(IDs.LOG2, 'TMath::Log2'),
    PFunction(IDs.LOG10, 'log10'),
    PFunction(IDs.LOG10, 'TMath::Log10'),

    PFunction(IDs.EXP, 'exp'),
    PFunction(IDs.EXP, 'TMath::Exp'),

    PFunction(IDs.SIN, 'sin'),
    PFunction(IDs.SIN, 'TMath::Sin'),
    PFunction(IDs.ASIN, 'arcsin'),
    PFunction(IDs.ASIN, 'TMath::ASin'),
    PFunction(IDs.COS, 'cos'),
    PFunction(IDs.COS, 'TMath::Cos'),
    PFunction(IDs.ACOS, 'arccos'),
    PFunction(IDs.ACOS, 'TMath::ACos'),
    PFunction(IDs.TAN, 'tan'),
    PFunction(IDs.TAN, 'TMath::Tan'),
    PFunction(IDs.ATAN, 'arctan'),
    PFunction(IDs.ATAN, 'TMath::ATan'),
    PFunction(IDs.ATAN2, 'arctan2', 2),
    PFunction(IDs.ATAN2, 'TMath::ATan2', 2),

    PFunction(IDs.COSH, 'TMath::CosH'),
    PFunction(IDs.ACOSH, 'TMath::ACosH'),
    PFunction(IDs.SINH, 'TMath::SinH'),
    PFunction(IDs.ASINH, 'TMath::ASinH'),
    PFunction(IDs.TANH, 'TMath::TanH'),
    PFunction(IDs.ATANH, 'TMath::ATanH'),
]

constants = [
    PConstant(ConstantIDs.TRUE, 'true'),
    PConstant(ConstantIDs.FALSE, 'false'),
    PConstant(ConstantIDs.INFINITY, 'TMath::Infinity()'),
    PConstant(ConstantIDs.NAN, 'TMath::QuietNaN()'),
    # PConstant(ConstantIDs., 'TMath::SignalingNaN()'),

    PConstant(ConstantIDs.SQRT2, 'sqrt2'),
    PConstant(ConstantIDs.SQRT2, 'TMath::Sqrt2()'),
    PConstant(ConstantIDs.E, 'e'),
    PConstant(ConstantIDs.E, 'TMath::E()'),
    PConstant(ConstantIDs.PI, 'pi'),
    PConstant(ConstantIDs.PI, 'TMath::Pi()'),
    PConstant(ConstantIDs.INVPI, 'TMath::InvPi()'),
    PConstant(ConstantIDs.PIOVER2, 'TMath::PiOver2()'),
    PConstant(ConstantIDs.PIOVER4, 'TMath::PiOver4()'),
    PConstant(ConstantIDs.TAU, 'TMath::TwoPi()'),
    PConstant(ConstantIDs.LN10, 'ln10'),
    PConstant(ConstantIDs.LN10, 'TMath::Ln10()'),
    PConstant(ConstantIDs.LOG10E, 'TMath::LogE()'),
    PConstant(ConstantIDs.DEG2RAD, 'TMath::DegToRad()'),
    PConstant(ConstantIDs.RAD2DEG, 'TMath::RadToDeg()'),

    PConstant(ConstantIDs.AVOGADRO, 'TMath::Na()'),
    PConstant(ConstantIDs.AVOGADRO_ERR, 'TMath::NaUncertainty()'),
    PConstant(ConstantIDs.BOLTZMANN, 'TMath::K()'),
    PConstant(ConstantIDs.BOLTZMANN_CGS, 'TMath::Kcgs()'),
    PConstant(ConstantIDs.BOLTZMANN_ERR, 'TMath::KUncertainty()'),
    PConstant(ConstantIDs.C, 'TMath::C()'),
    PConstant(ConstantIDs.C_CGS, 'TMath::Ccgs()'),
    PConstant(ConstantIDs.C_ERR, 'TMath::CUncertainty()'),
    PConstant(ConstantIDs.DRY_AIR_GAS, 'TMath::Rgair()'),
    PConstant(ConstantIDs.ELEMENTARY_CHARGE, 'TMath::Qe()'),
    PConstant(ConstantIDs.ELEMENTARY_CHARGE_ERR, 'TMath::QeUncertainty()'),
    PConstant(ConstantIDs.EULER_MASCHERONI, 'TMath::EulerGamma()'),
    PConstant(ConstantIDs.G, 'TMath::G()'),
    PConstant(ConstantIDs.G_CGS, 'TMath::Gcgs()'),
    PConstant(ConstantIDs.G_ERR, 'TMath::GUncertainty()'),
    PConstant(ConstantIDs.G_OVER_HBARC, 'TMath::GhbarC()'),
    PConstant(ConstantIDs.G_OVER_HBARC_ERR, 'TMath::GhbarCUncertainty()'),
    PConstant(ConstantIDs.GRAV_ACCEL, 'TMath::Gn()'),
    PConstant(ConstantIDs.GRAV_ACCEL_ERR, 'TMath::GnUncertainty()'),
    PConstant(ConstantIDs.H, 'TMath::H()'),
    PConstant(ConstantIDs.H_CGS, 'TMath::Hcgs()'),
    PConstant(ConstantIDs.H_ERR, 'TMath::HUncertainty()'),
    PConstant(ConstantIDs.HBAR, 'TMath::Hbar()'),
    PConstant(ConstantIDs.HBAR_CGS, 'TMath::Hbarcgs()'),
    PConstant(ConstantIDs.HBAR_ERR, 'TMath::HbarUncertainty()'),
    PConstant(ConstantIDs.HxC, 'TMath::HC()'),
    PConstant(ConstantIDs.HxC_CGS, 'TMath::HCcgs()'),
    PConstant(ConstantIDs.MOL_WEIGHT_DRY_AIR, 'TMath::MWair()'),
    PConstant(ConstantIDs.STEFAN_BOLTZMANN, 'TMath::Sigma()'),
    PConstant(ConstantIDs.STEFAN_BOLTZMANN_ERR, 'TMath::SigmaUncertainty()'),
    PConstant(ConstantIDs.UNIVERSAL_GAS, 'TMath::R()'),
    PConstant(ConstantIDs.UNIVERSAL_GAS_ERR, 'TMath::RUncertainty()'),
]

root_parser = Parser('ROOT', config, constants)
