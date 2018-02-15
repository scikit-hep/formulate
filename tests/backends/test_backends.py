# Licensed under a 3-clause BSD style license, see LICENSE.
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

from formulate import from_numexpr, to_numexpr, from_root, to_root

from ..utils import assert_equal_expressions


def do_checks(numexpr_input, root_input):
    def test():
        root_expression = from_root(root_input)
        numexpr_expression = from_numexpr(numexpr_input)
        assert_equal_expressions(root_expression, numexpr_expression)
        assert to_numexpr(root_expression) == to_numexpr(numexpr_expression)
        assert to_root(root_expression) == to_root(numexpr_expression)

    return test


test_001 = do_checks('True', 'true')
test_002 = do_checks('False', 'false')
test_003 = do_checks('sqrt(2)', 'sqrt(2)')
test_004 = do_checks('sqrt(2)', 'TMath::Sqrt(2)')
test_005 = do_checks('sqrt(abs(-4))', 'TMath::Sqrt(TMath::Abs(-4))')
test_006 = do_checks('A & B & C & D', 'A && B && C && D')
test_007 = do_checks('A & B | C & D', 'A && B || C && D')
test_008 = do_checks('A & ~B | C & D', 'A && !B || C && D')
