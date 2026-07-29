"""Surface syntax that must not change the meaning of an expression.

Whitespace and redundant parentheses are the two ways the same expression can
be written differently.  Each test therefore parses both spellings and compares
the *canonical serialization*, which is the only way to show that formulate
built the same tree -- evaluating the two source strings in Python would only
prove something about Python's own parser.
"""

from __future__ import annotations

import pytest
from hypothesis import given, settings
from hypothesis import strategies as st

import formulate


def numexpr_canonical(expr: str) -> str:
    return formulate.from_numexpr(expr).to_numexpr()


def root_canonical(expr: str) -> str:
    return formulate.from_root(expr).to_root()


# --- Whitespace ---

# Kept as token lists so that multi-character operators are never split.
TOKENIZED_EXPRESSIONS = [
    ["a", "+", "b"],
    ["a", "-", "b"],
    ["a", "*", "b"],
    ["a", "/", "b"],
    ["a", "%", "b"],
    ["a", "**", "b"],
    ["a", "<", "b"],
    ["a", "<=", "b"],
    ["a", ">", "b"],
    ["a", ">=", "b"],
    ["a", "==", "b"],
    ["a", "!=", "b"],
    ["a", "&", "b"],
    ["a", "|", "b"],
    ["a", "^", "b"],
    ["~", "a"],
    ["-", "a"],
    ["sqrt", "(", "a", ")"],
    ["arctan2", "(", "a", ",", "b", ")"],
    ["a", "+", "b", "*", "c", "**", "d"],
    ["(", "a", "+", "b", ")", "*", "c"],
    ["sqrt", "(", "a", "+", "b", ")", "/", "c"],
]

WHITESPACE = st.sampled_from(["", " ", "  ", "\t", " \t ", "\n"])


@pytest.mark.parametrize("tokens", TOKENIZED_EXPRESSIONS, ids="".join)
@given(data=st.data())
@settings(max_examples=25)
def test_whitespace_between_tokens_is_insignificant(tokens, data):
    gaps = data.draw(
        st.lists(WHITESPACE, min_size=len(tokens) + 1, max_size=len(tokens) + 1)
    )
    spaced = (
        "".join(gap + token for gap, token in zip(gaps, tokens, strict=False))
        + gaps[-1]
    )
    assert numexpr_canonical(spaced) == numexpr_canonical("".join(tokens))


@pytest.mark.parametrize(
    "reference,variation",
    [
        ("sqrt(a)", "sqrt (a)"),
        ("sqrt(a)", "sqrt( a )"),
        ("TMath::Sqrt(a)", "TMath::Sqrt ( a )"),
        ("a&&b", "a && b"),
        ("a||b", "a  ||  b"),
        ("!a", "! a"),
        ("a[0]", "a [ 0 ]"),
        ("Sum$(pt)", "Sum$( pt )"),
    ],
)
def test_root_whitespace_is_insignificant(reference, variation):
    assert root_canonical(variation) == root_canonical(reference)


# --- Redundant parentheses ---


@pytest.mark.parametrize(
    "reference,variations",
    [
        ("a+b", ["(a+b)", "((a+b))", "(a)+b", "a+(b)", "(a)+(b)"]),
        ("a-b", ["(a-b)", "((a-b))", "(a)-(b)"]),
        ("a*b", ["(a*b)", "((a*b))", "(a)*(b)"]),
        ("a/b", ["(a/b)", "((a/b))", "(a)/(b)"]),
        ("a**b", ["(a**b)", "((a**b))", "(a)**(b)"]),
        ("a<=b", ["(a<=b)", "(a)<=(b)"]),
        ("a!=b", ["(a!=b)", "(a)!=(b)"]),
        ("a&b", ["(a&b)", "((a&b))", "(a)&(b)"]),
        ("a|b", ["(a|b)", "((a|b))", "(a)|(b)"]),
        ("~a", ["(~a)", "~(a)", "(~(a))"]),
        ("sqrt(a)", ["(sqrt(a))", "sqrt((a))"]),
        # Parentheses that merely restate the default precedence
        ("a+b*c", ["a+(b*c)", "(a+(b*c))"]),
        ("a*b+c", ["(a*b)+c", "((a*b)+c)"]),
        ("a&b|c", ["(a&b)|c", "((a&b)|c)"]),
        ("a|b&c", ["a|(b&c)", "(a|(b&c))"]),
        ("a**b**c", ["a**(b**c)", "(a**(b**c))"]),
    ],
)
def test_redundant_parentheses_do_not_change_the_tree(reference, variations):
    expected = numexpr_canonical(reference)
    for variation in variations:
        assert numexpr_canonical(variation) == expected


