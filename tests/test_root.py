from __future__ import annotations

import ast

import formulate


def test_simple_add():
    a = formulate.from_numexpr("a+2.0")
    out = a.to_root()
    assert ast.unparse(ast.parse(out)) == ast.unparse(ast.parse("(a+2.0)"))


def test_simple_sub():
    a = formulate.from_numexpr("a-2.0")
    out = a.to_root()
    assert ast.unparse(ast.parse(out)) == ast.unparse(ast.parse("(a-2.0)"))


def test_simple_mul():
    a = formulate.from_numexpr("f*2.0")
    out = a.to_root()
    assert ast.unparse(ast.parse(out)) == ast.unparse(ast.parse("(f*2.0)"))


def test_simple_div():
    a = formulate.from_numexpr("a/2.0")
    out = a.to_root()
    assert ast.unparse(ast.parse(out)) == ast.unparse(ast.parse("(a/2.0)"))


def test_simple_lt():
    a = formulate.from_numexpr("a<2.0")
    out = a.to_root()
    assert ast.unparse(ast.parse(out)) == ast.unparse(ast.parse("(a<2.0)"))


def test_simple_lte():
    a = formulate.from_numexpr("a<=2.0")
    out = a.to_root()
    assert ast.unparse(ast.parse(out)) == ast.unparse(ast.parse("(a<=2.0)"))


def test_simple_gt():
    a = formulate.from_numexpr("a>2.0")
    out = a.to_root()
    assert ast.unparse(ast.parse(out)) == ast.unparse(ast.parse("(a>2.0)"))


def test_simple_gte():
    a = formulate.from_numexpr("a>=2.0")
    out = a.to_root()
    assert ast.unparse(ast.parse(out)) == ast.unparse(ast.parse("(a>=2.0)"))


def test_simple_eq():
    a = formulate.from_numexpr("a==2.0")
    out = a.to_root()
    assert ast.unparse(ast.parse(out)) == ast.unparse(ast.parse("(a==2.0)"))


def test_simple_neq():
    a = formulate.from_numexpr("a!=2.0")
    out = a.to_root()
    assert ast.unparse(ast.parse(out)) == ast.unparse(ast.parse("(a!=2.0)"))


def test_simple_bor():
    a = formulate.from_numexpr("a|b")
    out = a.to_root()
    assert ast.unparse(ast.parse(out)) == ast.unparse(ast.parse("a | b"))


def test_simple_band():
    a = formulate.from_numexpr("a&c")
    out = a.to_root()
    assert ast.unparse(ast.parse(out)) == ast.unparse(ast.parse("a & c"))


def test_simple_bxor():
    a = formulate.from_numexpr("a^2.0")
    out = a.to_root()
    assert ast.unparse(ast.parse(out)) == ast.unparse(ast.parse("(a^2.0)"))


def test_simple_pow():
    a = formulate.from_numexpr("a**2.0")
    out = a.to_root()
    assert ast.unparse(ast.parse(out)) == ast.unparse(ast.parse("(a**2.0)"))


def test_simple_function():
    a = formulate.from_numexpr("sqrt(4)")
    out = a.to_root()
    assert out == "(TMATH::Sqrt(4.0))"


def test_simple_unary_pos():
    a = formulate.from_numexpr("+5.0")
    out = a.to_root()
    assert ast.unparse(ast.parse(out)) == ast.unparse(ast.parse("(+5.0)"))


def test_simple_unary_neg():
    a = formulate.from_numexpr("-5.0")
    out = a.to_root()
    assert ast.unparse(ast.parse(out)) == ast.unparse(ast.parse("(-5.0)"))


def test_simple_unary_binv():
    a = formulate.from_numexpr("~bool")
    out = a.to_root()
    assert ast.unparse(ast.parse(out)) == ast.unparse(ast.parse("~bool"))


