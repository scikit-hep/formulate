"""Operator precedence and associativity.

Each case pairs an expression with the same expression written out with
explicit parentheses.  A case passes when both spellings serialize to the same
canonical string, which is only true if the parser built the same tree.

Cases are split by which parsers can read them: NumExpr and ROOT share
arithmetic and comparisons, but spell the logical operators differently, and
disagree about ``^`` (XOR in NumExpr, exponentiation in ROOT).
"""

from __future__ import annotations

import numpy as np
import pytest

import formulate


def assert_same_tree_numexpr(source, parenthesized):
    canonical = formulate.from_numexpr(parenthesized).to_numexpr()
    assert formulate.from_numexpr(source).to_numexpr() == canonical


def assert_same_tree_both(source, parenthesized):
    assert_same_tree_numexpr(source, parenthesized)
    canonical = formulate.from_root(parenthesized).to_root()
    assert formulate.from_root(source).to_root() == canonical


# --- Associativity ---------------------------------------------------------

LEFT_ASSOCIATIVE = [
    # Multiplication / division / modulo
    ("a*b*c", "(a*b)*c"),
    ("a*b*c*d*e*f", "((((a*b)*c)*d)*e)*f"),
    ("a/b/c", "(a/b)/c"),
    ("a/b/c/d/e/f", "((((a/b)/c)/d)/e)/f"),
    ("a*b/c", "(a*b)/c"),
    ("a/b*c", "(a/b)*c"),
    ("a*b/c*d/e*f", "((((a*b)/c)*d)/e)*f"),
    ("a%b%c", "(a%b)%c"),
    ("a%b%c%d%e", "(((a%b)%c)%d)%e"),
    ("a*b%c", "(a*b)%c"),
    ("a%b*c", "(a%b)*c"),
    ("a/b%c", "(a/b)%c"),
    ("a%b/c", "(a%b)/c"),
    ("a/b%c*d%e", "(((a/b)%c)*d)%e"),
    # Addition / subtraction
    ("a+b+c", "(a+b)+c"),
    ("a+b+c+d+e+f", "((((a+b)+c)+d)+e)+f"),
    ("a-b-c", "(a-b)-c"),
    ("a-b-c-d-e-f", "((((a-b)-c)-d)-e)-f"),
    ("a+b-c", "(a+b)-c"),
    ("a-b+c", "(a-b)+c"),
    ("a+b-c+d-e+f", "((((a+b)-c)+d)-e)+f"),
]

RIGHT_ASSOCIATIVE = [
    ("a**b**c", "a**(b**c)"),
    ("a**b**c**d", "a**(b**(c**d))"),
    ("a**b**c**d**e", "a**(b**(c**(d**e)))"),
]

LEFT_ASSOCIATIVE_NUMEXPR_ONLY = [
    ("a&b&c", "(a&b)&c"),
    ("a|b|c", "(a|b)|c"),
    ("a^b^c", "(a^b)^c"),
    ("a&b&c&d", "((a&b)&c)&d"),
]


@pytest.mark.parametrize("source,parenthesized", LEFT_ASSOCIATIVE, ids=lambda x: x)
def test_left_associative_operators(source, parenthesized):
    assert_same_tree_both(source, parenthesized)


@pytest.mark.parametrize("source,parenthesized", RIGHT_ASSOCIATIVE, ids=lambda x: x)
def test_power_is_right_associative(source, parenthesized):
    assert_same_tree_both(source, parenthesized)


@pytest.mark.parametrize(
    "source,parenthesized", LEFT_ASSOCIATIVE_NUMEXPR_ONLY, ids=lambda x: x
)
def test_left_associative_logical_operators(source, parenthesized):
    assert_same_tree_numexpr(source, parenthesized)


# --- Precedence between arithmetic levels ----------------------------------

