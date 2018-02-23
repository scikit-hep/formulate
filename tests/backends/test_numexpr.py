# Licensed under a 3-clause BSD style license, see LICENSE.
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

from formulate import Expression, Variable
from formulate import UnnamedConstant as UC
from formulate import from_numexpr, to_numexpr
from formulate.identifiers import IDs

from ..utils import make_check_result


check_result = make_check_result(from_numexpr, to_numexpr)


def _create_test_type(name, A, B, C, D):
    kwargs = {'A': str(A), 'B': str(B), 'C': str(C), 'D': str(D)}

    class NewTestClass(object):
        def test_basic_math(self):
            if isinstance(A, UC):
                # TODO
                pass
            else:
                check_result('+{A}', Expression(IDs.PLUS, A), **kwargs)
                check_result('-{A}', Expression(IDs.MINUS, A), **kwargs)
            check_result('{A} + {B}', Expression(IDs.ADD, A, B), **kwargs)
            check_result('{A} - {B}', Expression(IDs.SUB, A, B), **kwargs)
            check_result('{A} * {B}', Expression(IDs.MUL, A, B), **kwargs)
            check_result('{A} / {B}', Expression(IDs.DIV, A, B), **kwargs)
            check_result('{A} % {B}', Expression(IDs.MOD, A, B), **kwargs)

        def test_chain_math(self):
            check_result('{A} + {B} + {C} + {D}', Expression(IDs.ADD, A, B, C, D), **kwargs)
            check_result('{A} - {B} - {C} - {D}', Expression(IDs.SUB, A, B, C, D), **kwargs)
            check_result('{A} * {B} * {C} * {D}', Expression(IDs.MUL, A, B, C, D), **kwargs)
            check_result('{A} / {B} / {C} / {D}', Expression(IDs.DIV, A, B, C, D), **kwargs)
            check_result('{A} % {B} % {C} % {D}', Expression(IDs.MOD, A, B, C, D), **kwargs)

        def test_basic_boolean_operations(self):
            check_result('~{A}', Expression(IDs.NOT, A), **kwargs)
            check_result('{A} & {B}', Expression(IDs.AND, A, B), **kwargs)
            check_result('{A} | {B}', Expression(IDs.OR, A, B), **kwargs)
            check_result('{A} == {B}', Expression(IDs.EQ, A, B), **kwargs)
            check_result('{A} != {B}', Expression(IDs.NEQ, A, B), **kwargs)
            check_result('{A} > {B}', Expression(IDs.GT, A, B), **kwargs)
            check_result('{A} >= {B}', Expression(IDs.GTEQ, A, B), **kwargs)
            check_result('{A} < {B}', Expression(IDs.LT, A, B), **kwargs)
            check_result('{A} <= {B}', Expression(IDs.LTEQ, A, B), **kwargs)

        # def test_chain_boolean_operations(self):
        #     check_result('{A} & {B} & {C}', Expression(IDs.AND, A, Expression(IDs.AND, B, C)), **kwargs)

        def test_basic_functions(self):
            check_result('sqrt({A})', Expression(IDs.SQRT, A), **kwargs)
            check_result('arctan2({A}, {B})', Expression(IDs.ATAN2, A, B), **kwargs)

        def test_signed_functions(self):
            check_result('sqrt({A})', Expression(IDs.SQRT, A), **kwargs)
            check_result('arctan2({A}, {B})', Expression(IDs.ATAN2, A, B), **kwargs)
            check_result('-sqrt({A})', Expression(IDs.MINUS, Expression(IDs.SQRT, A)), **kwargs)
            check_result('+sqrt({A})', Expression(IDs.PLUS, Expression(IDs.SQRT, A)), **kwargs)
            check_result('- arctan2({A}, {B})', Expression(IDs.MINUS, Expression(IDs.ATAN2, A, B)), **kwargs)
            check_result(' + arctan2({A}, {B})', Expression(IDs.PLUS, Expression(IDs.ATAN2, A, B)), **kwargs)

        def test_math_with_functions(self):
            if isinstance(A, UC):
                # TODO
                pass
            else:
                check_result('sqrt(-{A})', Expression(IDs.SQRT, Expression(IDs.MINUS, A)), **kwargs)
                check_result('sqrt(+ {A})', Expression(IDs.SQRT, Expression(IDs.PLUS, A)), **kwargs)
            check_result('sqrt({A} + {B})', Expression(IDs.SQRT, Expression(IDs.ADD, A, B)), **kwargs)
            check_result('arctan2({A} - {B}, {B} % {A})', Expression(IDs.ATAN2, Expression(IDs.SUB, A, B), Expression(IDs.MOD, B, A)), **kwargs)
            check_result('sqrt({A})+sqrt({B})', Expression(IDs.ADD, Expression(IDs.SQRT, A), Expression(IDs.SQRT, B)), **kwargs)
            check_result('sqrt({A})*sqrt({A})', Expression(IDs.MUL, Expression(IDs.SQRT, A), Expression(IDs.SQRT, A)), **kwargs)
            check_result('arctan2({A}, {B})/sqrt({B})', Expression(IDs.DIV, Expression(IDs.ATAN2, A, B), Expression(IDs.SQRT, B)), **kwargs)

        def test_functions_of_functions(self):
            check_result('sqrt(sqrt({A}))', Expression(IDs.SQRT, Expression(IDs.SQRT, A)), **kwargs)
            check_result('sqrt(arctan2({A}, {B}))', Expression(IDs.SQRT, Expression(IDs.ATAN2, A, B)), **kwargs)
            check_result('arctan2(sqrt({A}), {B})', Expression(IDs.ATAN2, Expression(IDs.SQRT, A), B), **kwargs)

        def test_nested(self):
            check_result('sqrt(-sqrt({A}))', Expression(IDs.SQRT, Expression(IDs.MINUS, Expression(IDs.SQRT, A))), **kwargs)
            check_result('sqrt(sqrt({A}) + {B})', Expression(IDs.SQRT, Expression(IDs.ADD, Expression(IDs.SQRT, A), B)), **kwargs)
            check_result('sqrt(sqrt({A}) + sqrt({B}))', Expression(IDs.SQRT, Expression(IDs.ADD, Expression(IDs.SQRT, A), Expression(IDs.SQRT, B))), **kwargs)

    NewTestClass.__name__ = name

    return NewTestClass


