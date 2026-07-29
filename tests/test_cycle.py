"""Round-trip properties: converting between backends must not lose structure.

Serializing an AST produces a canonical, fully parenthesized string.  Two
properties follow from that and are what these tests check:

* *idempotence* -- re-parsing a serialized expression and serializing it again
  yields the identical string;
* *round-trip stability* -- going NumExpr -> ROOT -> NumExpr (or the other way
  round) lands back on the same canonical string.

Comparing canonical strings is a much sharper check than evaluating both sides
numerically, because it also catches lost parentheses and mis-nested operands
that happen to evaluate the same for a particular set of inputs.

Note that ROOT -> NumExpr -> ROOT is only stable for expressions without named
constants: NumExpr has no symbolic constants, so ``TMath::Pi()`` necessarily
comes back as the literal ``3.141592653589793``.
"""

from __future__ import annotations

import pytest
from hypothesis import given, settings
from hypothesis import strategies as st

import formulate

# Syntax that is spelled identically in NumExpr and ROOT.
COMMON_SYNTAX = [
    # Arithmetic
    "a+2.0",
    "a-2.0",
    "f*2.0",
    "a/2.0",
    "a%2.0",
    "a**2.0",
    "2.0 - -6",
    "+5.0",
    "-5.0",
    # Comparisons
    "a<2.0",
    "a<=2.0",
    "a>2.0",
    "a>=2.0",
    "a==2.0",
    "a!=2.0",
    # Chains and precedence
    "a+b+c+d",
    "(((a-b)-c)-d)",
    "a*b*c*d",
    "(((a/b)/c)/d)",
    "a**b**c**d",
    "(a+b)*(c+d)",
    "(a-b)/(c-d)",
    "((a+b)*c)/d",
    "a*(b+(c*d))",
    "a+b*c**d%f",
    # Functions
    "sqrt(a)",
    "arctan2(a, b)",
    "sqrt(a**2 + b**2)",
    "exp(-0.5*((a-b)/c)**2)",
    "min(a)",
    "max(a)",
    "sum(a)",
]

# NumExpr spells the logical operators &, | and ~ ...
NUMEXPR_EXPRESSIONS = [
    *COMMON_SYNTAX,
    "a&b",
    "a|b",
    "~bool",
    "a&b&c",
    "a|b|c",
    "a&b&c&d",
    "a|b|c|d",
    "~(a&b)",
    "~(a|b)",
    "a&(b|c)",
    "(a&b)|c",
    "a|(b&c)",
    "(a|b)&c",
    "(~a**b)*23/(var|45)",
    # NumExpr inlines named constants, but they survive a trip through ROOT
    "pi*a",
    "exp1**b",
]

# ... while ROOT spells them &&, || and !.
ROOT_EXPRESSIONS = [
    *COMMON_SYNTAX,
    "a&&b",
    "a||b",
    "!bool",
    "a&&b&&c",
    "a||b||c",
    "a&&b&&c&&d",
    "a||b||c||d",
    "!(a&&b)",
    "!(a||b)",
    "a&&(b||c)",
    "(a&&b)||c",
    "a||(b&&c)",
    "(a||b)&&c",
    "(!a**b)*23/(var||45)",
    "TMath::Sqrt(a)",
    "Sum$(pt)",
]

# ROOT features with no NumExpr counterpart; only idempotence applies.
ROOT_ONLY_EXPRESSIONS = [
    "a[0]",
    "a[0][1]",
    "mat[a+1][b]",
    "Length$(a)",
    "Length$()",
    "a:b",
    "TMath::Pi()",
    "TMath::Infinity()",
    "TMath::QuietNaN()",
]


def numexpr_canonical(expr: str) -> str:
    return formulate.from_numexpr(expr).to_numexpr()


def root_canonical(expr: str) -> str:
    return formulate.from_root(expr).to_root()


@pytest.mark.parametrize("expr", NUMEXPR_EXPRESSIONS, ids=lambda x: x)
def test_numexpr_serialization_is_idempotent(expr):
    canonical = numexpr_canonical(expr)
    assert numexpr_canonical(canonical) == canonical


@pytest.mark.parametrize(
    "expr", ROOT_EXPRESSIONS + ROOT_ONLY_EXPRESSIONS, ids=lambda x: x
)
def test_root_serialization_is_idempotent(expr):
    canonical = root_canonical(expr)
    assert root_canonical(canonical) == canonical


@pytest.mark.parametrize("expr", NUMEXPR_EXPRESSIONS, ids=lambda x: x)
def test_numexpr_root_numexpr_round_trip(expr):
    canonical = numexpr_canonical(expr)
    via_root = formulate.from_root(formulate.from_numexpr(expr).to_root()).to_numexpr()
    assert via_root == canonical


