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


# --- branch.leaf is one name, not an attribute access ---


def test_dotted_names_survive_the_backends_that_have_them():
    expr = formulate.from_root("branch.leaf + 1")
    assert expr.variables == {"branch.leaf"}
    assert expr.to_root() == "(branch.leaf + 1)"
    assert expr.to_python() == "(branch.leaf + 1)"


@pytest.mark.parametrize(
    "name,encoded",
    [
        ("branch.leaf", "branch_2e_leaf"),  # '.' is 0x2e
        ("x.y.z", "x_2e_y_2e_z"),
        # '_' is escaped as 0x5f inside a name that is being encoded, so this
        # cannot collide with the encoding of `a.b.c`.
        ("a.b_c", "a_2e_b_5f_c"),
        # Names NumExpr can already spell are left exactly as written, which is
        # why an underscore on its own is not encoded.
        ("pt_corrected", "pt_corrected"),
        ("pt", "pt"),
    ],
)
def test_numexpr_names_are_hex_encoded_only_where_they_have_to_be(name, encoded):
    """NumExpr rejects any expression containing a dot and has no quoting
    syntax, so a name it cannot spell is encoded the way uproot encodes C++
    classnames rather than emitted as-is or refused."""
    assert formulate.from_root(name).to_numexpr() == encoded


def test_only_the_offending_symbol_is_encoded():
    assert (
        formulate.from_root("branch.leaf + other").to_numexpr()
        == "(branch_2e_leaf + other)"
    )


def test_encoding_is_not_undone_on_the_way_back():
    """from_numexpr does not decode: a branch really named `branch_2e_leaf` is
    indistinguishable from an encoded `branch.leaf`, and silently renaming the
    former would be worse than not restoring the latter."""
    assert formulate.from_numexpr("branch_2e_leaf").to_root() == "branch_2e_leaf"


# --- Bare $ functions without parentheses ---


def test_bare_length_dollar():
    expr = formulate.from_root("Length$")
    assert isinstance(expr, Call)
    assert expr.function == "length"
    assert expr.arguments == ()


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
    assert formulate.from_root("a:b").to_python() == "a, b"


@pytest.mark.parametrize(
    "expr",
    [
        "(a:b)+c",
        "(a:b)",
        "-(a:b)",
        "sqrt(a:b)",
        "TMath::Max(a:b, c)",
        "arr[a:b]",
    ],
)
def test_multi_out_is_rejected_below_the_top_level(expr):
    """Because ':' is never parenthesized, a nested one could not be written
    back out unambiguously: `(a:b)+c` used to serialize as `a : b + c` and
    re-parse as `a:(b+c)`. ROOT does not accept these either -- ':' is how
    TTree::Draw separates whole expressions, not an operator.
    """
    with pytest.raises(formulate.ParseError):
        formulate.from_root(expr)


def test_multi_out_survives_a_round_trip_at_the_top_level():
    for expr in ("a:b", "a:b:c", "a+1:b*2"):
        serialized = formulate.from_root(expr).to_root()
        assert formulate.from_root(serialized).to_root() == serialized
