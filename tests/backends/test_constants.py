# Licensed under a 3-clause BSD style license, see LICENSE.
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import pytest

from formulate import from_numexpr, to_numexpr
from formulate import from_root, to_root

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


def create_constant_test(input_string, input_backend='root'):
    assert input_backend in ('root', 'numexpr'), 'Unrecognised backend specified'
    input_from_method = {
        'root': from_root,
        'numexpr': from_numexpr,
    }[input_backend]

    def test_constant():
        expression = input_from_method(input_string)
        root_result = to_root(expression)
        numexpr_result = to_numexpr(expression)
        assert pytest.approx(root_eval(input_string), root_eval(root_result))
        assert pytest.approx(root_eval(root_result), numexpr_eval(numexpr_result))
    return test_constant


# Test basic numexpr constants
test_numexpr_true = create_constant_test('True', input_backend='numexpr')
test_numexpr_false = create_constant_test('False', input_backend='numexpr')

# Test basic ROOT constants
test_true = create_constant_test('true')
test_false = create_constant_test('false')
test_sqrt2_1 = create_constant_test('sqrt2')
test_sqrt2_2 = create_constant_test('TMath::Sqrt2()')
test_e_1 = create_constant_test('e')
test_e_2 = create_constant_test('TMath::E()')
test_pi_1 = create_constant_test('pi')
test_pi_2 = create_constant_test('TMath::Pi()')
test_pi_over_2 = create_constant_test('TMath::PiOver2()')
test_pi_over_4 = create_constant_test('TMath::PiOver4()')
test_two_pi = create_constant_test('TMath::TwoPi()')
test_inv_pi = create_constant_test('TMath::InvPi()')
test_ln10_1 = create_constant_test('ln10')
test_ln10_2 = create_constant_test('TMath::Ln10()')
test_log10e = create_constant_test('TMath::LogE()')
