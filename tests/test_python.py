"""Serialization of parsed expressions to plain Python/NumPy syntax.

Python is an output-only backend (there is no ``from_python``), so these tests
pin the exact rendering and check that it is valid, evaluable Python.
"""

from __future__ import annotations

import ast

import numpy as np
import pytest

import formulate

# (ROOT source, expected Python serialization)
ROOT_TO_PYTHON = [
    ("a+2.0", "(a + 2.0)"),
    ("a-2.0", "(a - 2.0)"),
    ("f*2.0", "(f * 2.0)"),
    ("a/2.0", "(a / 2.0)"),
    ("a%2.0", "(a % 2.0)"),
    ("a**2.0", "(a ** 2.0)"),
    ("a<2.0", "(a < 2.0)"),
    ("a<=2.0", "(a <= 2.0)"),
    ("a>2.0", "(a > 2.0)"),
    ("a>=2.0", "(a >= 2.0)"),
    ("a==2.0", "(a == 2.0)"),
    ("a!=2.0", "(a != 2.0)"),
    # ROOT's logical operators map onto NumPy's bitwise ones
    ("a&&2.0", "(a & 2.0)"),
    ("a||2.0", "(a | 2.0)"),
    ("!bool", "(~bool)"),
    ("a&&b&&c", "((a & b) & c)"),
    ("a||b||c", "((a | b) | c)"),
    # Unary
    ("+5.0", "(+5.0)"),
    ("-5.0", "(-5.0)"),
    ("2.0 - -6", "(2.0 - (-6))"),
    # ROOT's ^ is exponentiation
    ("a^2.0", "(a ** 2.0)"),
    ("a^b^c^d", "(a ** (b ** (c ** d)))"),
    ("a**b**c**d", "(a ** (b ** (c ** d)))"),
    # Chained indices become a single NumPy tuple index
    ("a[45][1]", "a[45, 1]"),
    ("mat1[a**23][mat2[45 - -34]]", "mat1[(a ** 23), mat2[(45 - (-34))]]"),
    # Functions get the np. prefix
    ("TMath::sqrt(4)", "np.sqrt(4)"),
    ("pow(a, 2)", "np.power(a, 2)"),
    ("TMath::Min(a, b)", "np.minimum(a, b)"),
    ("TMath::Max(a, b)", "np.maximum(a, b)"),
    # Associativity
    ("a+b+c+d", "(((a + b) + c) + d)"),
    ("a-b-c-d", "(((a - b) - c) - d)"),
    ("a*b*c*d", "(((a * b) * c) * d)"),
    ("a/b/c/d", "(((a / b) / c) / d)"),
    ("!a**b*23/(var||45)", "(((~(a ** b)) * 23) / (var | 45))"),
]


@pytest.mark.parametrize("source,expected", ROOT_TO_PYTHON, ids=lambda x: x)
def test_root_to_python(source, expected):
    assert formulate.from_root(source).to_python() == expected


@pytest.mark.parametrize("expected", [e for _, e in ROOT_TO_PYTHON])
def test_python_output_is_syntactically_valid(expected):
    ast.parse(expected, mode="eval")


@pytest.mark.parametrize(
    "expr,expected",
    [
        ("a+b*c", 2.0 + 3.0 * 4.0),
        ("(a+b)*c", (2.0 + 3.0) * 4.0),
        ("a**b**c", 2.0 ** (3.0**4.0)),
        ("a/b/c", 2.0 / 3.0 / 4.0),
        ("-a**b", -(2.0**3.0)),
        ("TMath::Sqrt(a*a)", 2.0),
        ("TMath::Min(a, b)", 2.0),
        ("TMath::Max(a, b)", 3.0),
        ("pow(a, b)", 8.0),
        ("a%b", 2.0 % 3.0),
    ],
)
def test_python_output_evaluates_to_the_expected_value(expr, expected):
    """The generated Python must reproduce the semantics of the ROOT input."""
    rendered = formulate.from_root(expr).to_python()
    assert np.isclose(
        eval(rendered, {"np": np, "a": 2.0, "b": 3.0, "c": 4.0}),
        expected,
    )


@pytest.mark.parametrize(
    "expr,expected",
    [
        ("pi", np.pi),
        ("sqrt2", np.sqrt(2)),
        ("exp1", np.e),
        ("TMath::TwoPi()", 2 * np.pi),
    ],
)
def test_finite_constants_are_inlined_as_numbers(expr, expected):
    assert np.isclose(float(formulate.from_root(expr).to_python()), expected)


@pytest.mark.parametrize(
    "expr,check",
    [
        ("TMath::Infinity()", np.isposinf),
        ("-TMath::Infinity()", np.isneginf),
        ("TMath::QuietNaN()", np.isnan),
    ],
)
def test_non_finite_constants_are_rendered_as_python_floats(expr, check):
    """inf/nan have no NumExpr equivalent but Python can express them."""
    rendered = formulate.from_root(expr).to_python()
    assert check(eval(rendered))


@pytest.mark.parametrize("expr,expected", [("true", True), ("false", False)])
def test_boolean_constants(expr, expected):
    assert eval(formulate.from_root(expr).to_python()) is expected
