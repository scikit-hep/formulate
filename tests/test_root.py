"""Serialization of parsed expressions back to ROOT (TTreeFormula) syntax.

Expected values are exact strings: for a serializer the formatting *is* the
behaviour, so a looser comparison (e.g. re-parsing with ``ast``) would silently
accept dropped or added parentheses.
"""

from __future__ import annotations

import pytest

import formulate

# (numexpr source, expected ROOT serialization)
NUMEXPR_TO_ROOT = [
    # Arithmetic is spelled the same way in both languages
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
    ("+5.0", "(+5.0)"),
    ("-5.0", "(-5.0)"),
    ("2.0 - -6", "(2.0 - (-6))"),
    # Logical operators are doubled in ROOT
    ("a&b", "(a && b)"),
    ("a|b", "(a || b)"),
    ("~bool", "(!bool)"),
    ("a|b|c", "((a || b) || c)"),
    ("a&b&c", "((a && b) && c)"),
    ("a|b|c|d", "(((a || b) || c) || d)"),
    ("a&b&c&d", "(((a && b) && c) && d)"),
    # Functions are namespaced
    ("sqrt(4)", "TMath::Sqrt(4)"),
    ("arctan2(a, b)", "TMath::ATan2(a, b)"),
    # Associativity
    ("a+b+c+d", "(((a + b) + c) + d)"),
    ("a-b-c-d", "(((a - b) - c) - d)"),
    ("a*b*c*d", "(((a * b) * c) * d)"),
    ("a/b/c/d", "(((a / b) / c) / d)"),
    ("a**b**c**d", "(a ** (b ** (c ** d)))"),
    # Mixed precedence
    ("(~a**b)*23/(var|45)", "(((!(a ** b)) * 23) / (var || 45))"),
]

# (ROOT source, expected ROOT serialization)
ROOT_ROUND_TRIPS = [
    ("a&&2.0", "(a && 2.0)"),
    ("a||2.0", "(a || 2.0)"),
    ("!bool", "(!bool)"),
    ("a&&b&&c", "((a && b) && c)"),
    ("a||b||c", "((a || b) || c)"),
    ("a**2.0", "(a ** 2.0)"),
    # ROOT spells power as ^; it normalizes to **
    ("a^2.0", "(a ** 2.0)"),
    ("a^b^c^d", "(a ** (b ** (c ** d)))"),
    # Array indices stay in ROOT's [i][j] form
    ("a[45][1]", "a[45][1]"),
    ("mat1[a**23][mat2[45 - -34]]", "mat1[(a ** 23)][mat2[(45 - (-34))]]"),
    # Function-name normalization
    ("TMath::sqrt(4)", "TMath::Sqrt(4)"),
    ("pow(a, 2)", "TMath::Power(a, 2)"),
    ("Sum$(pt)", "Sum$(pt)"),
    # ':' separates multiple outputs and is never parenthesized
    ("a:b", "a : b"),
]


@pytest.mark.parametrize("source,expected", NUMEXPR_TO_ROOT, ids=lambda x: x)
def test_numexpr_to_root(source, expected):
    assert formulate.from_numexpr(source).to_root() == expected


@pytest.mark.parametrize("source,expected", ROOT_ROUND_TRIPS, ids=lambda x: x)
def test_root_to_root(source, expected):
    assert formulate.from_root(source).to_root() == expected


@pytest.mark.parametrize(
    "expected", [e for _, e in NUMEXPR_TO_ROOT] + [e for _, e in ROOT_ROUND_TRIPS]
)
def test_to_root_is_idempotent(expected):
    """Serialized output must re-parse to itself, so it is a stable canonical form."""
    assert formulate.from_root(expected).to_root() == expected


def test_xor_has_no_root_equivalent():
    # ROOT reads '^' as exponentiation, so numexpr's XOR cannot be expressed
    with pytest.raises(ValueError, match="not supported in ROOT"):
        formulate.from_numexpr("a^2.0").to_root()


def test_numexpr_only_function_has_no_root_equivalent():
    with pytest.raises(ValueError, match="not supported in ROOT"):
        formulate.from_numexpr("where(a, b, c)").to_root()