ARITHMETIC_PRECEDENCE = [
    # * and / bind tighter than + and -
    ("a+b*c", "a+(b*c)"),
    ("a*b+c", "(a*b)+c"),
    ("a-b*c", "a-(b*c)"),
    ("a*b-c", "(a*b)-c"),
    ("a+b/c", "a+(b/c)"),
    ("a/b+c", "(a/b)+c"),
    ("a-b/c", "a-(b/c)"),
    ("a/b-c", "(a/b)-c"),
    ("a*b+c*d", "(a*b)+(c*d)"),
    ("a/b-c/d", "(a/b)-(c/d)"),
    ("a*b+c-d/e", "((a*b)+c)-(d/e)"),
    ("a/b-c+d*e", "((a/b)-c)+(d*e)"),
    # % sits with * and /, above + and -
    ("a+b%c", "a+(b%c)"),
    ("a%b+c", "(a%b)+c"),
    ("a-b%c", "a-(b%c)"),
    ("a%b-c", "(a%b)-c"),
    ("a%b+c%d", "(a%b)+(c%d)"),
    # ** binds tighter than *, /, % and +, -
    ("a**b*c", "(a**b)*c"),
    ("a*b**c", "a*(b**c)"),
    ("a**b/c", "(a**b)/c"),
    ("a/b**c", "a/(b**c)"),
    ("a**b%c", "(a**b)%c"),
    ("a%b**c", "a%(b**c)"),
    ("a**b+c", "(a**b)+c"),
    ("a+b**c", "a+(b**c)"),
    ("a**b-c", "(a**b)-c"),
    ("a-b**c", "a-(b**c)"),
    ("a**b*c**d", "(a**b)*(c**d)"),
    ("a**b%c**d", "(a**b)%(c**d)"),
    # Three levels at once
    ("a+b*c**d", "a+(b*(c**d))"),
    ("a**b*c+d", "((a**b)*c)+d"),
    ("a+b/c**d", "a+(b/(c**d))"),
    ("a/b**c*d", "(a/(b**c))*d"),
    ("a-b**c/d", "a-((b**c)/d)"),
    ("a+b*c/d**e", "a+((b*c)/(d**e))"),
    ("a**b/c*d+e", "(((a**b)/c)*d)+e"),
    ("a*b**c/d-e", "((a*(b**c))/d)-e"),
    ("a-b+c*d**e", "(a-b)+(c*(d**e))"),
    ("a+b*c**d%e", "a+((b*(c**d))%e)"),
    ("a%b**c*d+e", "((a%(b**c))*d)+e"),
    ("a**b%c/d*e-f+g", "(((((a**b)%c)/d)*e)-f)+g"),
]


@pytest.mark.parametrize("source,parenthesized", ARITHMETIC_PRECEDENCE, ids=lambda x: x)
def test_arithmetic_precedence(source, parenthesized):
    assert_same_tree_both(source, parenthesized)


# --- Comparisons are below all arithmetic ---------------------------------

COMPARISON_PRECEDENCE = [
    ("a+b<c", "(a+b)<c"),
    ("a<b+c", "a<(b+c)"),
    ("a-b>c", "(a-b)>c"),
    ("a>b-c", "a>(b-c)"),
    ("a*b<c", "(a*b)<c"),
    ("a<b*c", "a<(b*c)"),
    ("a/b>c", "(a/b)>c"),
    ("a>b/c", "a>(b/c)"),
    ("a**b<c", "(a**b)<c"),
    ("a<b**c", "a<(b**c)"),
    ("a+b<=c+d", "(a+b)<=(c+d)"),
    ("a-b>=c-d", "(a-b)>=(c-d)"),
    ("a*b==c*d", "(a*b)==(c*d)"),
    ("a/b!=c/d", "(a/b)!=(c/d)"),
    ("a%b==c%d", "(a%b)==(c%d)"),
    ("a**b==c**d", "(a**b)==(c**d)"),
    ("a+b<c*d", "(a+b)<(c*d)"),
    ("a+b*c<d", "(a+(b*c))<d"),
    ("a*b**c>d", "(a*(b**c))>d"),
    ("a<b+c*d", "a<(b+(c*d))"),
    ("a**b*c<d+a/b", "((a**b)*c)<(d+(a/b))"),
]


