# Licensed under a 3-clause BSD style license, see LICENSE.
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

from formulate import Expression


def make_check_result(from_func, to_func):
    def check_result(input_string, expected_expression, expected_string=None, **kwargs):
        input_string = input_string.format(**kwargs)
        if expected_string is None:
            expected_string = input_string

        result = from_func(input_string)
        string = to_func(result)

        assert_equal_expressions(result, expected_expression)
        assert string.replace(' ', '') == expected_string.replace(' ', ''), (string, expected_string)
    return check_result


def assert_equal_expressions(lhs, rhs):
    assert isinstance(lhs, Expression)
    assert isinstance(rhs, Expression)
    assert lhs._id == rhs._id
    assert len(lhs._args) == len(rhs._args)
    for a, b in zip(lhs._args, rhs._args):
        print(repr(a), repr(b))
        assert isinstance(b, a.__class__)
        if isinstance(a, Expression):
            assert_equal_expressions(a, b)
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
