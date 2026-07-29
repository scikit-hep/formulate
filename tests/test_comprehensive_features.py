"""Cross-backend feature coverage: ROOT/TFormula and NumExpr language features.

Covers features that behave *differently* between the two languages, or that
only one of them has.
"""

from __future__ import annotations

import numpy as np
import pytest
from ordered_set import OrderedSet

import formulate
from formulate.AST import Call, Literal, Matrix, Symbol

# --- The '^' operator means different things in the two languages ---


def test_caret_is_exponentiation_in_root():
    assert formulate.from_root("a^b").to_root() == "(a ** b)"
    assert formulate.from_root("a^b").to_numexpr() == "(a ** b)"


def test_caret_is_xor_in_numexpr():
    assert formulate.from_numexpr("a^b").to_numexpr() == "(a ^ b)"
    # ROOT has no XOR operator at all, since it spells '^' as power
    with pytest.raises(ValueError, match="not supported in ROOT"):
        formulate.from_numexpr("a^b").to_root()


def test_double_star_is_exponentiation_in_both():
    assert formulate.from_root("a**b").to_numexpr() == "(a ** b)"
    assert formulate.from_numexpr("a**b").to_root() == "(a ** b)"


# --- Array indexing (ROOT only) ---


@pytest.mark.parametrize(
    "expr,root,python",
    [
        ("arr[0]", "arr[0]", "arr[0]"),
        ("arr[i]", "arr[i]", "arr[i]"),
        ("arr[i][j]", "arr[i][j]", "arr[i, j]"),
        ("tree.branch[0]", "tree.branch[0]", "tree.branch[0]"),
        ("arr[i+1]", "arr[(i + 1)]", "arr[(i + 1)]"),
    ],
)
def test_array_indexing(expr, root, python):
    parsed = formulate.from_root(expr)
    assert isinstance(parsed, Matrix)
    assert parsed.to_root() == root
    assert parsed.to_python() == python


def test_numexpr_has_no_array_indexing():
    with pytest.raises(formulate.ParseError):
        formulate.from_numexpr("arr[0]")


# --- ROOT's '$' keywords ---


@pytest.mark.parametrize(
    "expr,expected",
    [
        ("Length$(arr)", "Length$(arr)"),
        ("Length$", "Length$()"),
        ("Sum$(pt)", "Sum$(pt)"),
        ("Sum$(pt > 20)", "Sum$((pt > 20))"),
        ("Min$(arr)", "Min$(arr)"),
        ("Max$(arr)", "Max$(arr)"),
    ],
)
def test_root_dollar_functions(expr, expected):
    assert formulate.from_root(expr).to_root() == expected


def test_rndm_is_treated_as_an_ordinary_variable():
    # ROOT has a `rndm` keyword, but formulate has no notion of side effects,
    # so it is carried through as a plain symbol.
    parsed = formulate.from_root("TMath::Sin(pi*rndm)")
    assert parsed.variables == OrderedSet(["rndm"])
    assert parsed.to_root() == "TMath::Sin((TMath::Pi() * rndm))"


# --- Constants can be written with or without call parentheses ---


@pytest.mark.parametrize("expr", ["pi", "pi()", "Pi()", "PI()", "TMath::Pi()"])
def test_pi_spellings_all_resolve_to_the_same_constant(expr):
    parsed = formulate.from_root(expr)
    assert isinstance(parsed, Symbol)
    assert parsed.name == "pi"


@pytest.mark.parametrize("expr", ["Pi", "PI", "Sqrt2", "E"])
def test_a_bare_symbol_is_matched_case_sensitively(expr):
    """Only the call form (``Pi()``) is case-insensitive.

    A bare identifier is a branch name, and branch names in ROOT are
    case-sensitive, so ``Pi`` must stay a variable rather than becoming the
    constant ``pi``.
    """
    parsed = formulate.from_root(expr)
    assert isinstance(parsed, Symbol)
    assert parsed.name == expr
    assert parsed.variables == OrderedSet([expr])


def test_calling_a_constant_with_arguments_is_an_error():
    with pytest.raises(SyntaxError, match="should not have arguments"):
        formulate.from_root("pi(a)")


# --- Numeric literals ---


