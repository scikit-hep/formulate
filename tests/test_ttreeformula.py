# -*- coding: utf-8 -*-
from __future__ import annotations

import formulate

from formulate.toast import toast

import ast


def test_simple_add():
    a = formulate.from_root(("a+2.0"))
    out = a.to_python()
    assert ast.unparse(ast.parse(out)) == ast.unparse(ast.parse("a+2.0"))


def test_simple_sub():
    a = formulate.from_root(("a-2.0"))
    out = a.to_python()
    assert ast.unparse(ast.parse(out)) == ast.unparse(ast.parse("a-2.0"))


def test_simple_mul():
    a = formulate.from_root(("f*2.0"))
    out = a.to_python()
    assert ast.unparse(ast.parse(out)) == ast.unparse(ast.parse("f*2.0"))


def test_simple_div():
    a = formulate.from_root(("a/2.0"))
    out = a.to_python()
    assert ast.unparse(ast.parse(out)) == ast.unparse(ast.parse("a/2.0"))


def test_simple_lt():
    a = formulate.from_root(("a<2.0"))
    out = a.to_python()
    assert ast.unparse(ast.parse(out)) == ast.unparse(ast.parse("a<2.0"))


def test_simple_lte():
    a = formulate.from_root(("a<=2.0"))
    out = a.to_python()
    assert ast.unparse(ast.parse(out)) == ast.unparse(ast.parse("a<=2.0"))


def test_simple_gt():
    a = formulate.from_root(("a>2.0"))
    out = a.to_python()
    assert ast.unparse(ast.parse(out)) == ast.unparse(ast.parse("a>2.0"))


def test_simple_gte():
    a = formulate.from_root(("a>=2.0"))
    out = a.to_python()
    assert ast.unparse(ast.parse(out)) == ast.unparse(ast.parse("a>=2.0"))


def test_simple_eq():
    a = formulate.from_root(("a==2.0"))
    out = a.to_python()
    assert ast.unparse(ast.parse(out)) == ast.unparse(ast.parse("a==2.0"))


def test_simple_neq():
    a = formulate.from_root(("a!=2.0"))
    out = a.to_python()
    assert ast.unparse(ast.parse(out)) == ast.unparse(ast.parse("a!=2.0"))


def test_simple_bor():
    a = formulate.from_root(("a|b"))
    out = a.to_python()
    assert ast.unparse(ast.parse(out)) == ast.unparse(ast.parse("np.bitwise_or(a,b)"))


def test_simple_band():
    a = formulate.from_root(("a&c"))
    out = a.to_python()
    assert ast.unparse(ast.parse(out)) == ast.unparse(ast.parse("np.bitwise_and(a,c)"))


def test_simple_bxor():
    a = formulate.from_root(("a^2.0"))
    out = a.to_python()
    assert ast.unparse(ast.parse(out)) == ast.unparse(ast.parse("a^2.0"))


def test_simple_land():
    a = formulate.from_root(("a&&2.0"))
    out = a.to_python()
    assert ast.unparse(ast.parse(out)) == ast.unparse(ast.parse("a and 2.0"))


def test_simple_lor():
    a = formulate.from_root(("a||2.0"))
    out = a.to_python()
    assert ast.unparse(ast.parse(out)) == ast.unparse(ast.parse("a or 2.0"))


def test_simple_pow():
    a = formulate.from_root(("a**2.0"))
    out = a.to_python()
    assert ast.unparse(ast.parse(out)) == ast.unparse(ast.parse("a**2.0"))


def test_simple_matrix():
    a = formulate.from_root(("a[45][1]"))
    out = a.to_python()
    assert ast.unparse(ast.parse(out)) == ast.unparse(ast.parse("a[:, 45.0, 1.0]"))


def test_simple_function():
    a = formulate.from_root(("Math::sqrt(4)"))
    out = a.to_python()
    assert ast.unparse(ast.parse(out)) == ast.unparse(ast.parse("np.sqrt(4.0)"))


def test_simple_unary_pos():
    a = formulate.from_root(("+5.0"))
    out = a.to_python()
    assert ast.unparse(ast.parse(out)) == ast.unparse(ast.parse("+5.0"))


def test_simple_unary_neg():
    a = formulate.from_root(("-5.0"))
    out = a.to_python()
    assert ast.unparse(ast.parse(out)) == ast.unparse(ast.parse("-5.0"))


