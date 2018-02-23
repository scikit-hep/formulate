# Licensed under a 3-clause BSD style license, see LICENSE.
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import pytest

from formulate import from_root, to_root
from formulate import from_numexpr, to_numexpr

numexpr = pytest.importorskip("numexpr")
ROOT = pytest.importorskip("ROOT")


def root_eval(string, x=None, y=None, z=None, t=None):
    f = ROOT.TFormula('', string)
    f.Compile()
    if x is None:
        assert y is None and z is None and t is None
        return f.Eval(0)
    elif y is None:
        assert z is None and t is None
        return f.Eval(x)
    elif z is None:
        assert t is None
        return f.Eval(x, y)
    elif t is None:
        return f.Eval(x, y, z)
    else:
        return f.Eval(x, y, z, t)


def numexpr_eval(string, **kwargs):
    return numexpr.evaluate(string, local_dict=kwargs)


def create_formula_test(input_string, input_backend='root', root_raises=None, numexpr_raises=None):
    assert input_backend in ('root', 'numexpr'), 'Unrecognised backend specified'
    input_from_method = {
        'root': from_root,
        'numexpr': from_numexpr,
    }[input_backend]

    def test_constant():
        expression = input_from_method(input_string)

        if input_backend == 'root':
            root_result = to_root(expression)
            assert input_string, root_result

            if numexpr_raises:
                with pytest.raises(numexpr_raises):
                    to_numexpr(expression)
            else:
                numexpr_result = to_numexpr(expression)
                assert pytest.approx(root_eval(root_result), numexpr_eval(numexpr_result))
        else:
            numexpr_result = to_numexpr(expression)
            assert input_string, numexpr_result

            if root_raises:
                with pytest.raises(root_raises):
                    to_root(expression)
            else:
                root_result = to_root(expression)
                assert pytest.approx(numexpr_eval(numexpr_result), root_eval(root_result))

    return test_constant


test_add_root = create_formula_test('3.4 + 5e-7', input_backend='root')
test_add_numexpr = create_formula_test('3.4 + 5e-7', input_backend='numexpr')
test_sub_root = create_formula_test('3.4 - 5e-7', input_backend='root')
test_sub_numexpr = create_formula_test('3.4 - 5e-7', input_backend='numexpr')
test_mul_root = create_formula_test('3.4 * 5e-7', input_backend='root')
test_mul_numexpr = create_formula_test('3.4 * 5e-7', input_backend='numexpr')
test_div_root = create_formula_test('3.4 / 5e-7', input_backend='root')
test_div_numexpr = create_formula_test('3.4 / 5e-7', input_backend='numexpr')
test_mod_root = create_formula_test('3 % 5', input_backend='root')
test_mod_numexpr = create_formula_test('3 % 5', input_backend='numexpr')
test_pow_1_root = create_formula_test('3 ** 5', input_backend='root')
test_pow_1_numexpr = create_formula_test('3 ** 5', input_backend='numexpr')
test_pow_2_root = create_formula_test('3 ** -1.5', input_backend='root')
test_pow_2_numexpr = create_formula_test('3 ** -1.5', input_backend='numexpr')
test_pow_3_root = create_formula_test('3 **2', input_backend='root')
# test_pow_3_numexpr = create_formula_test('3 **2', input_backend='numexpr')
test_lshift_root = create_formula_test('3 << 5', input_backend='root')
test_lshift_numexpr = create_formula_test('3 << 5', input_backend='numexpr')
test_rshift_root = create_formula_test('3 >> 5', input_backend='root')
test_rshift_numexpr = create_formula_test('3 >> 5', input_backend='numexpr')

test_eq_1_root = create_formula_test('3 == 5', input_backend='root')
test_eq_1_numexpr = create_formula_test('3 == 5', input_backend='numexpr')
test_eq_2_root = create_formula_test('3 == 3', input_backend='root')
test_eq_2_numexpr = create_formula_test('3 == 3', input_backend='numexpr')