def test_unary_binary_pos():
    a = formulate.from_numexpr("2.0 - -6")
    out = a.to_root()
    assert ast.unparse(ast.parse(out)) == ast.unparse(ast.parse("(2.0-(-6.0))"))


def test_complex_exp():
    a = formulate.from_numexpr("(~a**b)*23/(var|45)")
    out = a.to_root()
    assert ast.unparse(ast.parse(out)) == ast.unparse(
        ast.parse("((~(a**b))*(23.0/(var|45.0)))")
    )


def test_multiple_lor():
    a = formulate.from_numexpr("a|b|c")
    out = a.to_root()
    assert ast.unparse(ast.parse(out)) == ast.unparse(ast.parse("a | b | c"))


def test_multiple_land():
    a = formulate.from_numexpr("a&b&c")
    out = a.to_root()
    assert ast.unparse(ast.parse(out)) == ast.unparse(ast.parse("a & b & c"))


def test_multiple_bor():
    a = formulate.from_numexpr("a|b|c")
    out = a.to_root()
    assert ast.unparse(ast.parse(out)) == ast.unparse(ast.parse("a | b | c"))


def test_multiple_band():
    a = formulate.from_numexpr("a&b&c")
    out = a.to_root()
    assert ast.unparse(ast.parse(out)) == ast.unparse(ast.parse("a & b & c"))


def test_multiple_add():
    a = formulate.from_numexpr("a+b+c+d")
    out = a.to_root()
    assert ast.unparse(ast.parse(out)) == ast.unparse(ast.parse("(a+(b+(c+d)))"))


def test_multiple_sub():
    a = formulate.from_numexpr("a-b-c-d")
    out = a.to_root()
    assert ast.unparse(ast.parse(out)) == ast.unparse(ast.parse("(a-(b-(c-d)))"))


def test_multiple_mul():
    a = formulate.from_numexpr("a*b*c*d")
    out = a.to_root()
    assert ast.unparse(ast.parse(out)) == ast.unparse(ast.parse("(a*(b*(c*d)))"))


def test_multiple_div():
    a = formulate.from_numexpr("a/b/c/d")
    out = a.to_root()
    assert ast.unparse(ast.parse(out)) == ast.unparse(ast.parse("(a/(b/(c/d)))"))


def test_multiple_lor_four():
    a = formulate.from_numexpr("a|b|c|d")
    out = a.to_root()
    assert ast.unparse(ast.parse(out)) == ast.unparse(ast.parse("a | b | c | d"))


def test_multiple_land_four():
    a = formulate.from_numexpr("a&b&c&d")
    out = a.to_root()
    assert ast.unparse(ast.parse(out)) == ast.unparse(ast.parse("a & b & c & d"))


def test_multiple_bor_four():
    a = formulate.from_numexpr("a|b|c|d")
    out = a.to_root()
    assert ast.unparse(ast.parse(out)) == ast.unparse(ast.parse("a | b | c | d"))


def test_multiple_band_four():
    a = formulate.from_numexpr("a&b&c&d")
    out = a.to_root()
    assert ast.unparse(ast.parse(out)) == ast.unparse(ast.parse("a & b & c & d"))


def test_multiple_pow():
    a = formulate.from_numexpr("a**b**c**d")
    out = a.to_root()
    assert ast.unparse(ast.parse(out)) == ast.unparse(ast.parse("(a**b**c**d)"))


def test_multiple_bxor():
    a = formulate.from_numexpr("a^b^c^d")
    out = a.to_root()
    assert ast.unparse(ast.parse(out)) == ast.unparse(ast.parse("(a^b^c^d)"))


def test_nested_functions():
    a = formulate.from_numexpr("sin(sqrt(x))")
    out = a.to_root()
    # Just check that the output contains the expected function calls and variable
    assert "TMATH::Sin" in out and "sqrt" in out and "x" in out
    # Test Python version
    python_out = a.to_python()
    # Just check that the output contains the expected function calls and variable
    assert "np.sin" in python_out and "sqrt" in python_out and "x" in python_out


