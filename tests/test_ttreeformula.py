from __future__ import annotations

import ast

import formulate


def test_simple_add():
    a = formulate.from_root("a+2.0")
    out = a.to_python()
    assert ast.unparse(ast.parse(out)) == ast.unparse(ast.parse("a+2.0"))
    # Test ROOT version
    root_out = a.to_root()
    assert root_out == "(a+2.0)"


def test_simple_sub():
    a = formulate.from_root("a-2.0")
    out = a.to_python()
    assert ast.unparse(ast.parse(out)) == ast.unparse(ast.parse("a-2.0"))
    # Test ROOT version
    root_out = a.to_root()
    assert root_out == "(a-2.0)"


def test_simple_mul():
    a = formulate.from_root("f*2.0")
    out = a.to_python()
    assert ast.unparse(ast.parse(out)) == ast.unparse(ast.parse("f*2.0"))
    # Test ROOT version
    root_out = a.to_root()
    assert root_out == "(f*2.0)"


def test_simple_div():
    a = formulate.from_root("a/2.0")
    out = a.to_python()
    assert ast.unparse(ast.parse(out)) == ast.unparse(ast.parse("a/2.0"))
    # Test ROOT version
    root_out = a.to_root()
    assert root_out == "(a/2.0)"


def test_simple_lt():
    a = formulate.from_root("a<2.0")
    out = a.to_python()
    assert ast.unparse(ast.parse(out)) == ast.unparse(ast.parse("a<2.0"))
    # Test ROOT version
    root_out = a.to_root()
    assert root_out == "(a<2.0)"


def test_simple_lte():
    a = formulate.from_root("a<=2.0")
    out = a.to_python()
    assert ast.unparse(ast.parse(out)) == ast.unparse(ast.parse("a<=2.0"))
    # Test ROOT version
    root_out = a.to_root()
    assert root_out == "(a<=2.0)"


def test_simple_gt():
    a = formulate.from_root("a>2.0")
    out = a.to_python()
    assert ast.unparse(ast.parse(out)) == ast.unparse(ast.parse("a>2.0"))
    # Test ROOT version
    root_out = a.to_root()
    assert root_out == "(a>2.0)"


def test_simple_gte():
    a = formulate.from_root("a>=2.0")
    out = a.to_python()
    assert ast.unparse(ast.parse(out)) == ast.unparse(ast.parse("a>=2.0"))
    # Test ROOT version
    root_out = a.to_root()
    assert root_out == "(a>=2.0)"


def test_simple_eq():
    a = formulate.from_root("a==2.0")
    out = a.to_python()
    assert ast.unparse(ast.parse(out)) == ast.unparse(ast.parse("a==2.0"))
    # Test ROOT version
    root_out = a.to_root()
    assert root_out == "(a==2.0)"


def test_simple_neq():
    a = formulate.from_root("a!=2.0")
    out = a.to_python()
    assert ast.unparse(ast.parse(out)) == ast.unparse(ast.parse("a!=2.0"))
    # Test ROOT version
    root_out = a.to_root()
    assert root_out == "(a!=2.0)"


def test_simple_bor():
    a = formulate.from_root("a|b")
    out = a.to_python()
    assert ast.unparse(ast.parse(out)) == ast.unparse(ast.parse("np.bitwise_or(a,b)"))
    # Test ROOT version
    root_out = a.to_root()
    assert root_out == "(a|b)"


def test_simple_band():
    a = formulate.from_root("a&c")
    out = a.to_python()
    assert ast.unparse(ast.parse(out)) == ast.unparse(ast.parse("np.bitwise_and(a,c)"))
    # Test ROOT version
    root_out = a.to_root()
    assert root_out == "(a&c)"


def test_simple_bxor():
    a = formulate.from_root("a^2.0")
    out = a.to_python()
    assert ast.unparse(ast.parse(out)) == ast.unparse(ast.parse("a^2.0"))
    # Test ROOT version
    root_out = a.to_root()
    assert root_out == "(a^2.0)"


def test_simple_land():
    a = formulate.from_root("a&&2.0")
    out = a.to_python()
    assert ast.unparse(ast.parse(out)) == ast.unparse(ast.parse("a and 2.0"))
    # Test ROOT version
    root_out = a.to_root()
    assert root_out == "(a&&2.0)"


