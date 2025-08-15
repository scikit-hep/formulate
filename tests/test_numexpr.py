from __future__ import annotations

import ast

import formulate


def test_simple_add():
    a = formulate.from_numexpr("a+2.0")
    out = a.to_numexpr()
    assert ast.unparse(ast.parse(out)) == ast.unparse(ast.parse("(a+2.0)"))


def test_simple_sub():
    a = formulate.from_numexpr("a-2.0")
    out = a.to_numexpr()
    assert ast.unparse(ast.parse(out)) == ast.unparse(ast.parse("(a-2.0)"))


def test_simple_mul():
    a = formulate.from_numexpr("f*2.0")
    out = a.to_numexpr()
    assert ast.unparse(ast.parse(out)) == ast.unparse(ast.parse("(f*2.0)"))


def test_simple_div():
    a = formulate.from_numexpr("a/2.0")
    out = a.to_numexpr()
    assert ast.unparse(ast.parse(out)) == ast.unparse(ast.parse("(a/2.0)"))


def test_simple_lt():
    a = formulate.from_numexpr("a<2.0")
    out = a.to_numexpr()
    assert ast.unparse(ast.parse(out)) == ast.unparse(ast.parse("(a<2.0)"))


def test_simple_lte():
    a = formulate.from_numexpr("a<=2.0")
    out = a.to_numexpr()
    assert ast.unparse(ast.parse(out)) == ast.unparse(ast.parse("(a<=2.0)"))


def test_simple_gt():
    a = formulate.from_numexpr("a>2.0")
    out = a.to_numexpr()
    assert ast.unparse(ast.parse(out)) == ast.unparse(ast.parse("(a>2.0)"))


def test_simple_gte():
    a = formulate.from_numexpr("a>=2.0")
    out = a.to_numexpr()
    assert ast.unparse(ast.parse(out)) == ast.unparse(ast.parse("(a>=2.0)"))


def test_simple_eq():
    a = formulate.from_numexpr("a==2.0")
    out = a.to_numexpr()
    assert ast.unparse(ast.parse(out)) == ast.unparse(ast.parse("(a==2.0)"))


def test_simple_neq():
    a = formulate.from_numexpr("a!=2.0")
    out = a.to_numexpr()
    assert ast.unparse(ast.parse(out)) == ast.unparse(ast.parse("(a!=2.0)"))


def test_simple_bor():
    a = formulate.from_numexpr("a|b")
    out = a.to_numexpr()
    assert ast.unparse(ast.parse(out)) == ast.unparse(ast.parse("a | b"))


def test_simple_band():
    a = formulate.from_numexpr("a&c")
    out = a.to_numexpr()
    assert ast.unparse(ast.parse(out)) == ast.unparse(ast.parse("a & c"))


def test_simple_bxor():
    a = formulate.from_numexpr("a^2.0")
    out = a.to_numexpr()
    assert ast.unparse(ast.parse(out)) == ast.unparse(ast.parse("(a^2.0)"))


def test_simple_pow():
    a = formulate.from_numexpr("a**2.0")
    out = a.to_numexpr()
    assert ast.unparse(ast.parse(out)) == ast.unparse(ast.parse("(a**2.0)"))


def test_simple_function():
    a = formulate.from_numexpr("sqrt(4)")
    out = a.to_numexpr()
    assert ast.unparse(ast.parse(out)) == ast.unparse(ast.parse("sqrt(4)"))


def test_simple_unary_pos():
    a = formulate.from_numexpr("+5.0")
    out = a.to_numexpr()
    assert ast.unparse(ast.parse(out)) == ast.unparse(ast.parse("(+5.0)"))


def test_simple_unary_neg():
    a = formulate.from_numexpr("-5.0")
    out = a.to_numexpr()
    assert ast.unparse(ast.parse(out)) == ast.unparse(ast.parse("(-5.0)"))


def test_simple_unary_binv():
    a = formulate.from_numexpr("~bool")
    out = a.to_numexpr()
    assert ast.unparse(ast.parse(out)) == ast.unparse(ast.parse("~bool"))


def test_unary_binary_pos():
    a = formulate.from_numexpr("2.0 - -6")
    out = a.to_numexpr()
    assert ast.unparse(ast.parse(out)) == ast.unparse(ast.parse("(2.0-(-6))"))


def test_complex_exp():
    a = formulate.from_numexpr("(~a**b)*23/(var|45)")
    out = a.to_numexpr()
    assert ast.unparse(ast.parse(out)) == ast.unparse(
        ast.parse("(((~(a**b))*23)/(var|45))")
    )


def test_multiple_lor():
    a = formulate.from_numexpr("a|b|c")
    out = a.to_numexpr()
    assert ast.unparse(ast.parse(out)) == ast.unparse(ast.parse("a | b | c"))


def test_multiple_land():
    a = formulate.from_numexpr("a&b&c")
    out = a.to_numexpr()
    assert ast.unparse(ast.parse(out)) == ast.unparse(ast.parse("a & b & c"))


# Removed redundant test_multiple_bor as it duplicates test_multiple_lor.


# Removed redundant test_multiple_band function.


def test_multiple_add():
    a = formulate.from_numexpr("a+b+c+d")
    out = a.to_numexpr()
    assert ast.unparse(ast.parse(out)) == ast.unparse(ast.parse("(((a+b)+c)+d)"))


def test_multiple_sub():
    a = formulate.from_numexpr("a-b-c-d")
    out = a.to_numexpr()
    assert ast.unparse(ast.parse(out)) == ast.unparse(ast.parse("(((a-b)-c)-d)"))


def test_multiple_mul():
    a = formulate.from_numexpr("a*b*c*d")
    out = a.to_numexpr()
    assert ast.unparse(ast.parse(out)) == ast.unparse(ast.parse("(((a*b)*c)*d)"))


def test_multiple_div():
    a = formulate.from_numexpr("a/b/c/d")
    out = a.to_numexpr()
    assert ast.unparse(ast.parse(out)) == ast.unparse(ast.parse("(((a/b)/c)/d)"))


def test_multiple_lor_four():
    a = formulate.from_numexpr("a|b|c|d")
    out = a.to_numexpr()
    assert ast.unparse(ast.parse(out)) == ast.unparse(ast.parse("a | b | c | d"))


def test_multiple_land_four():
    a = formulate.from_numexpr("a&b&c&d")
    out = a.to_numexpr()
    assert ast.unparse(ast.parse(out)) == ast.unparse(ast.parse("a & b & c & d"))


def test_multiple_bor_four():
    a = formulate.from_numexpr("a|b|c|d")
    out = a.to_numexpr()
    assert ast.unparse(ast.parse(out)) == ast.unparse(ast.parse("a | b | c | d"))


def test_multiple_band_four():
    a = formulate.from_numexpr("a&b&c&d")
    out = a.to_numexpr()
    assert ast.unparse(ast.parse(out)) == ast.unparse(ast.parse("a & b & c & d"))


def test_multiple_pow():
    a = formulate.from_numexpr("a**b**c**d")
    out = a.to_numexpr()
    assert ast.unparse(ast.parse(out)) == ast.unparse(ast.parse("(a**b**c**d)"))


def test_multiple_bxor():
    a = formulate.from_numexpr("a^b^c^d")
    out = a.to_numexpr()
    assert ast.unparse(ast.parse(out)) == ast.unparse(ast.parse("(a^b^c^d)"))
