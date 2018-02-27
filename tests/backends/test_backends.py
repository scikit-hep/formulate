# Licensed under a 3-clause BSD style license, see LICENSE.
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import pytest
import numpy as np
import numexpr

from formulate import from_auto, from_numexpr, to_numexpr, from_root, to_root

from ..utils import assert_equal_expressions


def do_checks(numexpr_input, root_input):
    def test():
        root_expression = from_root(root_input)
        numexpr_expression = from_numexpr(numexpr_input)
        assert_equal_expressions(root_expression, numexpr_expression)
        assert to_numexpr(root_expression) == to_numexpr(numexpr_expression)
        assert to_root(root_expression) == to_root(numexpr_expression)
        assert root_expression.to_numexpr() == numexpr_expression.to_numexpr()
        assert root_expression.to_root() == numexpr_expression.to_root()

    return test


test_001 = do_checks('True', 'true')
test_002 = do_checks('False', 'false')
test_003 = do_checks('sqrt(2)', 'sqrt(2)')
test_004 = do_checks('sqrt(2)', 'TMath::Sqrt(2)')
test_005 = do_checks('sqrt(abs(-4))', 'TMath::Sqrt(TMath::Abs(-4))')
test_006 = do_checks('A & B & C & D', 'A && B && C && D')
test_007 = do_checks('A & B | C & D', 'A && B || C && D')
test_008 = do_checks('A & ~B | C & D', 'A && !B || C && D')


def test_readme():
    momentum = from_root('TMath::Sqrt(X_PX**2 + X_PY**2 + X_PZ**2)')
    assert momentum.to_numexpr() == 'sqrt(((X_PX ** 2) + (X_PY ** 2) + (X_PZ ** 2)))'
    assert momentum.to_root() == 'TMath::Sqrt(((X_PX ** 2) + (X_PY ** 2) + (X_PZ ** 2)))'
    my_selection = from_numexpr('X_PT > 5 & (Mu_NHits > 3 | Mu_PT > 10)')
    assert my_selection.to_root() == '(X_PT > 5) && ((Mu_NHits > 3) || (Mu_PT > 10))'
    assert my_selection.to_numexpr() == '(X_PT > 5) & ((Mu_NHits > 3) | (Mu_PT > 10))'
    my_sum = from_auto('True + False')
    assert my_sum.to_root() == 'true + false'
    assert my_sum.to_numexpr() == 'True + False'
    my_check = from_auto('(X_THETA*TMath::DegToRad() > pi/4) && D_PE > 9.2')
    assert my_check.variables == {'D_PE', 'X_THETA'}
    assert my_check.named_constants == {'DEG2RAD', 'PI'}
    assert my_check.unnamed_constants == {'4', '9.2'}
    new_selection = (momentum > 100) and (my_check or (np.sqrt(my_sum) < 1))

    def numexpr_eval(string):
        return numexpr.evaluate(string, local_dict=dict(X_THETA=1234, D_PE=678))

    assert pytest.approx(numexpr_eval(new_selection.to_numexpr()),
                         numexpr_eval('((X_THETA * 0.017453292519943295) > (3.141592653589793 / 4)) & (D_PE > 9.2)'))