@pytest.mark.parametrize("expr", ROOT_EXPRESSIONS, ids=lambda x: x)
def test_root_numexpr_root_round_trip(expr):
    canonical = root_canonical(expr)
    via_numexpr = formulate.from_numexpr(
        formulate.from_root(expr).to_numexpr()
    ).to_root()
    assert via_numexpr == canonical


@pytest.mark.parametrize("expr", NUMEXPR_EXPRESSIONS, ids=lambda x: x)
def test_repeated_conversions_reach_a_fixed_point(expr):
    """Converting back and forth repeatedly must not keep changing the expression."""
    canonical = numexpr_canonical(expr)
    current = canonical
    for _ in range(3):
        current = formulate.from_root(
            formulate.from_numexpr(current).to_root()
        ).to_numexpr()
    assert current == canonical


def test_named_constants_do_not_survive_a_round_trip_through_numexpr():
    """NumExpr has no symbolic constants, so ROOT -> NumExpr -> ROOT inlines them.

    This is a documented consequence of the NumExpr language, not a bug; the
    test pins it so the behaviour cannot change silently.
    """
    numexpr = formulate.from_root("TMath::Pi()").to_numexpr()
    assert numexpr == "3.141592653589793"
    assert formulate.from_numexpr(numexpr).to_root() == "3.141592653589793"


@pytest.mark.parametrize(
    "root_expr,array_form", [("TMath::Min(a, b)", "Min$"), ("TMath::Max(a, b)", "Max$")]
)
def test_tmath_min_max_collapse_onto_the_array_form_via_numexpr(root_expr, array_form):
    """ROOT distinguishes TMath::Min from Min$; NumExpr has only one `min`.

    Both therefore serialize to the same NumExpr call, and parsing that back
    yields the array-reduction form.  ROOT -> ROOT is unaffected (see
    tests/test_root_semantics.py); only a detour through NumExpr collapses them.
    """
    numexpr = formulate.from_root(root_expr).to_numexpr()
    assert formulate.from_numexpr(numexpr).to_root() == f"{array_form}(a, b)"


# --- Property-based coverage over randomly built expressions ---

_LEAVES = st.sampled_from(["a", "b", "c", "d", "f", "var", "1", "2.5", "3e2", "pi"])
_BINARY_OPS = st.sampled_from(
    ["+", "-", "*", "/", "%", "**", "<", "<=", ">", ">=", "==", "!=", "&", "|"]
)
_UNARY_OPS = st.sampled_from(["-", "+", "~"])
_FUNCTIONS = st.sampled_from(["sqrt", "abs", "log", "sin", "cos", "arctan"])

# Every generated node is parenthesized, so the string is unambiguous and these
# tests exercise conversion rather than the grammar's precedence rules (those
# are covered by tests/test_operator_precedence.py).
GENERATED_NUMEXPR = st.recursive(
    _LEAVES,
    lambda children: st.one_of(
        st.builds("({} {} {})".format, children, _BINARY_OPS, children),
        st.builds("({}{})".format, _UNARY_OPS, children),
        st.builds("{}({})".format, _FUNCTIONS, children),
    ),
    max_leaves=8,
)


@given(expr=GENERATED_NUMEXPR)
@settings(max_examples=300)
def test_generated_expression_round_trips_through_root(expr):
    canonical = numexpr_canonical(expr)
    via_root = formulate.from_root(formulate.from_numexpr(expr).to_root()).to_numexpr()
    assert via_root == canonical


@given(expr=GENERATED_NUMEXPR)
@settings(max_examples=300)
def test_generated_expression_serialization_is_idempotent(expr):
    canonical = numexpr_canonical(expr)
    assert numexpr_canonical(canonical) == canonical


@given(expr=GENERATED_NUMEXPR)
@settings(max_examples=300)
def test_generated_expression_preserves_symbols(expr):
    """Conversion must never invent or drop a variable or constant."""
    parsed = formulate.from_numexpr(expr)
    reparsed = formulate.from_root(parsed.to_root())
    assert reparsed.variables == parsed.variables
    assert reparsed.named_constants == parsed.named_constants


# --- Conversions that are expected to fail ---


@pytest.mark.parametrize("expr", ["a^b", "a^b^c", "where(a, b, c)", "log1p(a)"])
def test_numexpr_only_constructs_cannot_be_converted_to_root(expr):
    with pytest.raises(ValueError, match="not supported in ROOT"):
        formulate.from_numexpr(expr).to_root()


@pytest.mark.parametrize(
    "expr,message",
    [
        ("a[0]", "forbidden in NumExpr"),
        ("TMath::Infinity()", "not supported in NumExpr"),
        ("TMath::QuietNaN()", "not supported in NumExpr"),
        ("Length$(a)", "not supported in NumExpr"),
        ("a:b", "not supported in NumExpr"),
    ],
)
def test_root_only_constructs_cannot_be_converted_to_numexpr(expr, message):
    with pytest.raises(ValueError, match=message):
        formulate.from_root(expr).to_numexpr()
