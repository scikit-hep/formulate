# Licensed under a 3-clause BSD style license, see LICENSE.
from __future__ import absolute_import, division, print_function

import sys

import numpy as np
import pytest

from formulate import from_numexpr, from_root, Expression, Variable, NamedConstant as NC, UnnamedConstant as UC
from formulate.identifiers import IDs, ConstantIDs
from .utils import assert_equal_expressions as aee


def test_get_variables():
    assert from_root('pi').variables == set()
    assert from_numexpr('2').variables == set()
    assert from_numexpr('2e-3').variables == set()
    assert from_numexpr('A').variables == {'A'}
    assert from_numexpr('A + A').variables == {'A'}
    assert from_numexpr('A + B').variables == {'A', 'B'}
    assert from_numexpr('A + A*A - 3e7').variables == {'A'}
    assert from_numexpr('arctan2(A, A)').variables == {'A'}
    assert from_numexpr('arctan2(A, B)').variables == {'A', 'B'}
    assert from_root('arctan2(A, pi)').variables == {'A'}
    assert from_numexpr('arctan2(arctan2(A, B), C)').variables == {'A', 'B', 'C'}
    for base, expect in [(UC('2'), set()), (Variable('A'), {'A'}), (NC(ConstantIDs.PI), set())]:
        expr = base
        for i in list(range(100)):
            expr = Expression(IDs.SQRT, expr)
        assert expr.variables == expect


def test_named_constants():
    assert from_root('pi').named_constants == {'PI'}
    assert from_numexpr('2').named_constants == set()
    assert from_numexpr('2e-3').named_constants == set()
    assert from_numexpr('A').named_constants == set()
    assert from_numexpr('A + A').named_constants == set()
    assert from_numexpr('A + B').named_constants == set()
    assert from_numexpr('A + A*A - 3e7').named_constants == set()
    assert from_numexpr('arctan2(A, A)').named_constants == set()
    assert from_numexpr('arctan2(A, B)').named_constants == set()
    assert from_root('arctan2(A, pi)').named_constants == {'PI'}
    assert from_numexpr('arctan2(arctan2(A, B), C)').named_constants == set()
    for base, expect in [(UC('2'), set()), (Variable('A'), set()), (NC(ConstantIDs.PI), {'PI'})]:
        expr = base
        for i in list(range(100)):
            expr = Expression(IDs.SQRT, expr)
        assert expr.named_constants == expect


def test_unnamed_constants():
    assert from_root('pi').unnamed_constants == set()
    assert from_numexpr('2').unnamed_constants == {'2'}
    assert from_numexpr('2e-3').unnamed_constants == {'2e-3'}
    assert from_numexpr('A').unnamed_constants == set()
    assert from_numexpr('A + A').unnamed_constants == set()
    assert from_numexpr('A + B').unnamed_constants == set()
    assert from_numexpr('A + A*A - 3e7').unnamed_constants == {'3e7'}
    assert from_numexpr('arctan2(A, A)').unnamed_constants == set()
    assert from_numexpr('arctan2(A, B)').unnamed_constants == set()
    assert from_root('arctan2(A, pi)').unnamed_constants == set()
    assert from_numexpr('arctan2(arctan2(A, B), C)').unnamed_constants == set()
    for base, expect in [(UC('2'), {'2'}), (Variable('A'), set()), (NC(ConstantIDs.PI), set())]:
        expr = base
        for i in list(range(100)):
            expr = Expression(IDs.SQRT, expr)
        assert expr.unnamed_constants == expect


