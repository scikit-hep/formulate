# Licensed under a 3-clause BSD style license, see LICENSE.
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import numpy as np

from formulate import Expression
from formulate.identifiers import IDs

from .utils import assert_equal_expressions as aee


def test_addition():
    aee(Expression(IDs.SQRT, 2) + Expression(IDs.SQRT, 3),
        Expression(IDs.ADD, Expression(IDs.SQRT, 2), Expression(IDs.SQRT, 3)))
    aee(Expression(IDs.SQRT, 2) + 3,
        Expression(IDs.ADD, Expression(IDs.SQRT, 2), 3))
    aee(3 + Expression(IDs.SQRT, 2),
        Expression(IDs.ADD, 3, Expression(IDs.SQRT, 2)))

    expression = Expression(IDs.SQRT, 2)
    expression += Expression(IDs.SQRT, 3)
    aee(expression, Expression(IDs.ADD, Expression(IDs.SQRT, 2), Expression(IDs.SQRT, 3)))
    expression = Expression(IDs.SQRT, 2)
    expression += 3
    aee(expression, Expression(IDs.ADD, Expression(IDs.SQRT, 2), 3))
    expression = 3
    expression += Expression(IDs.SQRT, 2)
    aee(expression, Expression(IDs.ADD, 3, Expression(IDs.SQRT, 2)))

    aee(np.add(Expression(IDs.SQRT, 2), Expression(IDs.SQRT, 3)),
        Expression(IDs.ADD, Expression(IDs.SQRT, 2), Expression(IDs.SQRT, 3)))
    aee(np.add(Expression(IDs.SQRT, 2), 3),
        Expression(IDs.ADD, Expression(IDs.SQRT, 2), 3))
    aee(np.add(3, Expression(IDs.SQRT, 2)),
        Expression(IDs.ADD, 3, Expression(IDs.SQRT, 2)))


def test_subtraction():
    aee(Expression(IDs.SQRT, 2) - Expression(IDs.SQRT, 3),
        Expression(IDs.SUB, Expression(IDs.SQRT, 2), Expression(IDs.SQRT, 3)))
    expression = Expression(IDs.SQRT, 2)
    expression -= Expression(IDs.SQRT, 3)
    aee(expression, Expression(IDs.SUB, Expression(IDs.SQRT, 2), Expression(IDs.SQRT, 3)))
    aee(np.subtract(Expression(IDs.SQRT, 2), Expression(IDs.SQRT, 3)),
        Expression(IDs.SUB, Expression(IDs.SQRT, 2), Expression(IDs.SQRT, 3)))


def test_multiplication():
    aee(Expression(IDs.SQRT, 2) * Expression(IDs.SQRT, 3),
        Expression(IDs.MUL, Expression(IDs.SQRT, 2), Expression(IDs.SQRT, 3)))
    expression = Expression(IDs.SQRT, 2)
    expression *= Expression(IDs.SQRT, 3)
    aee(expression, Expression(IDs.MUL, Expression(IDs.SQRT, 2), Expression(IDs.SQRT, 3)))
    aee(np.multiply(Expression(IDs.SQRT, 2), Expression(IDs.SQRT, 3)),
        Expression(IDs.MUL, Expression(IDs.SQRT, 2), Expression(IDs.SQRT, 3)))


# TODO Handle division


def test_power():
    aee(Expression(IDs.SQRT, 2)**Expression(IDs.SQRT, 3),
        Expression(IDs.POW, Expression(IDs.SQRT, 2), Expression(IDs.SQRT, 3)))
    expression = Expression(IDs.SQRT, 2)
    expression **= Expression(IDs.SQRT, 3)
    aee(expression, Expression(IDs.POW, Expression(IDs.SQRT, 2), Expression(IDs.SQRT, 3)))
    aee(np.power(Expression(IDs.SQRT, 2), Expression(IDs.SQRT, 3)),
        Expression(IDs.POW, Expression(IDs.SQRT, 2), Expression(IDs.SQRT, 3)))


def test_mod():
    aee(Expression(IDs.SQRT, 2) % Expression(IDs.SQRT, 3),
        Expression(IDs.MOD, Expression(IDs.SQRT, 2), Expression(IDs.SQRT, 3)))
    expression = Expression(IDs.SQRT, 2)
    expression %= Expression(IDs.SQRT, 3)
    aee(expression, Expression(IDs.MOD, Expression(IDs.SQRT, 2), Expression(IDs.SQRT, 3)))
    aee(np.mod(Expression(IDs.SQRT, 2), Expression(IDs.SQRT, 3)),
        Expression(IDs.MOD, Expression(IDs.SQRT, 2), Expression(IDs.SQRT, 3)))