@pytest.mark.parametrize(
    "expr,value",
    [
        ("42", 42),
        ("3.14159", 3.14159),
        ("1e-6", 1e-6),
        ("2.5E10", 2.5e10),
        (".5", 0.5),
        ("1.", 1.0),
    ],
)
def test_numeric_literal_forms(expr, value):
    for parse in (formulate.from_root, formulate.from_numexpr):
        parsed = parse(expr)
        assert isinstance(parsed, Literal)
        assert parsed.value == value
        assert type(parsed.value) is type(value)


@pytest.mark.parametrize("expr", ["0x10", "0b101", "1_000", "1j"])
def test_python_only_literal_forms_are_rejected(expr):
    """Neither ROOT nor NumExpr accepts these, so formulate must not either."""
    with pytest.raises(formulate.ParseError):
        formulate.from_root(expr)
    with pytest.raises(formulate.ParseError):
        formulate.from_numexpr(expr)


# --- String handling ---


@pytest.mark.parametrize(
    "expr", ["'hello' == s", "s != 'world'", "contains('s', 'test')", '"a" == b']
)
def test_string_literals_are_not_supported(expr):
    """NumExpr supports string comparisons; formulate's grammar deliberately
    does not, so the failure should be a clean parse error."""
    with pytest.raises(formulate.ParseError):
        formulate.from_numexpr(expr)


def test_contains_is_a_numexpr_only_function():
    # The function itself exists, it is only string *literals* that are absent
    assert formulate.from_numexpr("contains(s, t)").to_numexpr() == "contains(s, t)"
    # Neither other backend has a substring test to translate it into
    for backend in ("to_root", "to_python"):
        with pytest.raises(ValueError, match="not supported"):
            getattr(formulate.from_numexpr("contains(s, t)"), backend)()


# --- Both parsers agree on shared syntax ---


@pytest.mark.parametrize(
    "expr",
    [
        "a + b * c",
        "a * b + c * d",
        "a / b / c",
        "a ** b ** c",
        "a + b < c * d",
        "sqrt(a**2 + b**2)",
        "1/2 * a * b**2",
        "exp(-0.5*((a-b)/c)**2)",
        "sin(2*pi*a*b + c)",
        "abs(a - b) < 1e-6",
    ],
)
def test_root_and_numexpr_parsers_build_the_same_tree(expr):
    assert formulate.from_root(expr) == formulate.from_numexpr(expr)


# --- Translation tables ---


@pytest.mark.parametrize(
    "numexpr_expr,root_expr",
    [
        ("sin(x)", "TMath::Sin(x)"),
        ("cos(x)", "TMath::Cos(x)"),
        ("tan(x)", "TMath::Tan(x)"),
        ("sqrt(x)", "TMath::Sqrt(x)"),
        ("abs(x)", "TMath::Abs(x)"),
        ("exp(x)", "TMath::Exp(x)"),
        ("log(x)", "TMath::Log(x)"),
        ("log10(x)", "TMath::Log10(x)"),
        ("arcsin(x)", "TMath::ASin(x)"),
        ("arccos(x)", "TMath::ACos(x)"),
        ("arctan(x)", "TMath::ATan(x)"),
        ("arctan2(x, y)", "TMath::ATan2(x, y)"),
        ("arcsinh(x)", "TMath::ASinH(x)"),
        ("arccosh(x)", "TMath::ACosH(x)"),
        ("arctanh(x)", "TMath::ATanH(x)"),
        ("sinh(x)", "TMath::SinH(x)"),
        ("cosh(x)", "TMath::CosH(x)"),
        ("tanh(x)", "TMath::TanH(x)"),
        ("ceil(x)", "TMath::Ceil(x)"),
        ("floor(x)", "TMath::Floor(x)"),
        ("sum(x)", "Sum$(x)"),
        ("min(x)", "Min$(x)"),
        ("max(x)", "Max$(x)"),
    ],
)
def test_function_translations_go_both_ways(numexpr_expr, root_expr):
    assert formulate.from_numexpr(numexpr_expr).to_root() == root_expr
    assert formulate.from_root(root_expr).to_numexpr() == numexpr_expr