@pytest.mark.parametrize("source,parenthesized", COMPARISON_PRECEDENCE, ids=lambda x: x)
def test_comparison_precedence(source, parenthesized):
    assert_same_tree_both(source, parenthesized)


# --- Logical operators ------------------------------------------------------
#
# Note that these follow C/Python bitwise precedence: & binds tighter than ^,
# which binds tighter than |, and *all three bind tighter than a comparison*.
# That is the opposite of what `a < b & c` looks like at first glance.

LOGICAL_PRECEDENCE_NUMEXPR = [
    ("a&b|c", "(a&b)|c"),
    ("a|b&c", "a|(b&c)"),
    ("a&b|c&d", "(a&b)|(c&d)"),
    ("a|b&c|d", "(a|(b&c))|d"),
    ("a&b^c", "(a&b)^c"),
    ("a^b&c", "a^(b&c)"),
    ("a^b|c", "(a^b)|c"),
    ("a|b^c", "a|(b^c)"),
    ("a%b&c|d^f", "((a%b)&c)|(d^f)"),
    # Bitwise binds tighter than comparison
    ("a&b<c", "(a&b)<c"),
    ("a>b&c", "a>(b&c)"),
    ("a&b>c&d", "(a&b)>(c&d)"),
    ("a&b==c&d", "(a&b)==(c&d)"),
    ("a|b<c", "(a|b)<c"),
    ("a>b|c", "a>(b|c)"),
    ("a|b>c|d", "(a|b)>(c|d)"),
    ("a|b==c|d", "(a|b)==(c|d)"),
    # Arithmetic binds tighter than bitwise
    ("a+b&c", "(a+b)&c"),
    ("a&b+c", "a&(b+c)"),
    ("a*b|c", "(a*b)|c"),
    ("a|b*c", "a|(b*c)"),
    ("a**b^c", "(a**b)^c"),
    ("a^b**c", "a^(b**c)"),
    ("a**b&c**d", "(a**b)&(c**d)"),
    ("a&b**c", "a&(b**c)"),
    ("a**b|c**d", "(a**b)|(c**d)"),
    ("a|b**c", "a|(b**c)"),
    ("~a&b", "(~a)&b"),
    # Long mixed chains
    ("a|b&c<d+a*b**c", "(a|(b&c))<(d+(a*(b**c)))"),
    ("a**b**c<d&a", "(a**(b**c))<(d&a)"),
    ("a**b*c/d+a-b<c&d", "(((((a**b)*c)/d)+a)-b)<(c&d)"),
]

LOGICAL_PRECEDENCE_ROOT = [
    ("a&&b||c", "(a&&b)||c"),
    ("a||b&&c", "a||(b&&c)"),
    ("a&&b||c&&d", "(a&&b)||(c&&d)"),
    ("a+b&&c", "(a+b)&&c"),
    ("a&&b+c", "a&&(b+c)"),
    ("a*b||c", "(a*b)||c"),
    # ROOT's && and || are logical, not bitwise, so unlike NumExpr's & and |
    # they bind *looser* than a comparison -- as in C.
    ("a&&b<c", "a&&(b<c)"),
    ("a>b&&c", "(a>b)&&c"),
    ("a<b&&c<d", "(a<b)&&(c<d)"),
    ("a<b||c<d", "(a<b)||(c<d)"),
    ("!a&&b", "(!a)&&b"),
]


@pytest.mark.parametrize(
    "source,parenthesized", LOGICAL_PRECEDENCE_NUMEXPR, ids=lambda x: x
)
def test_numexpr_logical_precedence(source, parenthesized):
    assert_same_tree_numexpr(source, parenthesized)


@pytest.mark.parametrize(
    "source,parenthesized", LOGICAL_PRECEDENCE_ROOT, ids=lambda x: x
)
def test_root_logical_precedence(source, parenthesized):
    canonical = formulate.from_root(parenthesized).to_root()
    assert formulate.from_root(source).to_root() == canonical


