from __future__ import annotations

import pytest
from ordered_set import OrderedSet

import formulate
from formulate.AST import Call, Literal, Matrix, Symbol


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