TestPosInts = _create_test_type('TestPosInts', UC('1'), UC('2'), UC('3'), UC('4'))
TestNegInts = _create_test_type('TestNegInts', UC('-1'), UC('-2'), UC('-3'), UC('-4'))
TestMixInts = _create_test_type('TestMixInts', UC('1'), UC('-2'), UC('3'), UC('-4'))

TestPosFloats = _create_test_type('TestPosFloats', UC('1.2'), UC('3.4'), UC('4.5'), UC('6.7'))
TestNegFloats = _create_test_type('TestNegFloats', UC('-1.2'), UC('-3.4'), UC('-4.5'), UC('-6.7'))
TestMixFloats = _create_test_type('TestMixFloats', UC('1.2'), UC('-3.4'), UC('4.5'), UC('-6.7'))

TestPosScientific = _create_test_type('TestPosScientific', UC('1e-2'), UC('3.4e5'), UC('6.7e8'), UC('9e10'))
TestNegScientific = _create_test_type('TestNegScientific', UC('-1e-2'), UC('-3.4e5'), UC('-6.7e8'), UC('-9e10'))
TestMixScientific = _create_test_type('TestMixScientific', UC('1e-2'), UC('-3.4e5'), UC('6.7e8'), UC('-9e10'))

TestVariables = _create_test_type('TestVariables', Variable('A'), Variable('Bee'), Variable('C_is_4'), Variable('_Dxyz'))