def test_numexpr_and_root_disagree_about_logical_operator_precedence():
    """NumExpr's ``&`` is bitwise and binds tighter than a comparison; ROOT's
    ``&&`` is logical and binds looser.  Both match their source language, so
    the same-looking expression legitimately parses differently."""
    assert formulate.from_numexpr("a & b < c").to_numexpr() == "((a & b) < c)"
    assert formulate.from_root("a && b < c").to_root() == "(a && (b < c))"


@pytest.mark.parametrize("expr", ["a < b < c", "a == b == c", "a < b & c < d"])
def test_numexpr_rejects_chained_comparisons(expr):
    """In Python ``a < b < c`` means ``a < b and b < c``; formulate does not
    implement that, so it refuses the expression instead of silently parsing it
    as ``(a < b) < c``.

    ``a < b & c < d`` is included because ``&`` binds tighter than ``<``, which
    makes it a chained comparison rather than a conjunction of two comparisons.
    """
    with pytest.raises(formulate.ParseError, match="chained comparisons"):
        formulate.from_numexpr(expr)


@pytest.mark.parametrize(
    "expr,expected",
    [
        ("a < b < c", "((a < b) < c)"),
        ("a == b == c", "((a == b) == c)"),
        ("a<b<c<d", "(((a < b) < c) < d)"),
    ],
)
def test_root_reads_chained_comparisons_the_way_c_does(expr, expected):
    """ROOT is a C++ dialect, where comparisons simply associate to the left,
    so the expression is well defined and formulate accepts it."""
    assert formulate.from_root(expr).to_root() == expected


# --- Unary operators --------------------------------------------------------

UNARY_PRECEDENCE = [
    # Unary binds tighter than the binary arithmetic operators ...
    ("-a+b", "(-a)+b"),
    ("a+-b", "a+(-b)"),
    ("-a*b", "(-a)*b"),
    ("a*-b", "a*(-b)"),
    ("-a/b", "(-a)/b"),
    ("a/-b", "a/(-b)"),
    ("-a%b", "(-a)%b"),
    ("a%-b", "a%(-b)"),
    ("+a+b", "(+a)+b"),
    ("a++b", "a+(+b)"),
    ("+a*b", "(+a)*b"),
    ("a*+b", "a*(+b)"),
    # ... but not tighter than **
    ("-a**b", "-(a**b)"),
    ("+a**b", "+(a**b)"),
    ("a**-b", "a**(-b)"),
    ("a**+b", "a**(+b)"),
    ("-a**-b", "-(a**(-b))"),
    ("-a**b%c", "(-(a**b))%c"),
    # Stacked unary operators
    ("--a", "-(-a)"),
    ("---a", "-(-(-a))"),
    ("----a", "-(-(-(-a)))"),
    ("+-a", "+(-a)"),
    ("-+a", "-(+a)"),
    ("++a", "+(+a)"),
    ("--a**b", "-(-(a**b))"),
    # With functions
    ("-sin(a)", "-(sin(a))"),
    ("+cos(a)", "+(cos(a))"),
    ("-sqrt(a+b)", "-(sqrt(a+b))"),
    ("sqrt(-a+b)", "sqrt((-a)+b)"),
]


@pytest.mark.parametrize("source,parenthesized", UNARY_PRECEDENCE, ids=lambda x: x)
def test_unary_operator_precedence(source, parenthesized):
    assert_same_tree_both(source, parenthesized)


# --- Function calls bind tightest -------------------------------------------

FUNCTION_PRECEDENCE = [
    ("sin(a)+b", "(sin(a))+b"),
    ("a+sin(b)", "a+(sin(b))"),
    ("sin(a)*b", "(sin(a))*b"),
    ("a*sin(b)", "a*(sin(b))"),
    ("sin(a)**b", "(sin(a))**b"),
    ("a**sin(b)", "a**(sin(b))"),
    ("sin(a)+cos(b)", "(sin(a))+(cos(b))"),
    ("sin(a)*cos(b)+tan(c)", "((sin(a))*(cos(b)))+(tan(c))"),
    ("sqrt(a)**log(b)*exp(c)", "((sqrt(a))**(log(b)))*(exp(c))"),
    ("abs(a+b)*sin(c-d)/cos(e)", "((abs(a+b))*(sin(c-d)))/(cos(e))"),
    ("sin(cos(a))+sqrt(abs(b))", "(sin(cos(a)))+(sqrt(abs(b)))"),
    ("log(exp(a))**sqrt(abs(b))", "(log(exp(a)))**(sqrt(abs(b)))"),
    ("abs(sin(a))*cos(sqrt(b))", "(abs(sin(a)))*(cos(sqrt(b)))"),
]

