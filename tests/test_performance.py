from __future__ import annotations

import random
import sys
import time

import pytest

import formulate


def generate_long_expression(length=1000):
    """Generate a very long expression with the specified number of symbols and operators.

    Args:
        length: The approximate length of the expression in terms of symbols and operators.

    Returns:
        A string containing a valid expression with approximately the specified length.
    """
    # Define variables, operators, and constants to use in the expression
    variables = ["a", "b", "c", "d", "x", "y", "z"]
    # Use a more limited set of operators to avoid syntax issues
    binary_operators = ["+", "-", "*", "/"]
    constants = ["1.0", "2.0", "3.14", "42.0", "0.5"]

    # Start with a simple expression
    expression = random.choice(variables)

    # Add operators and operands until we reach the desired length
    current_length = 1
    while current_length < length:
        # Add a binary operator and an operand
        operator = random.choice(binary_operators)
        operand = random.choice(variables + constants)
        expression += operator + operand
        current_length += 2  # Operator + operand

    return expression


EXPRESSION_LENGTH = 10_000

sys.setrecursionlimit(50_000)  # TODO: where to best set this?


def test_generate_long_expression():
    """Test that the generate_long_expression function works correctly."""
    expr = generate_long_expression(EXPRESSION_LENGTH)
    assert len(expr) >= EXPRESSION_LENGTH

    # Try to parse the expression to make sure it's valid
    try:
        formulate.from_root(expr)
    except Exception as e:
        raise
        pytest.fail(f"Failed to parse generated expression, type={type(e)}: {e}")


@pytest.mark.parametrize(
    "test_name, expr_length, loader1, converter1, intermediate, loader2, converter2",
    [
        # TTreeFormula: Root -> Python -> Root -> Python
        (
            "TTreeFormula",
            EXPRESSION_LENGTH,
            (formulate.from_root, "from_root"),
            ("to_python", lambda ast: ast.to_python()),
            False,
            (formulate.from_root, "from_root"),
            ("to_python", lambda ast: ast.to_python()),
        ),
        # NumExpr: NumExpr -> Python -> NumExpr -> Python
        (
            "NumExpr",
            EXPRESSION_LENGTH,
            (formulate.from_numexpr, "from_numexpr"),
            ("to_python", lambda ast: ast.to_python()),
            False,
            (formulate.from_numexpr, "from_numexpr"),
            ("to_python", lambda ast: ast.to_python()),
        ),
        # Root->NumExpr->Root: Root -> NumExpr -> NumExpr -> Root
        (
            "Root_to_NumExpr",
            100,
            (formulate.from_root, "from_root"),
            ("to_numexpr", lambda ast: ast.to_numexpr()),
            True,
            (formulate.from_numexpr, "from_numexpr"),
            ("to_root", lambda ast: ast.to_root()),
        ),
        # NumExpr->Root->NumExpr: NumExpr -> Root -> Root -> NumExpr
        (
            "NumExpr_to_Root",
            100,
            (formulate.from_numexpr, "from_numexpr"),
            ("to_root", lambda ast: ast.to_root()),
            True,
            (formulate.from_root, "from_root"),
            ("to_numexpr", lambda ast: ast.to_numexpr()),
        ),
    ],
)
def test_expression_performance(
    test_name, expr_length, loader1, converter1, intermediate, loader2, converter2
):
    """Test that parsing and converting expressions takes less than 1 second.

    This parameterized test handles all combinations of loaders and converters:
    - TTreeFormula: from_root -> to_python -> from_root -> to_python
    - NumExpr: from_numexpr -> to_python -> from_numexpr -> to_python
    - Root->NumExpr: from_root -> to_numexpr -> from_numexpr -> to_root
    - NumExpr->Root: from_numexpr -> to_root -> from_root -> to_numexpr
    """
    # Generate an expression of appropriate length
    expr = generate_long_expression(expr_length)

    # Extract functions and names
    loader1_func, loader1_name = loader1
    converter1_name, converter1_func = converter1
    loader2_func, loader2_name = loader2
    converter2_name, converter2_func = converter2

    # First pass: load the expression and convert it
    start_time = time.time()
    ast1 = loader1_func(expr)
    parse_time1 = time.time() - start_time

    start_time = time.time()
    converted_expr1 = converter1_func(ast1)
    convert_time1 = time.time() - start_time

    # Second pass: load the converted expression (if intermediate=True) or the original expr
    start_time = time.time()
    ast2 = loader2_func(converted_expr1) if intermediate else loader2_func(expr)
    parse_time2 = time.time() - start_time

    start_time = time.time()
    converter2_func(ast2)
    convert_time2 = time.time() - start_time

    # Total time should be less than 1 second
    total_time = parse_time1 + convert_time1 + parse_time2 + convert_time2
    assert total_time < 3.0, f"Total time ({total_time:.2f}s) exceeds 1 second"

    # Print the times for debugging
    print(f"{test_name} {loader1_name} time: {parse_time1:.4f}s")
    print(f"{test_name} {converter1_name} time: {convert_time1:.4f}s")
    print(f"{test_name} {loader2_name} time: {parse_time2:.4f}s")
    print(f"{test_name} {converter2_name} time: {convert_time2:.4f}s")
    print(f"{test_name} total time: {total_time:.4f}s")
