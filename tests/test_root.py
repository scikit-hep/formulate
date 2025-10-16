from __future__ import annotations

import ast

import pytest

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


def test_simple_or():
    a = formulate.from_numexpr("a|b")
    out = a.to_root()
    assert out == "(a || b)"


def test_simple_and():
    a = formulate.from_numexpr("a&c")
    out = a.to_root()
    assert out == "(a && c)"


def test_simple_xor():
    a = formulate.from_numexpr("a^2.0")
    with pytest.raises(ValueError):
        a.to_root()


def test_simple_pow():
    a = formulate.from_numexpr("a**2.0")
    out = a.to_root()
    assert ast.unparse(ast.parse(out)) == ast.unparse(ast.parse("(a**2.0)"))


def test_simple_function():
    a = formulate.from_numexpr("sqrt(4)")
    out = a.to_root()
    assert out == "TMath::Sqrt(4)"


def test_simple_unary_pos():
    a = formulate.from_numexpr("+5.0")
    out = a.to_root()
    assert ast.unparse(ast.parse(out)) == ast.unparse(ast.parse("(+5.0)"))


def test_simple_unary_neg():
    a = formulate.from_numexpr("-5.0")
    out = a.to_root()
    assert ast.unparse(ast.parse(out)) == ast.unparse(ast.parse("(-5.0)"))


def test_simple_unary_inv():
    a = formulate.from_numexpr("~bool")
    out = a.to_root()
    assert out == "(!bool)"


def test_unary_binary_pos():
    a = formulate.from_numexpr("2.0 - -6")
    out = a.to_root()
    assert ast.unparse(ast.parse(out)) == ast.unparse(ast.parse("(2.0-(-6))"))


def test_complex_exp():
    a = formulate.from_numexpr("(~a**b)*23/(var|45)")
    out = a.to_root()
    assert out == "(((!(a ** b)) * 23) / (var || 45))"


def test_multiple_or():
    a = formulate.from_numexpr("a|b|c")
    out = a.to_root()
    assert out == "((a || b) || c)"


def test_multiple_and():
    a = formulate.from_numexpr("a&b&c")
    out = a.to_root()
    assert out == "((a && b) && c)"


def test_multiple_add():
    a = formulate.from_numexpr("a+b+c+d")
    out = a.to_root()
    assert ast.unparse(ast.parse(out)) == ast.unparse(ast.parse("(((a+b)+c)+d)"))


def test_multiple_sub():
    a = formulate.from_numexpr("a-b-c-d")
    out = a.to_root()
    assert ast.unparse(ast.parse(out)) == ast.unparse(ast.parse("(((a-b)-c)-d)"))


def test_multiple_mul():
    a = formulate.from_numexpr("a*b*c*d")
    out = a.to_root()
    assert ast.unparse(ast.parse(out)) == ast.unparse(ast.parse("(((a*b)*c)*d)"))


def test_multiple_div():
    a = formulate.from_numexpr("a/b/c/d")
    out = a.to_root()
    assert ast.unparse(ast.parse(out)) == ast.unparse(ast.parse("(((a/b)/c)/d)"))


def test_multiple_or_four():
    a = formulate.from_numexpr("a|b|c|d")
    out = a.to_root()
    assert out == "(((a || b) || c) || d)"


def test_multiple_and_four():
    a = formulate.from_numexpr("a&b&c&d")
    out = a.to_root()
    assert out == "(((a && b) && c) && d)"


def test_multiple_pow():
    a = formulate.from_numexpr("a**b**c**d")
    out = a.to_root()
    assert ast.unparse(ast.parse(out)) == ast.unparse(ast.parse("(a**b**c**d)"))