def test_addition():
    aee(Expression(IDs.SQRT, UC('2')) + Expression(IDs.SQRT, UC('3')),
        Expression(IDs.ADD, Expression(IDs.SQRT, UC('2')), Expression(IDs.SQRT, UC('3'))))
    aee(Expression(IDs.SQRT, UC('2')) + UC('3'),
        Expression(IDs.ADD, Expression(IDs.SQRT, UC('2')), UC('3')))
    aee(UC('3') + Expression(IDs.SQRT, UC('2')),
        Expression(IDs.ADD, UC('3'), Expression(IDs.SQRT, UC('2'))))

    expression = Expression(IDs.SQRT, UC('2'))
    expression += Expression(IDs.SQRT, UC('3'))
    aee(expression, Expression(IDs.ADD, Expression(IDs.SQRT, UC('2')), Expression(IDs.SQRT, UC('3'))))
    expression = Expression(IDs.SQRT, UC('2'))
    expression += UC('3')
    aee(expression, Expression(IDs.ADD, Expression(IDs.SQRT, UC('2')), UC('3')))
    expression = UC('3')
    expression += Expression(IDs.SQRT, UC('2'))
    aee(expression, Expression(IDs.ADD, UC('3'), Expression(IDs.SQRT, UC('2'))))

    aee(np.add(Expression(IDs.SQRT, UC('2')), Expression(IDs.SQRT, UC('3'))),
        Expression(IDs.ADD, Expression(IDs.SQRT, UC('2')), Expression(IDs.SQRT, UC('3'))))
    aee(np.add(Expression(IDs.SQRT, UC('2')), UC('3')),
        Expression(IDs.ADD, Expression(IDs.SQRT, UC('2')), UC('3')))
    aee(np.add(UC('3'), Expression(IDs.SQRT, UC('2'))),
        Expression(IDs.ADD, UC('3'), Expression(IDs.SQRT, UC('2'))))


def test_subtraction():
    aee(Expression(IDs.SQRT, UC('2')) - Expression(IDs.SQRT, UC('3')),
        Expression(IDs.SUB, Expression(IDs.SQRT, UC('2')), Expression(IDs.SQRT, UC('3'))))
    expression = Expression(IDs.SQRT, UC('2'))
    expression -= Expression(IDs.SQRT, UC('3'))
    aee(expression, Expression(IDs.SUB, Expression(IDs.SQRT, UC('2')), Expression(IDs.SQRT, UC('3'))))
    aee(np.subtract(Expression(IDs.SQRT, UC('2')), Expression(IDs.SQRT, UC('3'))),
        Expression(IDs.SUB, Expression(IDs.SQRT, UC('2')), Expression(IDs.SQRT, UC('3'))))


def test_multiplication():
    aee(Expression(IDs.SQRT, UC('2')) * Expression(IDs.SQRT, UC('3')),
        Expression(IDs.MUL, Expression(IDs.SQRT, UC('2')), Expression(IDs.SQRT, UC('3'))))
    expression = Expression(IDs.SQRT, UC('2'))
    expression *= Expression(IDs.SQRT, UC('3'))
    aee(expression, Expression(IDs.MUL, Expression(IDs.SQRT, UC('2')), Expression(IDs.SQRT, UC('3'))))
    aee(np.multiply(Expression(IDs.SQRT, UC('2')), Expression(IDs.SQRT, UC('3'))),
        Expression(IDs.MUL, Expression(IDs.SQRT, UC('2')), Expression(IDs.SQRT, UC('3'))))


@pytest.mark.skipif(sys.version_info.major < 3, reason="Python < 3 not supported for division.")
def test_division():
    aee(Expression(IDs.SQRT, UC('2')) / Expression(IDs.SQRT, UC('3')),
        Expression(IDs.DIV, Expression(IDs.SQRT, UC('2')), Expression(IDs.SQRT, UC('3'))))
    expression = Expression(IDs.SQRT, UC('2'))
    expression /= Expression(IDs.SQRT, UC('3'))
    aee(expression, Expression(IDs.DIV, Expression(IDs.SQRT, UC('2')), Expression(IDs.SQRT, UC('3'))))
    aee(np.divide(Expression(IDs.SQRT, UC('2')), Expression(IDs.SQRT, UC('3'))),
        Expression(IDs.DIV, Expression(IDs.SQRT, UC('2')), Expression(IDs.SQRT, UC('3'))))


