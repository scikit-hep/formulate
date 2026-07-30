from __future__ import annotations

import pytest

import formulate
from formulate.AST import BinaryOperator, Call, Matrix

# --- TMath::Min / TMath::Max round-trip (issue: both collapsed to Min$/Max$) ---


def test_tmath_min_roundtrip():
    expr = formulate.from_root("TMath::Min(a, b)")
    assert expr.to_root() == "TMath::Min(a, b)"


def test_tmath_max_roundtrip():
    expr = formulate.from_root("TMath::Max(a, b)")
    assert expr.to_root() == "TMath::Max(a, b)"


def test_array_min_roundtrip():
    expr = formulate.from_root("Min$(arr)")
    assert expr.to_root() == "Min$(arr)"


def test_array_max_roundtrip():
    expr = formulate.from_root("Max$(arr)")
    assert expr.to_root() == "Max$(arr)"


def test_tmath_min_distinct_from_array_min():
    scalar = formulate.from_root("TMath::Min(a, b)")
    array = formulate.from_root("Min$(arr)")
    assert scalar.to_root() != array.to_root()


def test_tmath_min_to_python():
    out = formulate.from_root("TMath::Min(a, b)").to_python()
    assert out == "np.minimum(a, b)"


def test_tmath_max_to_python():
    out = formulate.from_root("TMath::Max(a, b)").to_python()
    assert out == "np.maximum(a, b)"


@pytest.mark.parametrize(
    "expression,expected_name",
    [
        ("TMath::Min(a, b)", "TMath::Min"),
        ("TMath::Max(a, b)", "TMath::Max"),
    ],
)
def test_unsupported_tmath_error_names_what_was_written(expression, expected_name):
    # The canonical name (tmath_min) is internal and would mean nothing here.
    with pytest.raises(ValueError) as excinfo:
        formulate.from_root(expression).to_numexpr()
    message = str(excinfo.value)
    assert message == f'Function "{expected_name}" is not supported in NumExpr.'
    assert "tmath_" not in message


def test_unsupported_function_error_uses_its_own_name():
    with pytest.raises(ValueError) as excinfo:
        formulate.from_numexpr("where(a, b, c)").to_root()
    assert str(excinfo.value) == 'Function "where" is not supported in ROOT.'


# --- Bare $ functions without parentheses ---


def test_bare_length_dollar():
    expr = formulate.from_root("Length$")
    assert isinstance(expr, Call)
    assert expr.function == "length"
    assert expr.arguments == []


def test_bare_sum_dollar():
    expr = formulate.from_root("Sum$")
    assert isinstance(expr, Call)
    assert expr.function == "sum"


def test_bare_dollar_in_expression():
    expr = formulate.from_root("Sum$(pt)/Length$")
    assert isinstance(expr, BinaryOperator)


def test_bare_length_to_root():
    assert formulate.from_root("Length$").to_root() == "Length$()"


def test_bare_length_dollar_roundtrip():
    serialized = formulate.from_root("Length$").to_root()
    assert formulate.from_root(serialized).to_root() == serialized


# --- Indexing before power: a[0]**2 ---


@pytest.mark.parametrize(
    "expr",
    [
        "a[0]**2",
        "a[0]^2",
        "a[0][1]**2",
        "a[i]**b",
    ],
)
def test_indexed_power_parses(expr):
    result = formulate.from_root(expr)
    assert isinstance(result, BinaryOperator)
    assert result.operator == "pow"
    assert isinstance(result.left, Matrix)


def test_indexed_power_roundtrip():
    assert formulate.from_root("a[0]**2").to_root() == "(a[0] ** 2)"


# --- multi_out (:) is the only operator that is never parenthesized ---


def test_multi_out_is_not_parenthesized():
    # ':' separates the outputs of a TTreeFormula rather than combining two
    # values, so wrapping it in parentheses would change its meaning.
    assert formulate.from_root("a:b").to_root() == "a : b"
    assert formulate.from_root("a+1:b*2").to_root() == "(a + 1) : (b * 2)"
    assert formulate.from_root("a:b:c").to_root() == "a : b : c"


def test_multi_out_becomes_a_comma_in_python():
    assert formulate.from_root("a:b").to_python() == "a , b"