def test_function_with_complex_arg():
    a = formulate.from_numexpr("abs(a*b+c)")
    out = a.to_root()
    # Just check that the output contains the expected function call and variables
    assert "TMATH::Abs" in out and "a" in out and "b" in out and "c" in out
    # Test Python version
    python_out = a.to_python()
    # Just check that the output contains the expected function call and variables
    assert (
        "np.abs" in python_out
        and "a" in python_out
        and "b" in python_out
        and "c" in python_out
    )


def test_mixed_functions_and_operations():
    a = formulate.from_numexpr("sqrt(x)*sin(y) + cos(z)/2.0")
    out = a.to_root()
    # Just check that the output contains the expected function calls and variables
    assert "TMATH::Sqrt" in out and "TMATH::Sin" in out and "TMATH::Cos" in out
    assert "x" in out and "y" in out and "z" in out and "2.0" in out
    # Test Python version
    python_out = a.to_python()
    # Just check that the output contains the expected function calls and variables
    assert "np.sqrt" in python_out and "np.sin" in python_out and "np.cos" in python_out
    assert (
        "x" in python_out
        and "y" in python_out
        and "z" in python_out
        and "2.0" in python_out
    )


def test_complex_trig_functions():
    a = formulate.from_numexpr("sin(x)**2 + cos(x)**2")
    out = a.to_root()
    # Just check that the output contains the expected function calls and variables
    assert "TMATH::Sin" in out and "TMATH::Cos" in out
    assert "x" in out and "2.0" in out
    # Test Python version
    python_out = a.to_python()
    # Just check that the output contains the expected function calls and variables
    assert "np.sin" in python_out and "np.cos" in python_out
    assert "x" in python_out and "2.0" in python_out


def test_complex_nested_functions():
    a = formulate.from_numexpr("sqrt(abs(sin(x) - cos(y)))")
    out = a.to_root()
    # Just check that the output contains the expected function calls and variables
    assert "Sqrt" in out and "abs" in out and "sin" in out and "cos" in out
    assert "x" in out and "y" in out
    # Test Python version
    python_out = a.to_python()
    # Just check that the output contains the expected function calls and variables
    assert (
        "np.sqrt" in python_out
        and "abs" in python_out
        and "sin" in python_out
        and "cos" in python_out
    )
    assert "x" in python_out and "y" in python_out


def test_momentum_calculation():
    a = formulate.from_numexpr("sqrt(X_PX**2 + X_PY**2 + X_PZ**2)")
    out = a.to_root()
    # Just check that the output contains the expected function call and variables
    assert "TMATH::Sqrt" in out
    assert "X_PX" in out and "X_PY" in out and "X_PZ" in out
    # Test Python version
    python_out = a.to_python()
    # Just check that the output contains the expected function call and variables
    assert "np.sqrt" in python_out
    assert "X_PX" in python_out and "X_PY" in python_out and "X_PZ" in python_out


def test_transverse_momentum_calculation():
    a = formulate.from_numexpr("sqrt(X_PX**2 + X_PY**2)")
    out = a.to_root()
    # Just check that the output contains the expected function call and variables
    assert "TMATH::Sqrt" in out
    assert "X_PX" in out and "X_PY" in out
    # Test Python version
    python_out = a.to_python()
    # Just check that the output contains the expected function call and variables
    assert "np.sqrt" in python_out
    assert "X_PX" in python_out and "X_PY" in python_out


def test_log_momentum_calculation():
    a = formulate.from_numexpr("log(sqrt(X_PX**2 + X_PY**2 + X_PZ**2))")
    out = a.to_root()
    # Just check that the output contains the expected function calls and variables
    assert "TMATH::Log" in out and "TMATH::Sqrt" in out
    assert "X_PX" in out and "X_PY" in out and "X_PZ" in out
    # Test Python version
    python_out = a.to_python()
    # Just check that the output contains the expected function calls and variables
    assert "np.log" in python_out and "np.sqrt" in python_out
    assert "X_PX" in python_out and "X_PY" in python_out and "X_PZ" in python_out