test_neq_1_root = create_formula_test('3 != 5', input_backend='root')
test_neq_1_numexpr = create_formula_test('3 != 5', input_backend='numexpr')
test_neq_2_root = create_formula_test('3 != 3', input_backend='root')
test_neq_2_numexpr = create_formula_test('3 != 3', input_backend='numexpr')
test_gt_1_root = create_formula_test('3 > 1', input_backend='root')
test_gt_1_numexpr = create_formula_test('3 > 1', input_backend='numexpr')
test_gt_2_root = create_formula_test('3 > 3', input_backend='root')
test_gt_2_numexpr = create_formula_test('3 > 3', input_backend='numexpr')
test_gt_3_root = create_formula_test('5 > 3', input_backend='root')
test_gt_3_numexpr = create_formula_test('5 > 3', input_backend='numexpr')
test_gteq_1_root = create_formula_test('3 >= 1', input_backend='root')
test_gteq_1_numexpr = create_formula_test('3 >= 1', input_backend='numexpr')
test_gteq_2_root = create_formula_test('3 >= 3', input_backend='root')
test_gteq_2_numexpr = create_formula_test('3 >= 3', input_backend='numexpr')
test_gteq_3_root = create_formula_test('5 >= 3', input_backend='root')
test_gteq_3_numexpr = create_formula_test('5 >= 3', input_backend='numexpr')
test_lt_1_root = create_formula_test('3 < 1', input_backend='root')
test_lt_1_numexpr = create_formula_test('3 < 1', input_backend='numexpr')
test_lt_2_root = create_formula_test('3 < 3', input_backend='root')
test_lt_2_numexpr = create_formula_test('3 < 3', input_backend='numexpr')
test_lt_3_root = create_formula_test('5 < 3', input_backend='root')
test_lt_3_numexpr = create_formula_test('5 < 3', input_backend='numexpr')
test_lteq_1_root = create_formula_test('3 <= 1', input_backend='root')
test_lteq_1_numexpr = create_formula_test('3 <= 1', input_backend='numexpr')
test_lteq_2_root = create_formula_test('3 <= 3', input_backend='root')
test_lteq_2_numexpr = create_formula_test('3 <= 3', input_backend='numexpr')
test_lteq_3_root = create_formula_test('5 <= 3', input_backend='root')
test_lteq_3_numexpr = create_formula_test('5 <= 3', input_backend='numexpr')

test_and_1_root = create_formula_test('0 && 0', input_backend='root')
test_and_1_numexpr = create_formula_test('0 & 0', input_backend='numexpr')
test_and_2_root = create_formula_test('0 && 1', input_backend='root')
test_and_2_numexpr = create_formula_test('0 & 1', input_backend='numexpr')
test_and_3_root = create_formula_test('1 && 0', input_backend='root')
test_and_3_numexpr = create_formula_test('1 & 0', input_backend='numexpr')
test_and_4_root = create_formula_test('1 && 1', input_backend='root')
test_and_4_numexpr = create_formula_test('1 & 1', input_backend='numexpr')
test_and_5_root = create_formula_test('3 && 5', input_backend='root')
test_and_5_numexpr = create_formula_test('3 & 5', input_backend='numexpr')

test_or_1_root = create_formula_test('0 || 0', input_backend='root')
test_or_1_numexpr = create_formula_test('0 | 0', input_backend='numexpr')
test_or_2_root = create_formula_test('0 || 1', input_backend='root')
test_or_2_numexpr = create_formula_test('0 | 1', input_backend='numexpr')
test_or_3_root = create_formula_test('1 || 0', input_backend='root')
test_or_3_numexpr = create_formula_test('1 | 0', input_backend='numexpr')
test_or_4_root = create_formula_test('1 || 1', input_backend='root')
test_or_4_numexpr = create_formula_test('1 | 1', input_backend='numexpr')
test_or_5_root = create_formula_test('3 || 5', input_backend='root')
test_or_5_numexpr = create_formula_test('3 | 5', input_backend='numexpr')

test_xor_1_root = create_formula_test('0 ^ 0', input_backend='root')
test_xor_1_numexpr = create_formula_test('0 ^ 0', input_backend='numexpr')
test_xor_2_root = create_formula_test('0 ^ 1', input_backend='root')
test_xor_2_numexpr = create_formula_test('0 ^ 1', input_backend='numexpr')
test_xor_3_root = create_formula_test('1 ^ 0', input_backend='root')
test_xor_3_numexpr = create_formula_test('1 ^ 0', input_backend='numexpr')
test_xor_4_root = create_formula_test('1 ^ 1', input_backend='root')
test_xor_4_numexpr = create_formula_test('1 ^ 1', input_backend='numexpr')
test_xor_5_root = create_formula_test('3 ^ 5', input_backend='root')
test_xor_5_numexpr = create_formula_test('3 ^ 5', input_backend='numexpr')

test_not_1_root = create_formula_test('!0', input_backend='root')
test_not_1_numexpr = create_formula_test('~0', input_backend='numexpr')
test_not_2_root = create_formula_test('!1', input_backend='root')
test_not_2_numexpr = create_formula_test('~1', input_backend='numexpr')
test_not_3_root = create_formula_test('!0', input_backend='root')
test_not_3_numexpr = create_formula_test('~0', input_backend='numexpr')
test_not_4_root = create_formula_test('!1', input_backend='root')
test_not_4_numexpr = create_formula_test('~1', input_backend='numexpr')
test_not_5_root = create_formula_test('!5', input_backend='root')
test_not_5_numexpr = create_formula_test('~5', input_backend='numexpr')