FUNCTION_ARGUMENT_PRECEDENCE = [
    # Arguments are parsed as full expressions with the usual precedence
    ("cos(a+b*c)", "cos(a+(b*c))"),
    ("sqrt(a**b+c)", "sqrt((a**b)+c)"),
    ("sin(a+b*c**d)", "sin(a+(b*(c**d)))"),
    ("cos(a**b+c*d)", "cos((a**b)+(c*d))"),
    ("sqrt(a/b-c%d)", "sqrt((a/b)-(c%d))"),
    ("log(a*b/c+d)", "log(((a*b)/c)+d)"),
    ("abs(a**b**c+d)", "abs((a**(b**c))+d)"),
    ("sin(a**b**c)", "sin(a**(b**c))"),
    ("sqrt(a**b+c**d)", "sqrt((a**b)+(c**d))"),
    ("exp(a/b*c+d)", "exp(((a/b)*c)+d)"),
    ("abs(a+b*c-d/e)", "abs((a+(b*c))-(d/e))"),
    ("sin(a%b+c)", "sin((a%b)+c)"),
    ("sqrt(a**b%c+d)", "sqrt(((a**b)%c)+d)"),
]

NESTED_FUNCTIONS = [
    ("sin(cos(a))", "sin(cos(a))"),
    ("tan(asin(a))", "tan(arcsin(a))"),
    ("sin(cos(tan(abs(a))))", "sin(cos(tan(abs(a))))"),
    ("log(sqrt(abs(sin(cos(a)))))", "log(sqrt(abs(sin(cos(a)))))"),
    ("sin(cos(a+b))", "sin(cos(a+b))"),
    ("log(exp(a**b))", "log(exp(a**b))"),
    ("sin(cos(a))+b", "(sin(cos(a)))+b"),
    ("a*sqrt(abs(b))", "a*(sqrt(abs(b)))"),
    ("log(exp(a))**b", "(log(exp(a)))**b"),
]


@pytest.mark.parametrize(
    "source,parenthesized",
    FUNCTION_PRECEDENCE + FUNCTION_ARGUMENT_PRECEDENCE + NESTED_FUNCTIONS,
    ids=lambda x: x,
)
def test_function_call_precedence(source, parenthesized):
    assert_same_tree_both(source, parenthesized)


@pytest.mark.parametrize(
    "func", ["sin", "cos", "tan", "sqrt", "abs", "log", "exp", "arcsin", "tanh"]
)
@pytest.mark.parametrize("op", ["+", "-", "*", "/", "%", "**"])
def test_every_common_function_binds_tighter_than_every_operator(func, op):
    assert_same_tree_both(f"{func}(a){op}b", f"({func}(a)){op}b")
    assert_same_tree_both(f"a{op}{func}(b)", f"a{op}({func}(b))")


# --- Parentheses override precedence ----------------------------------------

PARENTHESES_OVERRIDE = [
    ("(a+b)*c", "a+b*c"),
    ("a*(b+c)", "a*b+c"),
    ("(a-b)/c", "a-b/c"),
    ("a/(b-c)", "a/b-c"),
    ("(a+b)**c", "a+b**c"),
    ("a**(b+c)", "a**b+c"),
    ("(a*b)**c", "a*b**c"),
    ("(a**b)**c", "a**b**c"),
    ("(a+b)*(c-d)", "a+b*c-d"),
    ("a**(b<c)", "a**b<c"),
]