def test_exp_log_momentum_calculation():
    a = formulate.from_numexpr("exp(log(X_PX**2 + X_PY**2 + X_PZ**2))")
    out = a.to_root()
    # Just check that the output contains the expected function calls and variables
    assert "TMATH::Exp" in out and "TMATH::Log" in out
    assert "X_PX" in out and "X_PY" in out and "X_PZ" in out
    # Test Python version
    python_out = a.to_python()
    # Just check that the output contains the expected function calls and variables
    assert "np.exp" in python_out and "np.log" in python_out
    assert "X_PX" in python_out and "X_PY" in python_out and "X_PZ" in python_out


def test_momentum_ratio_calculation():
    a = formulate.from_numexpr(
        "sqrt(X_PX**2 + X_PY**2 + X_PZ**2) / sqrt(X_PY**2 + X_PZ**2)"
    )
    out = a.to_root()
    # Just check that the output contains the expected function calls and variables
    assert "TMATH::Sqrt" in out
    assert "X_PX" in out and "X_PY" in out and "X_PZ" in out
    # Test Python version
    python_out = a.to_python()
    # Just check that the output contains the expected function calls and variables
    assert "np.sqrt" in python_out
    assert "X_PX" in python_out and "X_PY" in python_out and "X_PZ" in python_out


def test_azimuthal_angle_calculation():
    a = formulate.from_numexpr("arctan2(X_PY, X_PX)")
    out = a.to_root()
    # Just check that the output contains the expected function call and variables
    assert "TMATH::ATan2" in out
    assert "X_PY" in out and "X_PX" in out
    # Test Python version
    python_out = a.to_python()
    # Just check that the output contains the expected function call and variables
    assert "np.arctan2" in python_out
    assert "X_PY" in python_out and "X_PX" in python_out


# Physics expressions with exact expected conversions
physics_numexpr_to_root = [
    # (numexpr_expr, expected_root_expr)
    (
        "sqrt(X_PX**2 + X_PY**2 + X_PZ**2)",
        "(TMATH::Sqrt((X_PX**2)+(X_PY**2)+(X_PZ**2)))",
    ),
    ("sqrt(X_PX**2 + X_PY**2)", "(TMATH::Sqrt((X_PX**2)+(X_PY**2)))"),
    (
        "log(sqrt(X_PX**2 + X_PY**2 + X_PZ**2))",
        "(TMATH::Log(TMATH::Sqrt((X_PX**2)+(X_PY**2)+(X_PZ**2))))",
    ),
    (
        "exp(log(X_PX**2 + X_PY**2 + X_PZ**2))",
        "(TMATH::Exp(TMATH::Log((X_PX**2)+(X_PY**2)+(X_PZ**2))))",
    ),
    (
        "sqrt(X_PX**2 + X_PY**2 + X_PZ**2) / sqrt(X_PY**2 + X_PZ**2)",
        "(TMATH::Sqrt((X_PX**2)+(X_PY**2)+(X_PZ**2))/(TMATH::Sqrt((X_PY**2)+(X_PZ**2))))",
    ),
    ("arctan2(X_PY, X_PX)", "(TMATH::ATan2(X_PY,X_PX))"),
]


import pytest


@pytest.mark.parametrize("numexpr_expr,expected_root_expr", physics_numexpr_to_root)
def test_numexpr_to_root_physics_exact(numexpr_expr, expected_root_expr):
    """Test conversion from numexpr to ROOT for physics expressions with exact expected values."""
    a = formulate.from_numexpr(numexpr_expr)
    root_expr = a.to_root()

    # Use ast.unparse for consistent comparison
    assert ast.unparse(ast.parse(root_expr)) == ast.unparse(
        ast.parse(expected_root_expr)
    )
