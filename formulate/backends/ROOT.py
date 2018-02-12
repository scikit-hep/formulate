# Licensed under a 3-clause BSD style license, see LICENSE.
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

from ..identifiers import IDs, ConstantIDs
from ..parser import Operator, Function, Parser, Constant


__all__ = [
    'root_parser',
]


config = [
    Operator(IDs.MINUS, '-', rhs_only=True),
    Operator(IDs.PLUS, '+', rhs_only=True),
    Operator(IDs.ADD, '+'),
    Operator(IDs.SUB, '-'),
    Operator(IDs.MUL, '*'),
    Operator(IDs.DIV, '/'),
    Operator(IDs.MOD, '%'),

    Operator(IDs.EQ, '=='),
    Operator(IDs.NEQ, '!='),
    Operator(IDs.GT, '>'),
    Operator(IDs.GTEQ, '>='),
    Operator(IDs.LT, '<'),
    Operator(IDs.LTEQ, '<='),

    Operator(IDs.AND, '&&'),
    Operator(IDs.OR, '||'),
    Operator(IDs.NOT, '!', rhs_only=True),

    Function(IDs.SQRT, 'sqrt'),
    Function(IDs.SQRT, 'TMath::Sqrt'),
    Function(IDs.ABS, 'TMath::Abs'),

    Function(IDs.LOG, 'log'),
    Function(IDs.LOG, 'TMath::Log'),
    Function(IDs.LOG2, 'log2'),
    Function(IDs.LOG2, 'TMath::Log2'),
    Function(IDs.LOG10, 'log10'),
    Function(IDs.LOG10, 'TMath::Log10'),

    Function(IDs.EXP, 'exp'),
    Function(IDs.EXP, 'TMath::Exp'),

    Function(IDs.SIN, 'sin'),
    Function(IDs.SIN, 'TMath::Sin'),
    Function(IDs.ASIN, 'arcsin'),
    Function(IDs.ASIN, 'TMath::ASin'),
    Function(IDs.COS, 'cos'),
    Function(IDs.COS, 'TMath::Cos'),
    Function(IDs.ACOS, 'arccos'),
    Function(IDs.ACOS, 'TMath::ACos'),
    Function(IDs.TAN, 'tan'),
    Function(IDs.TAN, 'TMath::Tan'),
    Function(IDs.ATAN, 'arctan'),
    Function(IDs.ATAN, 'TMath::ATan'),
    Function(IDs.ATAN2, 'arctan2', 2),
    Function(IDs.ATAN2, 'TMath::ATan2', 2),
]

constants = [
    Constant(ConstantIDs.SQRT2, 'sqrt2'),
    Constant(ConstantIDs.SQRT2, 'TMath::Sqrt2()'),
    Constant(ConstantIDs.E, 'e'),
    Constant(ConstantIDs.E, 'TMath::E()'),
    Constant(ConstantIDs.PI, 'pi'),
    Constant(ConstantIDs.PI, 'TMath::Pi()'),
    Constant(ConstantIDs.INVPI, 'TMath::InvPi()'),
    Constant(ConstantIDs.PIOVER2, 'TMath::PiOver2()'),
    Constant(ConstantIDs.PIOVER4, 'TMath::PiOver4()'),
    Constant(ConstantIDs.TAU, 'TMath::TwoPi()'),
    Constant(ConstantIDs.LN10, 'ln10'),
    Constant(ConstantIDs.LN10, 'TMath::Ln10()'),
    Constant(ConstantIDs.LOG10E, 'TMath::LogE()'),
]

root_parser = Parser('ROOT', config, constants)