@pytest.mark.parametrize("grouped,ungrouped", PARENTHESES_OVERRIDE, ids=lambda x: x)
def test_parentheses_change_the_tree(grouped, ungrouped):
    assert (
        formulate.from_numexpr(grouped).to_numexpr()
        != formulate.from_numexpr(ungrouped).to_numexpr()
    )


NESTED_PARENTHESES = [
    ("((a+b)*c)/d", "((a+b)*c)/d"),
    ("a/((b+c)*d)", "a/((b+c)*d)"),
    ("((a+b)*c)**((d-e)/f)", "((a+b)*c)**((d-e)/f)"),
    ("(a*b+c)/(d**e-f)", "((a*b)+c)/((d**e)-f)"),
    ("(a**b)%(c*d)+(e/f)", "((a**b)%(c*d))+(e/f)"),
    ("(a+(b*c))**((d/e)-(f%g))", "(a+(b*c))**((d/e)-(f%g))"),
    ("((a**b)+c)*((d%e)/f)", "((a**b)+c)*((d%e)/f)"),
    ("a**((b+c)*d)", "a**((b+c)*d)"),
    ("(a**b+c)**d", "((a**b)+c)**d"),
    ("a**(b+c*d)*e", "(a**(b+(c*d)))*e"),
]


@pytest.mark.parametrize("source,parenthesized", NESTED_PARENTHESES, ids=lambda x: x)
def test_nested_parentheses(source, parenthesized):
    assert_same_tree_both(source, parenthesized)


# --- Numeric literals participate in precedence the same way ----------------

LITERAL_PRECEDENCE = [
    ("1.+2.*3.", "1.+(2.*3.)"),
    ("2.**3.**4.", "2.**(3.**4.)"),
    ("10./2./5.", "(10./2.)/5."),
    ("1.+2.-3.*4.", "(1.+2.)-(3.*4.)"),
    ("-1.**2.", "-(1.**2.)"),
    ("1.*-2.", "1.*(-2.)"),
]


@pytest.mark.parametrize("source,parenthesized", LITERAL_PRECEDENCE, ids=lambda x: x)
def test_numeric_literal_precedence(source, parenthesized):
    assert_same_tree_both(source, parenthesized)


# --- Precedence pairs, generated --------------------------------------------

PRECEDENCE_LEVELS = {"**": 3, "*": 2, "/": 2, "%": 2, "+": 1, "-": 1}


@pytest.mark.parametrize("op1", sorted(PRECEDENCE_LEVELS))
@pytest.mark.parametrize("op2", sorted(PRECEDENCE_LEVELS))
def test_every_arithmetic_operator_pair(op1, op2):
    source = f"a{op1}b{op2}c"
    if PRECEDENCE_LEVELS[op2] > PRECEDENCE_LEVELS[op1]:
        parenthesized = f"a{op1}(b{op2}c)"
    elif PRECEDENCE_LEVELS[op1] > PRECEDENCE_LEVELS[op2]:
        parenthesized = f"(a{op1}b){op2}c"
    elif op1 == op2 == "**":
        parenthesized = "a**(b**c)"
    else:
        parenthesized = f"(a{op1}b){op2}c"
    assert_same_tree_both(source, parenthesized)


# --- The tree really does evaluate the way the precedence implies ------------


@pytest.mark.parametrize(
    "expr",
    [
        "a+b*c",
        "a*b+c",
        "a/b/c",
        "a*b/c",
        "a**b*c",
        "a-b-c",
        "a%b+c",
        "-a**b",
        "a+b*c**d%e",
        "(a+b)*c",
        "a/(b-c)",
        "a**b**c",
    ],
)
def test_generated_python_matches_native_python_evaluation(expr):
    """Python and formulate agree on precedence for the operators they share,
    so evaluating both must give the same number."""
    values = {"a": 2.0, "b": 3.0, "c": 4.0, "d": 2.0, "e": 5.0}
    rendered = formulate.from_numexpr(expr).to_python()
    assert np.isclose(
        eval(rendered, {"np": np, **values}),
        eval(expr, {}, dict(values)),
    )