def test_power():
    aee(Expression(IDs.SQRT, UC('2')) ** Expression(IDs.SQRT, UC('3')),
        Expression(IDs.POW, Expression(IDs.SQRT, UC('2')), Expression(IDs.SQRT, UC('3'))))
    expression = Expression(IDs.SQRT, UC('2'))
    expression **= Expression(IDs.SQRT, UC('3'))
    aee(expression, Expression(IDs.POW, Expression(IDs.SQRT, UC('2')), Expression(IDs.SQRT, UC('3'))))
    aee(np.power(Expression(IDs.SQRT, UC('2')), Expression(IDs.SQRT, UC('3'))),
        Expression(IDs.POW, Expression(IDs.SQRT, UC('2')), Expression(IDs.SQRT, UC('3'))))


def test_mod():
    aee(Expression(IDs.SQRT, UC('2')) % Expression(IDs.SQRT, UC('3')),
        Expression(IDs.MOD, Expression(IDs.SQRT, UC('2')), Expression(IDs.SQRT, UC('3'))))
    expression = Expression(IDs.SQRT, UC('2'))
    expression %= Expression(IDs.SQRT, UC('3'))
    aee(expression, Expression(IDs.MOD, Expression(IDs.SQRT, UC('2')), Expression(IDs.SQRT, UC('3'))))
    aee(np.mod(Expression(IDs.SQRT, UC('2')), Expression(IDs.SQRT, UC('3'))),
        Expression(IDs.MOD, Expression(IDs.SQRT, UC('2')), Expression(IDs.SQRT, UC('3'))))


def test_and():
    aee(Expression(IDs.SQRT, UC('2')) & Expression(IDs.SQRT, UC('3')),
        Expression(IDs.AND, Expression(IDs.SQRT, UC('2')), Expression(IDs.SQRT, UC('3'))))
    expression = Expression(IDs.SQRT, UC('2'))
    expression &= Expression(IDs.SQRT, UC('3'))
    aee(expression, Expression(IDs.AND, Expression(IDs.SQRT, UC('2')), Expression(IDs.SQRT, UC('3'))))
    aee(np.bitwise_and(Expression(IDs.SQRT, UC('2')), Expression(IDs.SQRT, UC('3'))),
        Expression(IDs.AND, Expression(IDs.SQRT, UC('2')), Expression(IDs.SQRT, UC('3'))))


def test_or():
    aee(Expression(IDs.SQRT, UC('2')) | Expression(IDs.SQRT, UC('3')),
        Expression(IDs.OR, Expression(IDs.SQRT, UC('2')), Expression(IDs.SQRT, UC('3'))))
    expression = Expression(IDs.SQRT, UC('2'))
    expression |= Expression(IDs.SQRT, UC('3'))
    aee(expression, Expression(IDs.OR, Expression(IDs.SQRT, UC('2')), Expression(IDs.SQRT, UC('3'))))
    aee(np.bitwise_or(Expression(IDs.SQRT, UC('2')), Expression(IDs.SQRT, UC('3'))),
        Expression(IDs.OR, Expression(IDs.SQRT, UC('2')), Expression(IDs.SQRT, UC('3'))))


def test_xor():
    aee(Expression(IDs.SQRT, UC('2')) ^ Expression(IDs.SQRT, UC('3')),
        Expression(IDs.XOR, Expression(IDs.SQRT, UC('2')), Expression(IDs.SQRT, UC('3'))))
    expression = Expression(IDs.SQRT, UC('2'))
    expression ^= Expression(IDs.SQRT, UC('3'))
    aee(expression, Expression(IDs.XOR, Expression(IDs.SQRT, UC('2')), Expression(IDs.SQRT, UC('3'))))
    aee(np.bitwise_xor(Expression(IDs.SQRT, UC('2')), Expression(IDs.SQRT, UC('3'))),
        Expression(IDs.XOR, Expression(IDs.SQRT, UC('2')), Expression(IDs.SQRT, UC('3'))))