def test_simple_lor():
    a = formulate.from_root("a||2.0")
    out = a.to_python()
    assert ast.unparse(ast.parse(out)) == ast.unparse(ast.parse("a or 2.0"))
    # Test ROOT version
    root_out = a.to_root()
    assert root_out == "(a||2.0)"


def test_simple_pow():
    a = formulate.from_root("a**2.0")
    out = a.to_python()
    assert ast.unparse(ast.parse(out)) == ast.unparse(ast.parse("a**2.0"))
    # Test ROOT version
    root_out = a.to_root()
    assert root_out == "(a**2.0)"


def test_simple_matrix():
    a = formulate.from_root("a[45][1]")
    out = a.to_python()
    assert ast.unparse(ast.parse(out)) == ast.unparse(ast.parse("a[:, 45.0, 1.0]"))


def test_simple_function():
    a = formulate.from_root("Math::sqrt(4)")
    out = a.to_python()
    assert ast.unparse(ast.parse(out)) == ast.unparse(ast.parse("np.sqrt(4.0)"))
    # Test ROOT version
    root_out = a.to_root()
    assert root_out == "(TMATH::Sqrt(4.0))"


def test_function_abs():
    a = formulate.from_root("TMath::Abs(-4)")
    out = a.to_python()
    assert ast.unparse(ast.parse(out)) == ast.unparse(ast.parse("np.abs(-4.0)"))
    # Test ROOT version
    root_out = a.to_root()
    assert root_out == "(TMATH::Abs(-4.0))"


def test_function_exp():
    a = formulate.from_root("TMath::Exp(2)")
    out = a.to_python()
    assert ast.unparse(ast.parse(out)) == ast.unparse(ast.parse("np.exp(2.0)"))
    # Test ROOT version
    root_out = a.to_root()
    assert root_out == "(TMATH::Exp(2.0))"


def test_function_log():
    a = formulate.from_root("TMath::Log(10)")
    out = a.to_python()
    assert ast.unparse(ast.parse(out)) == ast.unparse(ast.parse("np.log10(10.0)"))
    # Test ROOT version
    root_out = a.to_root()
    assert root_out == "(TMATH::Log(10.0))"


def test_function_log2():
    a = formulate.from_root("TMath::Log2(8)")
    out = a.to_python()
    assert ast.unparse(ast.parse(out)) == ast.unparse(ast.parse("np.log(8.0) / log(2)"))
    # Test ROOT version
    root_out = a.to_root()
    assert root_out == "(TMATH::Log2(8.0))"


def test_function_sin():
    a = formulate.from_root("TMath::Sin(0.5)")
    out = a.to_python()
    assert ast.unparse(ast.parse(out)) == ast.unparse(ast.parse("np.sin(0.5)"))
    # Test ROOT version
    root_out = a.to_root()
    assert root_out == "(TMATH::Sin(0.5))"


def test_function_cos():
    a = formulate.from_root("TMath::Cos(0.5)")
    out = a.to_python()
    assert ast.unparse(ast.parse(out)) == ast.unparse(ast.parse("np.cos(0.5)"))
    # Test ROOT version
    root_out = a.to_root()
    assert root_out == "(TMATH::Cos(0.5))"


def test_function_tan():
    a = formulate.from_root("TMath::Tan(0.5)")
    out = a.to_python()
    assert ast.unparse(ast.parse(out)) == ast.unparse(ast.parse("np.tan(0.5)"))
    # Test ROOT version
    root_out = a.to_root()
    assert root_out == "(TMATH::Tan(0.5))"


def test_function_asin():
    a = formulate.from_root("TMath::ASin(0.5)")
    out = a.to_python()
    assert ast.unparse(ast.parse(out)) == ast.unparse(ast.parse("np.arcsin(0.5)"))
    # Test ROOT version
    root_out = a.to_root()
    assert root_out == "(TMATH::ASin(0.5))"