def test_simple_unary_binv():
    a = formulate.from_root(("~bool"))
    out = a.to_python()
    assert ast.unparse(ast.parse(out)) == ast.unparse(ast.parse("np.invert(bool)"))


def test_simple_unary_linv():
    a = formulate.from_root(("!bool"))
    out = a.to_python()
    assert ast.unparse(ast.parse(out)) == ast.unparse(ast.parse("np.logical_not(bool)"))


def test_unary_binary_pos():
    a = formulate.from_root(("2.0 - -6"))
    out = a.to_python()
    assert ast.unparse(ast.parse(out)) == ast.unparse(ast.parse("2.0--6.0"))


def test_complex_matrix():
    a = formulate.from_root(("mat1[a**23][mat2[45 - -34]]"))
    out = a.to_python()
    assert ast.unparse(ast.parse(out)) == ast.unparse(ast.parse("(mat1[:,a**23.0,mat2[:,45.0--34.0]])"))


def test_complex_exp():
    a = formulate.from_root(("~a**b*23/(var||45)"))
    out = a.to_python()
    assert ast.unparse(ast.parse(out)) == ast.unparse(ast.parse("np.invert(a**b*23.0/var or 45.0)"))


def test_multiple_lor():
    a = formulate.from_root(("a||b||c"))
    out = a.to_python()
    assert ast.unparse(ast.parse(out)) == ast.unparse(ast.parse("a or b or c"))


def test_multiple_land():
    a = formulate.from_root(("a&&b&&c"))
    out = a.to_python()
    assert ast.unparse(ast.parse(out)) == ast.unparse(ast.parse("a and b and c"))


def test_multiple_bor():
    a = formulate.from_root(("a|b|c"))
    out = a.to_python()
    assert ast.unparse(ast.parse(out)) == ast.unparse(ast.parse("np.bitwise_or(np.bitwise_or(a,b),c)"))


def test_multiple_band():
    a = formulate.from_root(("a&b&c"))
    out = a.to_python()
    assert ast.unparse(ast.parse(out)) == ast.unparse(ast.parse("np.bitwise_and(np.bitwise_and(a,b),c)"))


def test_multiple_add():
    a = formulate.from_root(("a+b+c+d"))
    out = a.to_python()
    assert ast.unparse(ast.parse(out)) == ast.unparse(ast.parse("a+b+c+d"))


def test_multiple_sub():
    a = formulate.from_root(("a-b-c-d"))
    out = a.to_python()
    assert ast.unparse(ast.parse(out)) == ast.unparse(ast.parse("a-b-c-d"))


def test_multiple_mul():
    a = formulate.from_root(("a*b*c*d"))
    out = a.to_python()
    assert ast.unparse(ast.parse(out)) == ast.unparse(ast.parse("a*b*c*d"))


def test_multiple_div():
    a = formulate.from_root(("a/b/c/d"))
    out = a.to_python()
    assert ast.unparse(ast.parse(out)) == ast.unparse(ast.parse("a/b/c/d"))


def test_multiple_lor_four():
    a = formulate.from_root(("a||b||c||d"))
    out = a.to_python()
    assert ast.unparse(ast.parse(out)) == ast.unparse(ast.parse("a or b or c or d"))


def test_multiple_land_four():
    a = formulate.from_root(("a&&b&&c&&d"))
    out = a.to_python()
    assert ast.unparse(ast.parse(out)) == ast.unparse(ast.parse("a and b and c and d"))


def test_multiple_bor_four():
    a = formulate.from_root(("a|b|c|d"))
    out = a.to_python()
    assert ast.unparse(ast.parse(out)) == ast.unparse(ast.parse("np.bitwise_or(np.bitwise_or(np.bitwise_or(a,b),c),d)"))


def test_multiple_band_four():
    a = formulate.from_root(("a&b&c&d"))
    out = a.to_python()
    assert ast.unparse(ast.parse(out)) == ast.unparse(ast.parse("np.bitwise_and(np.bitwise_and(np.bitwise_and(a,b),c),d)"))


def test_multiple_pow():
    a = formulate.from_root(("a**b**c**d"))
    out = a.to_python()
    assert ast.unparse(ast.parse(out)) == ast.unparse(ast.parse("a**b**c**d"))


def test_multiple_bxor():
    a = formulate.from_root(("a^b^c^d"))
    out = a.to_python()
    assert ast.unparse(ast.parse(out)) == ast.unparse(ast.parse("a^b^c^d"))