def test_left_shift():
    aee(Expression(IDs.SQRT, UC('2')) << Expression(IDs.SQRT, UC('3')),
        Expression(IDs.LSHIFT, Expression(IDs.SQRT, UC('2')), Expression(IDs.SQRT, UC('3'))))
    expression = Expression(IDs.SQRT, UC('2'))
    expression <<= Expression(IDs.SQRT, UC('3'))
    aee(expression, Expression(IDs.LSHIFT, Expression(IDs.SQRT, UC('2')), Expression(IDs.SQRT, UC('3'))))
    aee(np.left_shift(Expression(IDs.SQRT, UC('2')), Expression(IDs.SQRT, UC('3'))),
        Expression(IDs.LSHIFT, Expression(IDs.SQRT, UC('2')), Expression(IDs.SQRT, UC('3'))))


def test_right_shift():
    aee(Expression(IDs.SQRT, UC('2')) >> Expression(IDs.SQRT, UC('3')),
        Expression(IDs.RSHIFT, Expression(IDs.SQRT, UC('2')), Expression(IDs.SQRT, UC('3'))))
    expression = Expression(IDs.SQRT, UC('2'))
    expression >>= Expression(IDs.SQRT, UC('3'))
    aee(expression, Expression(IDs.RSHIFT, Expression(IDs.SQRT, UC('2')), Expression(IDs.SQRT, UC('3'))))
    aee(np.right_shift(Expression(IDs.SQRT, UC('2')), Expression(IDs.SQRT, UC('3'))),
        Expression(IDs.RSHIFT, Expression(IDs.SQRT, UC('2')), Expression(IDs.SQRT, UC('3'))))


def test_negative():
    aee(-Expression(IDs.SQRT, UC('2')),
        Expression(IDs.MINUS, Expression(IDs.SQRT, UC('2'))))


def test_positive():
    aee(+Expression(IDs.SQRT, UC('2')),
        Expression(IDs.PLUS, Expression(IDs.SQRT, UC('2'))))


def test_not():
    aee(~Expression(IDs.SQRT, UC('2')),
        Expression(IDs.NOT, Expression(IDs.SQRT, UC('2'))))


def test_abs():
    aee(abs(Expression(IDs.SQRT, UC('2'))),
        Expression(IDs.ABS, Expression(IDs.SQRT, UC('2'))))
    aee(np.abs(Expression(IDs.SQRT, UC('2'))),
        Expression(IDs.ABS, Expression(IDs.SQRT, UC('2'))))


def test_equals():
    aee(Expression(IDs.SQRT, UC('2')) == Expression(IDs.SQRT, UC('3')),
        Expression(IDs.EQ, Expression(IDs.SQRT, UC('2')), Expression(IDs.SQRT, UC('3'))))


def test_not_equals():
    aee(Expression(IDs.SQRT, UC('2')) != Expression(IDs.SQRT, UC('3')),
        Expression(IDs.NEQ, Expression(IDs.SQRT, UC('2')), Expression(IDs.SQRT, UC('3'))))


def test_greater_than():
    aee(Expression(IDs.SQRT, UC('2')) > Expression(IDs.SQRT, UC('3')),
        Expression(IDs.GT, Expression(IDs.SQRT, UC('2')), Expression(IDs.SQRT, UC('3'))))


def test_greater_than_or_equal():
    aee(Expression(IDs.SQRT, UC('2')) >= Expression(IDs.SQRT, UC('3')),
        Expression(IDs.GTEQ, Expression(IDs.SQRT, UC('2')), Expression(IDs.SQRT, UC('3'))))


def test_less_than():
    aee(Expression(IDs.SQRT, UC('2')) < Expression(IDs.SQRT, UC('3')),
        Expression(IDs.LT, Expression(IDs.SQRT, UC('2')), Expression(IDs.SQRT, UC('3'))))