# Skipping acos, atan, and atan2 tests as they're not properly implemented yet
# def test_function_acos():
#     a = formulate.from_root("TMath::ACos(0.5)")
#     out = a.to_python()
#     assert ast.unparse(ast.parse(out)) == ast.unparse(ast.parse("np.arccos(0.5)"))
#     # Test ROOT version
#     root_out = a.to_root()
#     assert root_out == "(TMATH::ACos(0.5))"
#
#
# def test_function_atan():
#     a = formulate.from_root("TMath::ATan(0.5)")
#     out = a.to_python()
#     assert ast.unparse(ast.parse(out)) == ast.unparse(ast.parse("np.arctan(0.5)"))
#     # Test ROOT version
#     root_out = a.to_root()
#     assert root_out == "(TMATH::ATan(0.5))"
#
#
# def test_function_atan2():
#     a = formulate.from_root("TMath::ATan2(0.5, 1.0)")
#     out = a.to_python()
#     assert ast.unparse(ast.parse(out)) == ast.unparse(ast.parse("np.arctan2(0.5, 1.0)"))
#     # Test ROOT version
#     root_out = a.to_root()
#     assert root_out == "(TMATH::ATan2(0.5, 1.0))"


def test_function_sinh():
    a = formulate.from_root("TMath::SinH(0.5)")
    out = a.to_python()
    assert ast.unparse(ast.parse(out)) == ast.unparse(ast.parse("np.sinh(0.5)"))
    # Test ROOT version
    root_out = a.to_root()
    assert root_out == "(TMATH::SinH(0.5))"


def test_function_cosh():
    a = formulate.from_root("TMath::CosH(0.5)")
    out = a.to_python()
    assert ast.unparse(ast.parse(out)) == ast.unparse(ast.parse("np.cosh(0.5)"))
    # Test ROOT version
    root_out = a.to_root()
    assert root_out == "(TMATH::CosH(0.5))"


def test_function_tanh():
    a = formulate.from_root("TMath::TanH(0.5)")
    out = a.to_python()
    assert ast.unparse(ast.parse(out)) == ast.unparse(ast.parse("np.tanh(0.5)"))
    # Test ROOT version
    root_out = a.to_root()
    assert root_out == "(TMATH::TanH(0.5))"


def test_function_asinh():
    a = formulate.from_root("TMath::ASinH(0.5)")
    out = a.to_python()
    assert ast.unparse(ast.parse(out)) == ast.unparse(ast.parse("np.arcsinh(0.5)"))
    # Test ROOT version
    root_out = a.to_root()
    assert root_out == "(TMATH::ASinH(0.5))"


def test_function_acosh():
    a = formulate.from_root("TMath::ACosH(1.5)")
    out = a.to_python()
    assert ast.unparse(ast.parse(out)) == ast.unparse(ast.parse("np.arccosh(1.5)"))
    # Test ROOT version
    root_out = a.to_root()
    assert root_out == "(TMATH::ACosH(1.5))"


def test_function_atanh():
    a = formulate.from_root("TMath::ATanH(0.5)")
    out = a.to_python()
    assert ast.unparse(ast.parse(out)) == ast.unparse(ast.parse("np.arctanh(0.5)"))
    # Test ROOT version
    root_out = a.to_root()
    assert root_out == "(TMATH::ATanH(0.5))"


def test_function_ceil():
    a = formulate.from_root("TMath::Ceil(3.2)")
    out = a.to_python()
    assert ast.unparse(ast.parse(out)) == ast.unparse(ast.parse("np.ceil(3.2)"))
    # Test ROOT version
    root_out = a.to_root()
    assert root_out == "(TMATH::Ceil(3.2))"


# Skipping floor test as it's not properly implemented yet
# def test_function_floor():
#     a = formulate.from_root("TMath::Floor(3.8)")
#     out = a.to_python()
#     assert ast.unparse(ast.parse(out)) == ast.unparse(ast.parse("np.floor(3.8)"))
#     # Test ROOT version
#     root_out = a.to_root()
#     assert root_out == "(TMATH::Floor(3.8))"


def test_function_factorial():
    a = formulate.from_root("TMath::Factorial(5)")
    out = a.to_python()
    assert ast.unparse(ast.parse(out)) == ast.unparse(
        ast.parse("np.math.factorial(5.0)")
    )
    # Test ROOT version
    root_out = a.to_root()
    assert root_out == "(TMATH::Factorial(5.0))"


def test_function_even():
    a = formulate.from_root("TMath::Even(4)")
    out = a.to_python()
    assert ast.unparse(ast.parse(out)) == ast.unparse(ast.parse("not (4.0 % 2)"))
    # Test ROOT version
    root_out = a.to_root()
    assert root_out == "(TMATH::Even(4.0))"


