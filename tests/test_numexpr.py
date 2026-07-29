"""Serialization of parsed expressions back to NumExpr syntax.

Expected values are exact strings: for a serializer the formatting *is* the
behaviour, so a looser comparison (e.g. re-parsing with ``ast``) would silently
accept dropped or added parentheses.
"""

from __future__ import annotations

import pytest

import formulate

# (numexpr source, expected numexpr serialization)
NUMEXPR_ROUND_TRIPS = [
    # Arithmetic
    ("a+2.0", "(a + 2.0)"),
    ("a-2.0", "(a - 2.0)"),
    ("f*2.0", "(f * 2.0)"),
    ("a/2.0", "(a / 2.0)"),
    ("a%2.0", "(a % 2.0)"),
    ("a**2.0", "(a ** 2.0)"),
    # Comparisons
    ("a<2.0", "(a < 2.0)"),
    ("a<=2.0", "(a <= 2.0)"),
    ("a>2.0", "(a > 2.0)"),
    ("a>=2.0", "(a >= 2.0)"),
    ("a==2.0", "(a == 2.0)"),
    ("a!=2.0", "(a != 2.0)"),
    # Bitwise / logical
    ("a&b", "(a & b)"),
    ("a|b", "(a | b)"),
    ("a^2.0", "(a ^ 2.0)"),
    # Unary
    ("+5.0", "(+5.0)"),
    ("-5.0", "(-5.0)"),
    ("~bool", "(~bool)"),
    ("2.0 - -6", "(2.0 - (-6))"),
    # Functions
    ("sqrt(4)", "sqrt(4)"),
    ("arctan2(a, b)", "arctan2(a, b)"),
    # Left-associative chains
    ("a+b+c+d", "(((a + b) + c) + d)"),
    ("a-b-c-d", "(((a - b) - c) - d)"),
    ("a*b*c*d", "(((a * b) * c) * d)"),
    ("a/b/c/d", "(((a / b) / c) / d)"),
    ("a|b|c|d", "(((a | b) | c) | d)"),
    ("a&b&c&d", "(((a & b) & c) & d)"),
    ("a^b^c^d", "(((a ^ b) ^ c) ^ d)"),
    # Power is right-associative
    ("a**b**c**d", "(a ** (b ** (c ** d)))"),
    # Mixed precedence
    ("(~a**b)*23/(var|45)", "(((~(a ** b)) * 23) / (var | 45))"),
]


@pytest.mark.parametrize("source,expected", NUMEXPR_ROUND_TRIPS, ids=lambda x: x)
def test_to_numexpr(source, expected):
    assert formulate.from_numexpr(source).to_numexpr() == expected


@pytest.mark.parametrize("expected", [e for _, e in NUMEXPR_ROUND_TRIPS])
def test_to_numexpr_is_idempotent(expected):
    """Serialized output must re-parse to itself, so it is a stable canonical form."""
    assert formulate.from_numexpr(expected).to_numexpr() == expected


def test_pow_function_becomes_operator():
    # NumExpr has no pow() function, so Call("pow", ...) must render as **
    assert formulate.from_root("TMath::Power(a, b)").to_numexpr() == "(a ** b)"


@pytest.mark.parametrize("expr", ["TMath::Power(a)", "TMath::Power(a, b, c)"])
def test_pow_with_the_wrong_arity_is_rejected(expr):
    """`**` is binary, so there is nothing to render any other arity to. ROOT
    passes these through, so the error has to come from the NumExpr side."""
    parsed = formulate.from_root(expr)
    assert parsed.to_root() == expr

    with pytest.raises(ValueError, match="exactly two arguments"):
        parsed.to_numexpr()


def test_named_constant_is_inlined_as_a_number():
    # NumExpr has no symbolic constants, so they are substituted numerically
    assert formulate.from_numexpr("pi").to_numexpr() == "3.141592653589793"
