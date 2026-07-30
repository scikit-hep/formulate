"""The AST node classes themselves.

These tests build nodes directly rather than going through a parser, so they
can reach shapes the grammar cannot produce (a Matrix with no indices, a
BinaryOperator with an operator no backend supports) and pin the behaviour of
``__str__`` and of the ``variables`` / ``named_constants`` /
``unnamed_constants`` properties on every node type.
"""

from __future__ import annotations

import pytest
from ordered_set import OrderedSet

import formulate
from formulate.AST import BinaryOperator, Call, Literal, Matrix, Symbol, UnaryOperator

# --- __str__ is a debugging representation, not backend syntax ---


@pytest.mark.parametrize(
    "node,expected",
    [
        (Literal(3.14), "3.14"),
        (Literal(3), "3"),
        (Symbol("x"), "x"),
        (UnaryOperator("neg", Symbol("x")), "neg(x)"),
        (BinaryOperator("add", Symbol("a"), Symbol("b")), "add(a, b)"),
        (Matrix(Symbol("a"), (Literal(0),)), "a[0]"),
        (Matrix(Symbol("a"), (Literal(0), Symbol("i"))), "a[0, i]"),
        (Matrix(Symbol("a"), ()), "a[]"),
        (Call("sqrt", (Symbol("a"),)), "sqrt(a)"),
        (Call("length", ()), "length()"),
        (Call("arctan2", (Symbol("a"), Literal(1))), "arctan2(a, 1)"),
        (
            BinaryOperator("mul", UnaryOperator("neg", Symbol("a")), Literal(2)),
            "mul(neg(a), 2)",
        ),
    ],
)
def test_str_representation(node, expected):
    assert str(node) == expected


# --- Nodes are frozen value objects ---


@pytest.mark.parametrize(
    "left,right,equal",
    [
        (Literal(1.0), Literal(1.0), True),
        (Literal(1.0), Literal(2.0), False),
        (Symbol("a"), Symbol("a"), True),
        (Symbol("a"), Symbol("b"), False),
        (Symbol("a"), Literal(1.0), False),
        (UnaryOperator("neg", Symbol("a")), UnaryOperator("neg", Symbol("a")), True),
        (UnaryOperator("neg", Symbol("a")), UnaryOperator("pos", Symbol("a")), False),
        (
            BinaryOperator("add", Symbol("a"), Symbol("b")),
            BinaryOperator("add", Symbol("a"), Symbol("b")),
            True,
        ),
        (
            BinaryOperator("add", Symbol("a"), Symbol("b")),
            BinaryOperator("add", Symbol("b"), Symbol("a")),
            False,
        ),
        (Call("sqrt", (Symbol("a"),)), Call("sqrt", (Symbol("a"),)), True),
        (Call("sqrt", (Symbol("a"),)), Call("abs", (Symbol("a"),)), False),
        (Matrix(Symbol("a"), (Literal(0),)), Matrix(Symbol("a"), (Literal(0),)), True),
    ],
)
def test_nodes_compare_by_value(left, right, equal):
    assert (left == right) is equal


def test_nodes_are_immutable():
    with pytest.raises(AttributeError):
        Symbol("a").name = "b"


def test_every_node_of_a_parsed_tree_is_hashable():
    # Children are held in tuples, not lists, so a node can be used as a dict
    # key or set member -- Call and Matrix are the ones that hold several.
    parsed = formulate.from_root("TMath::Max(a[0][1], -b) + !c > pi")
    node_types = {type(node).__name__ for node in parsed._walk()}
    assert node_types == {
        "Literal",
        "Symbol",
        "UnaryOperator",
        "BinaryOperator",
        "Matrix",
        "Call",
    }
    assert len({hash(node) for node in parsed._walk()}) > 1
    assert hash(parsed) == hash(
        formulate.from_root("TMath::Max(a[0][1], -b) + !c > pi")
    )