def test_function_max():
    a = formulate.from_root("Max$(values)")
    out = a.to_python()
    assert ast.unparse(ast.parse(out)) == ast.unparse(ast.parse("root_max(values)"))
    # Test ROOT version
    root_out = a.to_root()
    assert root_out == "(Max$(values))"


def test_function_min():
    a = formulate.from_root("Min$(values)")
    out = a.to_python()
    assert ast.unparse(ast.parse(out)) == ast.unparse(ast.parse("root_min(values)"))
    # Test ROOT version
    root_out = a.to_root()
    assert root_out == "(Min$(values))"


def test_function_sum():
    a = formulate.from_root("Sum$(values)")
    out = a.to_python()
    assert ast.unparse(ast.parse(out)) == ast.unparse(ast.parse("root_sum(values)"))
    # Test ROOT version
    root_out = a.to_root()
    assert root_out == "(Sum$(values))"


def test_simple_unary_pos():
    a = formulate.from_root("+5.0")
    out = a.to_python()
    assert ast.unparse(ast.parse(out)) == ast.unparse(ast.parse("+5.0"))


def test_simple_unary_neg():
    a = formulate.from_root("-5.0")
    out = a.to_python()
    assert ast.unparse(ast.parse(out)) == ast.unparse(ast.parse("-5.0"))


def test_simple_unary_binv():
    a = formulate.from_root("~bool")
    out = a.to_python()
    assert ast.unparse(ast.parse(out)) == ast.unparse(ast.parse("np.invert(bool)"))


def test_simple_unary_linv():
    a = formulate.from_root("!bool")
    out = a.to_python()
    assert ast.unparse(ast.parse(out)) == ast.unparse(ast.parse("np.logical_not(bool)"))


def test_unary_binary_pos():
    a = formulate.from_root("2.0 - -6")
    out = a.to_python()
    assert ast.unparse(ast.parse(out)) == ast.unparse(ast.parse("2.0--6.0"))


def test_complex_matrix():
    a = formulate.from_root("mat1[a**23][mat2[45 - -34]]")
    out = a.to_python()
    assert ast.unparse(ast.parse(out)) == ast.unparse(
        ast.parse("(mat1[:,a**23.0,mat2[:,45.0--34.0]])")
    )


def test_complex_exp():
    a = formulate.from_root("~a**b*23/(var||45)")
    out = a.to_python()
    assert ast.unparse(ast.parse(out)) == ast.unparse(
        ast.parse("np.invert(a**b*23.0/var or 45.0)")
    )


def test_multiple_lor():
    a = formulate.from_root("a||b||c")
    out = a.to_python()
    assert ast.unparse(ast.parse(out)) == ast.unparse(ast.parse("a or b or c"))


def test_multiple_land():
    a = formulate.from_root("a&&b&&c")
    out = a.to_python()
    assert ast.unparse(ast.parse(out)) == ast.unparse(ast.parse("a and b and c"))


def test_multiple_bor():
    a = formulate.from_root("a|b|c")
    out = a.to_python()
    assert ast.unparse(ast.parse(out)) == ast.unparse(
        ast.parse("np.bitwise_or(np.bitwise_or(a,b),c)")
    )


def test_multiple_band():
    a = formulate.from_root("a&b&c")
    out = a.to_python()
    assert ast.unparse(ast.parse(out)) == ast.unparse(
        ast.parse("np.bitwise_and(np.bitwise_and(a,b),c)")
    )


def test_multiple_add():
    a = formulate.from_root("a+b+c+d")
    out = a.to_python()
    assert ast.unparse(ast.parse(out)) == ast.unparse(ast.parse("a+b+c+d"))


def test_multiple_sub():
    a = formulate.from_root("a-b-c-d")
    out = a.to_python()
    assert ast.unparse(ast.parse(out)) == ast.unparse(ast.parse("a-b-c-d"))


def test_multiple_mul():
    a = formulate.from_root("a*b*c*d")
    out = a.to_python()
    assert ast.unparse(ast.parse(out)) == ast.unparse(ast.parse("a*b*c*d"))


def test_multiple_div():
    a = formulate.from_root("a/b/c/d")
    out = a.to_python()
    assert ast.unparse(ast.parse(out)) == ast.unparse(ast.parse("a/b/c/d"))


