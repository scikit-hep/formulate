from __future__ import annotations

import lark
import pytest
from hypothesis import assume, given, settings
from hypothesis import strategies as st

import formulate


# Test for empty strings
def test_empty_string():
    """Test that empty strings are rejected."""
    with pytest.raises(Exception):
        formulate.from_root("")

    with pytest.raises(Exception):
        formulate.from_numexpr("")


# Test for whitespace-only strings
def test_whitespace_string():
    """Test that whitespace-only strings are rejected."""
    with pytest.raises(Exception):
        formulate.from_root("   ")

    with pytest.raises(Exception):
        formulate.from_numexpr("   ")


# Test for invalid syntax
def test_invalid_syntax():
    """Test that expressions with invalid syntax are rejected."""

    # Invalid characters
    with pytest.raises(Exception):
        formulate.from_root("a$b")

    with pytest.raises(Exception):
        formulate.from_numexpr("a$b")


# Test for unsupported operations
def test_unsupported_operations():
    """Test that unsupported operations are rejected."""
    # Try some operations that are definitely not supported
    with pytest.raises(Exception):
        formulate.from_root("a ? b : c")  # Ternary operator is not supported

    with pytest.raises(Exception):
        formulate.from_numexpr("a ? b : c")  # Ternary operator is not supported

    with pytest.raises(Exception):
        formulate.from_root("a ?? b")  # Null coalescing operator is not supported

    with pytest.raises(Exception):
        formulate.from_numexpr("a ?? b")  # Null coalescing operator is not supported


# Test for very large expressions
def test_very_large_expression():
    """Test that very large expressions are handled correctly."""
    # Create a very large expression
    large_expr = "a" + "+a" * 1000

    # This should either parse successfully or raise a specific error,
    # but it shouldn't crash the parser
    try:
        formulate.from_root(large_expr)
    except (RecursionError, MemoryError):
        # These are acceptable errors for very large expressions
        pass
    except Exception as e:
        # Other exceptions might indicate a problem
        pytest.fail(f"Unexpected exception: {e}")

    try:
        formulate.from_numexpr(large_expr)
    except (RecursionError, MemoryError):
        # These are acceptable errors for very large expressions
        pass
    except Exception as e:
        # Other exceptions might indicate a problem
        pytest.fail(f"Unexpected exception: {e}")


# Use Hypothesis to generate invalid expressions
@given(st.text(alphabet=st.characters(blacklist_categories=("L", "N")), min_size=1))
@settings(max_examples=1000)
def test_invalid_characters(s):
    """Test that expressions with invalid characters are rejected."""
    # Skip strings that contain only whitespace or valid operators
    assume(not s.isspace())
    assume(not all(c in "+-*/()<>=!&|^~_ " for c in s))  # TODO: why does _ not fail?

    # The expression should be rejected
    with pytest.raises(Exception):
        formulate.from_root(s)

    with pytest.raises(Exception):
        formulate.from_numexpr(s)


# Generate expressions with unbalanced parentheses
@given(
    st.text(alphabet="(", min_size=1, max_size=10),
    st.text(alphabet=")", min_size=0, max_size=9),
)
@settings(max_examples=1000)
def test_unbalanced_parentheses(open_parens, close_parens):
    """Test that expressions with unbalanced parentheses are rejected."""
    # Ensure we have more opening parentheses than closing ones
    assume(len(open_parens) > len(close_parens))

    # Create an expression with unbalanced parentheses
    expr = "a" + open_parens + "+b" + close_parens

    # The expression should be rejected
    with pytest.raises(lark.ParseError):
        formulate.from_root(expr)

    with pytest.raises(lark.ParseError):
        formulate.from_numexpr(expr)


# Test for invalid operator combinations
def test_invalid_operator_combinations():
    """Test that expressions with invalid operator combinations are rejected."""
    # Test specific invalid operator combinations
    invalid_expressions = [
        "a@b",  # @ is not a valid operator
        "a#b",  # # is not a valid operator
        "a$b",  # $ is not a valid operator
        "a`b",  # ` is not a valid operator
        "a\\b",  # \ is not a valid operator
        "a;b",  # ; is not a valid operator
        "a?b",  # ? is not a valid operator
    ]

    for expr in invalid_expressions:
        with pytest.raises(Exception):
            formulate.from_root(expr)

        with pytest.raises(Exception):
            formulate.from_numexpr(expr)


# Generate expressions with missing operands
@given(
    st.sampled_from(["a", "b", "c", "d", "f", "var"]),
    st.sampled_from(
        ["+", "-", "*", "/", "<", "<=", ">", ">=", "==", "!=", "&", "|", "^", "**"]
    ),
)
@settings(max_examples=100)
def test_missing_operands(var, op):
    """Test that expressions with missing operands are rejected."""
    # Create expressions with missing operands
    expr1 = f"{var}{op}"  # Missing right operand
    expr2 = f"{op}{var}"  # Missing left operand (except for unary operators)

    # The expressions should be rejected (except for unary + and -)
    if op not in ["+", "-"]:
        with pytest.raises(Exception):
            formulate.from_root(expr1)

        with pytest.raises(Exception):
            formulate.from_numexpr(expr1)

    if op not in ["+", "-", "~", "!"]:  # These can be unary operators
        with pytest.raises(Exception):
            formulate.from_root(expr2)

        with pytest.raises(Exception):
            formulate.from_numexpr(expr2)
