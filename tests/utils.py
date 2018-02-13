# Licensed under a 3-clause BSD style license, see LICENSE.
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

from formulate import Component, Expression, Variable


def make_check_result(from_func, to_func):
    def check_result(input_string, expected_expression, expected_string=None, **kwargs):
        input_string = input_string.format(**kwargs)
        if expected_string is None:
            expected_string = input_string

        result = from_func(input_string)
        string = to_func(result)

        assert_equal_expressions(result, expected_expression)
        # TODO Stop stripping parentheses
        assert (string.replace(' ', '').replace('(', '').replace(')', '') ==
                expected_string.replace(' ', '').replace('(', '').replace(')', '')), (string, expected_string)
    return check_result


def assert_equal_expressions(lhs, rhs):
    assert isinstance(lhs, Component)
    assert isinstance(rhs, Component)
    if isinstance(lhs, Variable):
        assert isinstance(rhs, Variable)
        assert lhs.name == rhs.name
    else:
        assert lhs.id == rhs.id
        assert len(lhs.args) == len(rhs.args)
        for a, b in zip(lhs.args, rhs.args):
            assert isinstance(b, a.__class__)
            if isinstance(a, Expression):
                assert_equal_expressions(a, b)
            elif isinstance(a, Variable):
                assert a.name == b.name
            else:
                # Could floating point precision become a problem here?
                assert a == b
        # TODO Check the equivalent method always gets it right
        # assert lhs.equivilent(rhs)
        # assert rhs.equivilent(lhs)


# def test_empty():
#     from_numexpr('')

# TODO What should this do? Just a number?
# assert_equal_expressions(from_numexpr('-1'), Expression(ID, 1, 1))