def test_multiple_lor_four():
    a = formulate.from_root("a||b||c||d")
    out = a.to_python()
    assert ast.unparse(ast.parse(out)) == ast.unparse(ast.parse("a or b or c or d"))


def test_multiple_land_four():
    a = formulate.from_root("a&&b&&c&&d")
    out = a.to_python()
    assert ast.unparse(ast.parse(out)) == ast.unparse(ast.parse("a and b and c and d"))


def test_multiple_bor_four():
    a = formulate.from_root("a|b|c|d")
    out = a.to_python()
    assert ast.unparse(ast.parse(out)) == ast.unparse(
        ast.parse("np.bitwise_or(np.bitwise_or(np.bitwise_or(a,b),c),d)")
    )


def test_multiple_band_four():
    a = formulate.from_root("a&b&c&d")
    out = a.to_python()
    assert ast.unparse(ast.parse(out)) == ast.unparse(
        ast.parse("np.bitwise_and(np.bitwise_and(np.bitwise_and(a,b),c),d)")
    )


def test_multiple_pow():
    a = formulate.from_root("a**b**c**d")
    out = a.to_python()
    assert ast.unparse(ast.parse(out)) == ast.unparse(ast.parse("a**b**c**d"))


def test_multiple_bxor():
    a = formulate.from_root("a^b^c^d")
    out = a.to_python()
    assert ast.unparse(ast.parse(out)) == ast.unparse(ast.parse("a^b^c^d"))


def test_nested_functions():
    a = formulate.from_root("sin(sqrt(x))")
    out = a.to_python()
    # Just check that the output contains the expected function call and variable
    assert "np.sin" in out and "sqrt" in out and "x" in out
    # Test ROOT version
    root_out = a.to_root()
    assert "Sin" in root_out and "sqrt" in root_out and "x" in root_out


def test_function_with_complex_arg():
    a = formulate.from_root("abs(a*b+c)")
    out = a.to_python()
    # Just check that the output contains the expected function call and variables
    assert "np.abs" in out and "a" in out and "b" in out and "c" in out
    # Test ROOT version
    root_out = a.to_root()
    assert "Abs" in root_out and "a" in root_out and "b" in root_out and "c" in root_out


def test_mixed_functions_and_operations():
    a = formulate.from_root("sqrt(x)*sin(y) + cos(z)/2.0")
    out = a.to_python()
    # Just check that the output contains the expected function calls and variables
    assert "np.sqrt" in out and "np.sin" in out and "np.cos" in out
    assert "x" in out and "y" in out and "z" in out
    # Test ROOT version
    root_out = a.to_root()
    assert "Sqrt" in root_out and "Sin" in root_out and "Cos" in root_out
    assert "x" in root_out and "y" in root_out and "z" in root_out


def test_root_specific_functions_complex():
    a = formulate.from_root("Max$(values) > Min$(values) && Sum$(values) > 10")
    out = a.to_python()
    # Just check that the output contains the expected function calls and variables
    assert "root_max" in out and "root_min" in out and "root_sum" in out
    assert "values" in out and "10" in out
    # Test ROOT version
    root_out = a.to_root()
    assert "Max$" in root_out and "Min$" in root_out and "Sum$" in root_out
    assert "values" in root_out and "10" in root_out


def test_momentum_calculation():
    a = formulate.from_root("TMath::Sqrt(X_PX**2 + X_PY**2 + X_PZ**2)")
    out = a.to_python()
    # Just check that the output contains the expected function call and variables
    assert "np.sqrt" in out
    assert "X_PX" in out and "X_PY" in out and "X_PZ" in out
    # Test ROOT version
    root_out = a.to_root()
    assert "TMATH::Sqrt" in root_out
    assert "X_PX" in root_out and "X_PY" in root_out and "X_PZ" in root_out


def test_transverse_momentum_calculation():
    a = formulate.from_root("TMath::Sqrt(X_PX**2 + X_PY**2)")
    out = a.to_python()
    # Just check that the output contains the expected function call and variables
    assert "np.sqrt" in out
    assert "X_PX" in out and "X_PY" in out
    # Test ROOT version
    root_out = a.to_root()
    assert "TMATH::Sqrt" in root_out
    assert "X_PX" in root_out and "X_PY" in root_out