def test_and():
    aee(Expression(IDs.SQRT, 2) & Expression(IDs.SQRT, 3),
        Expression(IDs.AND, Expression(IDs.SQRT, 2), Expression(IDs.SQRT, 3)))
    expression = Expression(IDs.SQRT, 2)
    expression &= Expression(IDs.SQRT, 3)
    aee(expression, Expression(IDs.AND, Expression(IDs.SQRT, 2), Expression(IDs.SQRT, 3)))
    aee(np.bitwise_and(Expression(IDs.SQRT, 2), Expression(IDs.SQRT, 3)),
        Expression(IDs.AND, Expression(IDs.SQRT, 2), Expression(IDs.SQRT, 3)))


def test_or():
    aee(Expression(IDs.SQRT, 2) | Expression(IDs.SQRT, 3),
        Expression(IDs.OR, Expression(IDs.SQRT, 2), Expression(IDs.SQRT, 3)))
    expression = Expression(IDs.SQRT, 2)
    expression |= Expression(IDs.SQRT, 3)
    aee(expression, Expression(IDs.OR, Expression(IDs.SQRT, 2), Expression(IDs.SQRT, 3)))
    aee(np.bitwise_or(Expression(IDs.SQRT, 2), Expression(IDs.SQRT, 3)),
        Expression(IDs.OR, Expression(IDs.SQRT, 2), Expression(IDs.SQRT, 3)))


def test_xor():
    aee(Expression(IDs.SQRT, 2) ^ Expression(IDs.SQRT, 3),
        Expression(IDs.XOR, Expression(IDs.SQRT, 2), Expression(IDs.SQRT, 3)))
    expression = Expression(IDs.SQRT, 2)
    expression ^= Expression(IDs.SQRT, 3)
    aee(expression, Expression(IDs.XOR, Expression(IDs.SQRT, 2), Expression(IDs.SQRT, 3)))
    aee(np.bitwise_xor(Expression(IDs.SQRT, 2), Expression(IDs.SQRT, 3)),
        Expression(IDs.XOR, Expression(IDs.SQRT, 2), Expression(IDs.SQRT, 3)))


def test_left_shift():
    aee(Expression(IDs.SQRT, 2) << Expression(IDs.SQRT, 3),
        Expression(IDs.LSHIFT, Expression(IDs.SQRT, 2), Expression(IDs.SQRT, 3)))
    expression = Expression(IDs.SQRT, 2)
    expression <<= Expression(IDs.SQRT, 3)
    aee(expression, Expression(IDs.LSHIFT, Expression(IDs.SQRT, 2), Expression(IDs.SQRT, 3)))
    aee(np.left_shift(Expression(IDs.SQRT, 2), Expression(IDs.SQRT, 3)),
        Expression(IDs.LSHIFT, Expression(IDs.SQRT, 2), Expression(IDs.SQRT, 3)))


def test_right_shift():
    aee(Expression(IDs.SQRT, 2) >> Expression(IDs.SQRT, 3),
        Expression(IDs.RSHIFT, Expression(IDs.SQRT, 2), Expression(IDs.SQRT, 3)))
    expression = Expression(IDs.SQRT, 2)
    expression >>= Expression(IDs.SQRT, 3)
    aee(expression, Expression(IDs.RSHIFT, Expression(IDs.SQRT, 2), Expression(IDs.SQRT, 3)))
    aee(np.right_shift(Expression(IDs.SQRT, 2), Expression(IDs.SQRT, 3)),
        Expression(IDs.RSHIFT, Expression(IDs.SQRT, 2), Expression(IDs.SQRT, 3)))


def test_negative():
    aee(-Expression(IDs.SQRT, 2),
        Expression(IDs.MINUS, Expression(IDs.SQRT, 2)))


def test_positive():
    aee(+Expression(IDs.SQRT, 2),
        Expression(IDs.PLUS, Expression(IDs.SQRT, 2)))


def test_not():
    aee(~Expression(IDs.SQRT, 2),
        Expression(IDs.NOT, Expression(IDs.SQRT, 2)))


def test_abs():
    aee(abs(Expression(IDs.SQRT, 2)),
        Expression(IDs.ABS, Expression(IDs.SQRT, 2)))
    aee(np.abs(Expression(IDs.SQRT, 2)),
        Expression(IDs.ABS, Expression(IDs.SQRT, 2)))


def test_equals():
    aee(Expression(IDs.SQRT, 2) == Expression(IDs.SQRT, 3),
        Expression(IDs.EQ, Expression(IDs.SQRT, 2), Expression(IDs.SQRT, 3)))