def test_equal_expressions_from_different_sources_compare_equal():
    assert formulate.from_root("a+b") == formulate.from_numexpr("a+b")
    assert formulate.from_root("a+b") != formulate.from_numexpr("b+a")


# --- Symbol classification ---


def test_symbol_is_a_variable_unless_it_names_a_constant():
    assert Symbol("x").variables == OrderedSet(["x"])
    assert Symbol("x").named_constants == OrderedSet()
    assert Symbol("pi").variables == OrderedSet()
    assert Symbol("pi").named_constants == OrderedSet(["pi"])
    assert Symbol("pi").unnamed_constants == OrderedSet()


def test_literal_is_an_unnamed_constant():
    assert Literal(5.0).unnamed_constants == OrderedSet([5.0])
    assert Literal(5.0).variables == OrderedSet()
    assert Literal(5.0).named_constants == OrderedSet()


# --- Properties recurse through every child ---


def test_unary_operator_delegates_to_its_operand():
    assert UnaryOperator("neg", Symbol("x")).variables == OrderedSet(["x"])
    assert UnaryOperator("inv", Symbol("pi")).named_constants == OrderedSet(["pi"])
    assert UnaryOperator("pos", Literal(5.0)).unnamed_constants == OrderedSet([5.0])


def test_binary_operator_unions_both_sides():
    node = BinaryOperator(
        "add", Symbol("a"), BinaryOperator("mul", Symbol("b"), Literal(2))
    )
    assert node.variables == OrderedSet(["a", "b"])
    assert node.unnamed_constants == OrderedSet([2])


def test_matrix_covers_the_base_and_every_index():
    node = Matrix(Symbol("a"), (Symbol("i"), Literal(3), Symbol("pi")))
    assert node.variables == OrderedSet(["a", "i"])
    assert node.named_constants == OrderedSet(["pi"])
    assert node.unnamed_constants == OrderedSet([3])


def test_matrix_with_no_indices():
    node = Matrix(Symbol("a"), ())
    assert node.variables == OrderedSet(["a"])
    assert node.named_constants == OrderedSet()
    assert node.unnamed_constants == OrderedSet()


def test_matrix_base_can_itself_hold_constants():
    assert Matrix(Literal(3.14), (Symbol("i"),)).unnamed_constants == OrderedSet([3.14])
    assert formulate.from_root("pi[0]").named_constants == OrderedSet(["pi"])


def test_call_covers_every_argument():
    node = Call(
        "arctan2", (Symbol("a"), BinaryOperator("add", Symbol("b"), Literal(1)))
    )
    assert node.variables == OrderedSet(["a", "b"])
    assert node.unnamed_constants == OrderedSet([1])


def test_call_with_no_arguments_has_no_symbols():
    node = Call("length", ())
    assert node.variables == OrderedSet()
    assert node.named_constants == OrderedSet()
    assert node.unnamed_constants == OrderedSet()


# --- True/False are lowercased to canonical constant names ---


def test_true_symbol_from_root():
    expr = formulate.from_root("True")
    assert isinstance(expr, Symbol)
    assert expr.name == "true"


def test_false_symbol_from_numexpr():
    expr = formulate.from_numexpr("False")
    assert isinstance(expr, Symbol)
    assert expr.name == "false"


# --- Backends reject what they cannot express ---


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
        Matrix(Symbol("a"), (Literal(0),)).to_numexpr()


def test_call_unsupported_function_raises():
    # length (ROOT array function) is not available in NumExpr
    with pytest.raises(ValueError, match="not supported in NumExpr"):
        Call("length", ()).to_numexpr()


# --- Literal formatting ---


@pytest.mark.parametrize(
    "value,expected", [(3, "3"), (3.0, "3.0"), (3.14, "3.14"), (1e-6, "1e-06")]
)
def test_literals_keep_their_python_repr(value, expected):
    node = Literal(value)
    assert node.to_root() == expected
    assert node.to_numexpr() == expected
    assert node.to_python() == expected