def test_less_than_or_equal():
    aee(Expression(IDs.SQRT, UC('2')) <= Expression(IDs.SQRT, UC('3')),
        Expression(IDs.LTEQ, Expression(IDs.SQRT, UC('2')), Expression(IDs.SQRT, UC('3'))))


# TODO where


def test_sin():
    aee(np.sin(Expression(IDs.SQRT, UC('2'))),
        Expression(IDs.SIN, Expression(IDs.SQRT, UC('2'))))


def test_cos():
    aee(np.cos(Expression(IDs.SQRT, UC('2'))),
        Expression(IDs.COS, Expression(IDs.SQRT, UC('2'))))


def test_tan():
    aee(np.tan(Expression(IDs.SQRT, UC('2'))),
        Expression(IDs.TAN, Expression(IDs.SQRT, UC('2'))))


def test_arcsin():
    aee(np.arcsin(Expression(IDs.SQRT, UC('2'))),
        Expression(IDs.ASIN, Expression(IDs.SQRT, UC('2'))))


def test_arccos():
    aee(np.arccos(Expression(IDs.SQRT, UC('2'))),
        Expression(IDs.ACOS, Expression(IDs.SQRT, UC('2'))))


def test_arctan():
    aee(np.arctan(Expression(IDs.SQRT, UC('2'))),
        Expression(IDs.ATAN, Expression(IDs.SQRT, UC('2'))))


def test_arctan2():
    aee(np.arctan2(Expression(IDs.SQRT, UC('2')), Expression(IDs.SQRT, UC('3'))),
        Expression(IDs.ATAN2, Expression(IDs.SQRT, UC('2')), Expression(IDs.SQRT, UC('3'))))


def test_sinh():
    aee(np.sinh(Expression(IDs.SQRT, UC('2'))),
        Expression(IDs.ASINH, Expression(IDs.SQRT, UC('2'))))


def test_cosh():
    aee(np.cosh(Expression(IDs.SQRT, UC('2'))),
        Expression(IDs.COSH, Expression(IDs.SQRT, UC('2'))))


def test_tanh():
    aee(np.tanh(Expression(IDs.SQRT, UC('2'))),
        Expression(IDs.TANH, Expression(IDs.SQRT, UC('2'))))


def test_arcsinh():
    aee(np.arcsinh(Expression(IDs.SQRT, UC('2'))),
        Expression(IDs.ASINH, Expression(IDs.SQRT, UC('2'))))


def test_arccosh():
    aee(np.arccosh(Expression(IDs.SQRT, UC('2'))),
        Expression(IDs.ACOSH, Expression(IDs.SQRT, UC('2'))))


def test_arctanh():
    aee(np.arctanh(Expression(IDs.SQRT, UC('2'))),
        Expression(IDs.ATANH, Expression(IDs.SQRT, UC('2'))))


def test_log():
    aee(np.log(Expression(IDs.SQRT, UC('2'))),
        Expression(IDs.LOG, Expression(IDs.SQRT, UC('2'))))


def test_log10():
    aee(np.log10(Expression(IDs.SQRT, UC('2'))),
        Expression(IDs.LOG10, Expression(IDs.SQRT, UC('2'))))


def test_log1p():
    aee(np.log1p(Expression(IDs.SQRT, UC('2'))),
        Expression(IDs.LOG1p, Expression(IDs.SQRT, UC('2'))))


def test_exp():
    aee(np.exp(Expression(IDs.SQRT, UC('2'))),
        Expression(IDs.EXP, Expression(IDs.SQRT, UC('2'))))


def test_expm1():
    aee(np.expm1(Expression(IDs.SQRT, UC('2'))),
        Expression(IDs.EXPM1, Expression(IDs.SQRT, UC('2'))))


def test_sqrt():
    aee(np.sqrt(Expression(IDs.SQRT, UC('2'))),
        Expression(IDs.SQRT, Expression(IDs.SQRT, UC('2'))))
