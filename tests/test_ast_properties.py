from __future__ import annotations

import pytest
from ordered_set import OrderedSet

import formulate
from formulate.AST import BinaryOperator, Call, Literal, Matrix, Symbol, UnaryOperator


def test_zero_arg_call_parses():
    expr = formulate.from_root("Length$()")
    assert isinstance(expr, Call)
    assert expr.arguments == []


def test_zero_arg_call_to_root():
    assert formulate.from_root("Length$()").to_root() == "Length$()"


def test_zero_arg_call_variables():
    assert Call("length", []).variables == OrderedSet()


def test_zero_arg_call_named_constants():
    assert Call("length", []).named_constants == OrderedSet()


def test_zero_arg_call_unnamed_constants():
    assert Call("length", []).unnamed_constants == OrderedSet()


def test_matrix_named_constants_includes_base():
    expr = formulate.from_root("pi[0]")
    assert "pi" in expr.named_constants


def test_matrix_named_constants_index_only():
    expr = formulate.from_root("a[0]")
    assert expr.named_constants == OrderedSet()


def test_matrix_unnamed_constants_includes_base_literal():
    m = Matrix(Literal(3.14), [Symbol("i")])
    assert 3.14 in m.unnamed_constants


def test_matrix_variables_no_indices():
    m = Matrix(Symbol("a"), [])
    assert m.variables == OrderedSet(["a"])


@pytest.mark.parametrize("expr", ["a[0]", "a[i]", "a[0][1]"])
def test_matrix_named_constants_empty_when_no_constants(expr):
    assert formulate.from_root(expr).named_constants == OrderedSet()


# --- __str__ representations ---


def test_literal_str():
    assert str(Literal(3.14)) == "3.14"


def test_symbol_str():
    assert str(Symbol("x")) == "x"


def test_unary_operator_str():
    assert str(UnaryOperator("neg", Symbol("x"))) == "neg(x)"


def test_binary_operator_str():
    assert str(BinaryOperator("add", Symbol("a"), Symbol("b"))) == "add(a, b)"


def test_matrix_str():
    assert str(Matrix(Symbol("a"), [Literal(0)])) == "a[0]"


def test_call_str():
    assert str(Call("sqrt", [Symbol("a")])) == "sqrt(a)"


# --- UnaryOperator property delegation ---


def test_unary_operator_variables():
    assert UnaryOperator("neg", Symbol("x")).variables == OrderedSet(["x"])


def test_unary_operator_named_constants():
    assert UnaryOperator("inv", Symbol("pi")).named_constants == OrderedSet(["pi"])


def test_unary_operator_unnamed_constants():
    assert UnaryOperator("pos", Literal(5.0)).unnamed_constants == OrderedSet([5.0])


# --- True/False are lowercased to canonical constant names ---


def test_true_symbol_from_root():
    expr = formulate.from_root("True")
    assert isinstance(expr, Symbol)
    assert expr.name == "true"


def test_false_symbol_from_numexpr():
    expr = formulate.from_numexpr("False")
    assert isinstance(expr, Symbol)
    assert expr.name == "false"


# --- Backend error cases ---


def test_symbol_unsupported_constant_raises():
    # inf/neginf/nan are in CONSTANTS but not supported by NumExpr
    with pytest.raises(ValueError, match="not supported in NumExpr"):
        Symbol("inf").to_numexpr()


def test_unary_operator_unsupported_raises():
    # xor has no unary form in ROOT
    with pytest.raises(ValueError, match="not supported in ROOT"):
        UnaryOperator("xor", Symbol("a")).to_root()


def test_binary_operator_unsupported_raises():
    # xor is not in ROOT operator symbols
    with pytest.raises(ValueError, match="not supported in ROOT"):
        BinaryOperator("xor", Symbol("a"), Symbol("b")).to_root()


def test_matrix_forbidden_in_numexpr():
    # NumExpr forbids array indexing
    with pytest.raises(ValueError, match="forbidden in NumExpr"):
        Matrix(Symbol("a"), [Literal(0)]).to_numexpr()


def test_call_pow_as_operator_in_numexpr():
    # NumExpr renders pow() as ** rather than as a function call
    result = formulate.from_root("pow(a, b)").to_numexpr()
    assert result == "(a ** b)"


def test_call_unsupported_function_raises():
    # length (ROOT array function) is not available in NumExpr
    with pytest.raises(ValueError, match="not supported in NumExpr"):
        Call("length", []).to_numexpr()