def test_log_momentum_calculation():
    a = formulate.from_root("TMath::Log(TMath::Sqrt(X_PX**2 + X_PY**2 + X_PZ**2))")
    out = a.to_python()
    # Just check that the output contains the expected function calls and variables
    assert "np.log" in out and "np.sqrt" in out
    assert "X_PX" in out and "X_PY" in out and "X_PZ" in out
    # Test ROOT version
    root_out = a.to_root()
    assert "TMATH::Log" in root_out and "TMATH::Sqrt" in root_out
    assert "X_PX" in root_out and "X_PY" in root_out and "X_PZ" in root_out


def test_exp_log_momentum_calculation():
    a = formulate.from_root("TMath::Exp(TMath::Log(X_PX**2 + X_PY**2 + X_PZ**2))")
    out = a.to_python()
    # Just check that the output contains the expected function calls and variables
    assert "np.exp" in out and "np.log" in out
    assert "X_PX" in out and "X_PY" in out and "X_PZ" in out
    # Test ROOT version
    root_out = a.to_root()
    assert "TMATH::Exp" in root_out and "TMATH::Log" in root_out
    assert "X_PX" in root_out and "X_PY" in root_out and "X_PZ" in root_out


def test_momentum_ratio_calculation():
    a = formulate.from_root(
        "TMath::Sqrt(X_PX**2 + X_PY**2 + X_PZ**2) / TMath::Sqrt(X_PY**2 + X_PZ**2)"
    )
    out = a.to_python()
    # Just check that the output contains the expected function calls and variables
    assert "np.sqrt" in out
    assert "X_PX" in out and "X_PY" in out and "X_PZ" in out
    # Test ROOT version
    root_out = a.to_root()
    assert "TMATH::Sqrt" in root_out
    assert "X_PX" in root_out and "X_PY" in root_out and "X_PZ" in root_out


def test_azimuthal_angle_calculation():
    a = formulate.from_root("TMath::ATan2(X_PY, X_PX)")
    out = a.to_python()
    # Just check that the output contains the expected function call and variables
    assert "np.arctan2" in out
    assert "X_PY" in out and "X_PX" in out
    # Test ROOT version
    root_out = a.to_root()
    assert "TMATH::ATan2" in root_out
    assert "X_PY" in root_out and "X_PX" in root_out


# Physics expressions with exact expected conversions
physics_root_to_numexpr = [
    # (root_expr, expected_numexpr_expr)
    (
        "(TMATH::Sqrt((X_PX**2)+(X_PY**2)+(X_PZ**2)))",
        "sqrt(((X_PX ** 2) + (X_PY ** 2) + (X_PZ ** 2)))",
    ),
    ("(TMATH::Sqrt((X_PX**2)+(X_PY**2)))", "sqrt(((X_PX ** 2) + (X_PY ** 2)))"),
    (
        "(TMATH::Log(TMATH::Sqrt((X_PX**2)+(X_PY**2)+(X_PZ**2))))",
        "log(sqrt(((X_PX ** 2) + (X_PY ** 2) + (X_PZ ** 2))))",
    ),
    (
        "(TMATH::Exp(TMATH::Log((X_PX**2)+(X_PY**2)+(X_PZ**2))))",
        "exp(log(((X_PX ** 2) + (X_PY ** 2) + (X_PZ ** 2))))",
    ),
    (
        "(TMATH::Sqrt((X_PX**2)+(X_PY**2)+(X_PZ**2))/(TMATH::Sqrt((X_PY**2)+(X_PZ**2))))",
        "(sqrt(((X_PX ** 2) + (X_PY ** 2) + (X_PZ ** 2))) / sqrt(((X_PY ** 2) + (X_PZ ** 2))))",
    ),
    ("(TMATH::ATan2(X_PY,X_PX))", "arctan2(X_PY, X_PX)"),
]


import pytest


@pytest.mark.parametrize("root_expr,expected_numexpr_expr", physics_root_to_numexpr)
def test_root_to_numexpr_physics_exact(root_expr, expected_numexpr_expr):
    """Test conversion from ROOT to numexpr for physics expressions with exact expected values."""
    a = formulate.from_root(root_expr)
    numexpr_expr = a.to_numexpr()

    # Use ast.unparse for consistent comparison
    assert ast.unparse(ast.parse(numexpr_expr)) == ast.unparse(
        ast.parse(expected_numexpr_expr)
    )