def test_not_equals():
    aee(Expression(IDs.SQRT, 2) != Expression(IDs.SQRT, 3),
        Expression(IDs.NEQ, Expression(IDs.SQRT, 2), Expression(IDs.SQRT, 3)))


def test_greater_than():
    aee(Expression(IDs.SQRT, 2) > Expression(IDs.SQRT, 3),
        Expression(IDs.GT, Expression(IDs.SQRT, 2), Expression(IDs.SQRT, 3)))


def test_greater_than_or_equal():
    aee(Expression(IDs.SQRT, 2) >= Expression(IDs.SQRT, 3),
        Expression(IDs.GTEQ, Expression(IDs.SQRT, 2), Expression(IDs.SQRT, 3)))


def test_less_than():
    aee(Expression(IDs.SQRT, 2) < Expression(IDs.SQRT, 3),
        Expression(IDs.LT, Expression(IDs.SQRT, 2), Expression(IDs.SQRT, 3)))


def test_less_than_or_equal():
    aee(Expression(IDs.SQRT, 2) <= Expression(IDs.SQRT, 3),
        Expression(IDs.LTEQ, Expression(IDs.SQRT, 2), Expression(IDs.SQRT, 3)))


# TODO where


def test_sin():
    aee(np.sin(Expression(IDs.SQRT, 2)),
        Expression(IDs.SIN, Expression(IDs.SQRT, 2)))


def test_cos():
    aee(np.cos(Expression(IDs.SQRT, 2)),
        Expression(IDs.COS, Expression(IDs.SQRT, 2)))


def test_tan():
    aee(np.tan(Expression(IDs.SQRT, 2)),
        Expression(IDs.TAN, Expression(IDs.SQRT, 2)))


def test_arcsin():
    aee(np.arcsin(Expression(IDs.SQRT, 2)),
        Expression(IDs.ASIN, Expression(IDs.SQRT, 2)))


def test_arccos():
    aee(np.arccos(Expression(IDs.SQRT, 2)),
        Expression(IDs.ACOS, Expression(IDs.SQRT, 2)))


def test_arctan():
    aee(np.arctan(Expression(IDs.SQRT, 2)),
        Expression(IDs.ATAN, Expression(IDs.SQRT, 2)))


def test_arctan2():
    aee(np.arctan2(Expression(IDs.SQRT, 2), Expression(IDs.SQRT, 3)),
        Expression(IDs.ATAN2, Expression(IDs.SQRT, 2), Expression(IDs.SQRT, 3)))


def test_sinh():
    aee(np.sinh(Expression(IDs.SQRT, 2)),
        Expression(IDs.ASINH, Expression(IDs.SQRT, 2)))


def test_cosh():
    aee(np.cosh(Expression(IDs.SQRT, 2)),
        Expression(IDs.COSH, Expression(IDs.SQRT, 2)))


def test_tanh():
    aee(np.tanh(Expression(IDs.SQRT, 2)),
        Expression(IDs.TANH, Expression(IDs.SQRT, 2)))


def test_arcsinh():
    aee(np.arcsinh(Expression(IDs.SQRT, 2)),
        Expression(IDs.ASINH, Expression(IDs.SQRT, 2)))


def test_arccosh():
    aee(np.arccosh(Expression(IDs.SQRT, 2)),
        Expression(IDs.ACOSH, Expression(IDs.SQRT, 2)))


def test_arctanh():
    aee(np.arctanh(Expression(IDs.SQRT, 2)),
        Expression(IDs.ATANH, Expression(IDs.SQRT, 2)))


def test_log():
    aee(np.log(Expression(IDs.SQRT, 2)),
        Expression(IDs.LOG, Expression(IDs.SQRT, 2)))


def test_log10():
    aee(np.log10(Expression(IDs.SQRT, 2)),
        Expression(IDs.LOG10, Expression(IDs.SQRT, 2)))


def test_log1p():
    aee(np.log1p(Expression(IDs.SQRT, 2)),
        Expression(IDs.LOG1p, Expression(IDs.SQRT, 2)))


def test_exp():
    aee(np.exp(Expression(IDs.SQRT, 2)),
        Expression(IDs.EXP, Expression(IDs.SQRT, 2)))


def test_expm1():
    aee(np.expm1(Expression(IDs.SQRT, 2)),
        Expression(IDs.EXPM1, Expression(IDs.SQRT, 2)))


def test_sqrt():
    aee(np.sqrt(Expression(IDs.SQRT, 2)),
        Expression(IDs.SQRT, Expression(IDs.SQRT, 2)))