@pytest.mark.parametrize(
    "reference,variation",
    [
        ("a&&b", "(a)&&(b)"),
        ("a||b", "((a||b))"),
        ("!a", "!(a)"),
        ("a^b", "(a)^(b)"),
        ("TMath::Sqrt(a)", "(TMath::Sqrt((a)))"),
        ("a[0]", "(a[0])"),
    ],
)
def test_root_redundant_parentheses_do_not_change_the_tree(reference, variation):
    assert root_canonical(variation) == root_canonical(reference)


@pytest.mark.parametrize(
    "grouped,ungrouped",
    [
        ("(a+b)*c", "a+b*c"),
        ("a*(b+c)", "a*b+c"),
        ("(a**b)**c", "a**b**c"),
        ("(a&b)|c", "a|b&c"),
    ],
)
def test_parentheses_that_do_change_the_tree(grouped, ungrouped):
    """The counterpart to the tests above: grouping that overrides precedence."""
    assert numexpr_canonical(grouped) != numexpr_canonical(ungrouped)


# --- Malformed input ---

OPERATORS = [
    "+",
    "-",
    "*",
    "/",
    "**",
    "<",
    "<=",
    ">",
    ">=",
    "==",
    "!=",
    "&",
    "|",
    "^",
    "&&",
    "||",
]

# The bool says whether the template is also invalid for '+' and '-', which are
# valid as unary prefixes and so make some of these templates parseable.
INVALID_TEMPLATES = {
    "a * {op} b": False,  # operator where an operand is expected
    "a {op} {op} b": False,  # doubled operator
    "(a {op} b": True,  # unmatched opening parenthesis
    "a {op} b)": True,  # unmatched closing parenthesis
    "a {op} ": True,  # missing right operand
    "{op} b": False,  # missing left operand
}


@pytest.mark.parametrize("template,fail_plusminus", INVALID_TEMPLATES.items())
@pytest.mark.parametrize("op", OPERATORS)
def test_malformed_expressions_are_rejected(template, fail_plusminus, op):
    expr = template.format(op=op)
    if fail_plusminus or op not in ("+", "-"):
        with pytest.raises(formulate.ParseError):
            formulate.from_numexpr(expr)
        with pytest.raises(formulate.ParseError):
            formulate.from_root(expr)
    else:
        # '+'/'-' are unary prefixes, so these particular strings do parse
        formulate.from_numexpr(expr)
        formulate.from_root(expr)


@pytest.mark.parametrize(
    "expr",
    [
        "sqrt(",
        "sqrt)",
        "sqrt(,a)",
        "sqrt(a,,b)",
        "a[",
        "a[0",
        "a..b",
        "a b",
        "3 4",
        "()",
    ],
)
def test_structurally_broken_expressions_are_rejected(expr):
    with pytest.raises(formulate.ParseError):
        formulate.from_root(expr)


@pytest.mark.parametrize(
    "expr,expected",
    [
        ("sqrt(a,)", "TMath::Sqrt(a)"),
        ("arctan2(a, b,)", "TMath::ATan2(a, b)"),
    ],
)
def test_trailing_comma_in_an_argument_list_is_allowed(expr, expected):
    """The grammar permits a trailing comma, as C++ and Python both do."""
    assert root_canonical(expr) == expected
