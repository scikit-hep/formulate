# Licensed under a 3-clause BSD style license, see LICENSE.
import sys

import pytest

from formulate import Expression, ParsingException
from formulate import UnnamedConstant as UC
from formulate import from_numexpr, to_numexpr
from formulate.identifiers import IDs

from .utils import make_check_result


check_result = make_check_result(from_numexpr, to_numexpr)
if sys.version_info < (3, 5):
    RecursionError = RuntimeError


@pytest.mark.slow
def test_long_chain():
    args = [UC(str(i)) for i in range(1000)]
    check_result(" + ".join(map(str, args)), Expression(IDs.ADD, *args))


def test_alternating_chain():
    string = "0"
    expected = UC("0")
    for i in range(1, 100):
        op_name, op_id = {0: (" + ", IDs.ADD), 1: (" - ", IDs.SUB)}[i % 2]
        string += op_name + str(i)
        expected = Expression(op_id, expected, UC(str(i)))
    check_result(string, expected)


@pytest.mark.slow
@pytest.mark.xfail(raises=RecursionError)
def test_long_alternating_chain():
    string = "0"
    expected = UC("0")
    for i in range(1, 1000):
        op_name, op_id = {0: (" + ", IDs.ADD), 1: (" - ", IDs.SUB)}[i % 2]
        string += op_name + str(i)
        expected = Expression(op_id, expected, UC(str(i)))
    check_result(string, expected)


def test_3_deep_chain():
    string = "sqrt(sqrt(sqrt(2)))"
    expected = Expression(IDs.SQRT, Expression(IDs.SQRT, Expression(IDs.SQRT, UC("2"))))
    check_result(string, expected)


@pytest.mark.slow
@pytest.mark.xfail(raises=RecursionError)
def test_5_deep_chain():
    string = "2"
    expected = UC("2")
    for _ in list(range(5)):
        string = f"sqrt({string})"
        expected = Expression(IDs.SQRT, expected)
    print(string)
    check_result(string, expected)


@pytest.mark.slow
@pytest.mark.xfail(raises=RecursionError)
def test_10_deep_chain():
    string = "2"
    expected = UC("2")
    for _ in list(range(10)):
        string = f"sqrt({string})"
        expected = Expression(IDs.SQRT, expected)
    print(string)
    check_result(string, expected)


def test_parse_invalid_expression():
    with pytest.raises(ParsingException):
        from_numexpr("saadasd()&+|()")


def test_invalid_arg_parse():
    with pytest.raises(ValueError):
        from_numexpr(Expression(IDs.SQRT, UC("2")))


def test_too_many_function_arguments():
    with pytest.raises(ParsingException):
        from_numexpr("sqrt(2, 3)")


def test_invalid_arg_to_string():
    with pytest.raises(ValueError):
        to_numexpr("1")