@pytest.mark.parametrize(
    "canonical,value,root_expr",
    [
        ("pi", 3.141592653589793, "TMath::Pi()"),
        ("exp1", 2.718281828459045, "TMath::E()"),
        ("sqrt2", 1.4142135623730951, "TMath::Sqrt2()"),
        ("invpi", 0.3183098861837907, "TMath::InvPi()"),
        ("piover2", 1.5707963267948966, "TMath::PiOver2()"),
        ("piover4", 0.7853981633974483, "TMath::PiOver4()"),
        ("tau", 6.283185307179586, "TMath::TwoPi()"),
        ("ln10", 2.302585092994046, "TMath::Ln10()"),
        ("avogadro", 6.02214076e23, "TMath::Na()"),
        ("k_boltzmann", 1.380649e-23, "TMath::K()"),
        ("c_light", 299792458.0, "TMath::C()"),
        ("eminus", -1.602176634e-19, "-TMath::Qe()"),
        ("eplus", 1.602176634e-19, "TMath::Qe()"),
        ("h_planck", 6.62607015e-34, "TMath::H()"),
        ("hbar", 6.62607015e-34, "TMath::Hbar()"),
        ("hbarc", 1.97326968e-16, "(TMath::Hbar() * TMath::C())"),
    ],
)
def test_constant_translations(canonical, value, root_expr):
    assert formulate.from_numexpr(canonical).to_root() == root_expr
    # Both spellings must inline to the same number in NumExpr
    from_canonical = eval(formulate.from_numexpr(canonical).to_numexpr())
    from_root = eval(formulate.from_root(root_expr).to_numexpr())
    assert np.isclose(from_canonical, value)
    assert np.isclose(from_root, value)


# --- variables / named_constants / unnamed_constants ---


@pytest.mark.parametrize(
    "expr,variables,named,unnamed",
    [
        ("2", [], [], [2]),
        ("2e-3", [], [], [2e-3]),
        ("A", ["A"], [], []),
        ("A + A", ["A"], [], []),
        ("A + B", ["A", "B"], [], []),
        ("A + A*A - 3e7", ["A"], [], [3e7]),
        ("arctan2(A, A)", ["A"], [], []),
        ("arctan2(A, B)", ["A", "B"], [], []),
        ("arctan2(arctan2(A, B), C)", ["A", "B", "C"], [], []),
        ("A.B * A.C", ["A.B", "A.C"], [], []),
        (
            "sin(x) * exp(y) * (z * 21 - exp1 - w - 1.0)",
            ["x", "y", "z", "w"],
            ["exp1"],
            [21, 1.0],
        ),
        (
            "var1 + pi * var2 / var_with_underscore",
            ["var1", "var2", "var_with_underscore"],
            ["pi"],
            [],
        ),
    ],
)
def test_symbol_and_constant_extraction_from_numexpr(expr, variables, named, unnamed):
    parsed = formulate.from_numexpr(expr)
    assert parsed.variables == OrderedSet(variables)
    assert parsed.named_constants == OrderedSet(named)
    assert parsed.unnamed_constants == OrderedSet(unnamed)


@pytest.mark.parametrize(
    "expr,variables,named,unnamed",
    [
        ("pi", [], ["pi"], []),
        ("arctan2(A, pi)", ["A"], ["pi"], []),
        ("mat[1][a]", ["mat", "a"], [], [1]),
        ("A.B * A.C", ["A.B", "A.C"], [], []),
        ("Length$", [], [], []),
        ("TMath::Pi() * TMath::E()", [], ["pi", "exp1"], []),
    ],
)
def test_symbol_and_constant_extraction_from_root(expr, variables, named, unnamed):
    parsed = formulate.from_root(expr)
    assert parsed.variables == OrderedSet(variables)
    assert parsed.named_constants == OrderedSet(named)
    assert parsed.unnamed_constants == OrderedSet(unnamed)


def test_variables_preserve_first_appearance_order():
    assert formulate.from_numexpr("c + b + a + b").variables == OrderedSet(
        ["c", "b", "a"]
    )


def test_zero_argument_call_has_no_symbols():
    parsed = formulate.from_root("Length$")
    assert isinstance(parsed, Call)
    assert parsed.arguments == []
    assert parsed.variables == OrderedSet()
