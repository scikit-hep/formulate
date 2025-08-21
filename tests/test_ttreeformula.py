from __future__ import annotations

import ast

import formulate


def test_simple_add():
    a = formulate.from_root("a+2.0")
    out = a.to_python()
    assert ast.unparse(ast.parse(out)) == ast.unparse(ast.parse("a+2.0"))


def test_simple_sub():
    a = formulate.from_root("a-2.0")
    out = a.to_python()
    assert ast.unparse(ast.parse(out)) == ast.unparse(ast.parse("a-2.0"))


def test_simple_mul():
    a = formulate.from_root("f*2.0")
    out = a.to_python()
    assert ast.unparse(ast.parse(out)) == ast.unparse(ast.parse("f*2.0"))


def test_simple_div():
    a = formulate.from_root("a/2.0")
    out = a.to_python()
    assert ast.unparse(ast.parse(out)) == ast.unparse(ast.parse("a/2.0"))


def test_simple_lt():
    a = formulate.from_root("a<2.0")
    out = a.to_python()
    assert ast.unparse(ast.parse(out)) == ast.unparse(ast.parse("a<2.0"))


def test_simple_lte():
    a = formulate.from_root("a<=2.0")
    out = a.to_python()
    assert ast.unparse(ast.parse(out)) == ast.unparse(ast.parse("a<=2.0"))


def test_simple_gt():
    a = formulate.from_root("a>2.0")
    out = a.to_python()
    assert ast.unparse(ast.parse(out)) == ast.unparse(ast.parse("a>2.0"))


def test_simple_gte():
    a = formulate.from_root("a>=2.0")
    out = a.to_python()
    assert ast.unparse(ast.parse(out)) == ast.unparse(ast.parse("a>=2.0"))


def test_simple_eq():
    a = formulate.from_root("a==2.0")
    out = a.to_python()
    assert ast.unparse(ast.parse(out)) == ast.unparse(ast.parse("a==2.0"))


def test_simple_neq():
    a = formulate.from_root("a!=2.0")
    out = a.to_python()
    assert ast.unparse(ast.parse(out)) == ast.unparse(ast.parse("a!=2.0"))


def test_simple_and():
    a = formulate.from_root("a&&2.0")
    out = a.to_python()
    assert ast.unparse(ast.parse(out)) == ast.unparse(ast.parse("a & 2.0"))


def test_simple_lor():
    a = formulate.from_root("a||2.0")
    out = a.to_python()
    assert ast.unparse(ast.parse(out)) == ast.unparse(ast.parse("a | 2.0"))


def test_simple_pow():
    a = formulate.from_root("a**2.0")
    out = a.to_python()
    assert ast.unparse(ast.parse(out)) == ast.unparse(ast.parse("a**2.0"))


def test_simple_pow2():
    a = formulate.from_root("a^2.0")
    out = a.to_python()
    assert ast.unparse(ast.parse(out)) == ast.unparse(ast.parse("a**2.0"))


def test_simple_matrix():
    a = formulate.from_root("a[45][1]")
    out = a.to_python()
    assert ast.unparse(ast.parse(out)) == ast.unparse(ast.parse("a[45, 1]"))


def test_simple_function():
    a = formulate.from_root("Math::sqrt(4)")
    out = a.to_python()
    assert ast.unparse(ast.parse(out)) == ast.unparse(ast.parse("sqrt(4)"))


def test_simple_unary_pos():
    a = formulate.from_root("+5.0")
    out = a.to_python()
    assert ast.unparse(ast.parse(out)) == ast.unparse(ast.parse("+5.0"))


def test_simple_unary_neg():
    a = formulate.from_root("-5.0")
    out = a.to_python()
    assert ast.unparse(ast.parse(out)) == ast.unparse(ast.parse("-5.0"))


def test_simple_unary_inv():
    a = formulate.from_root("!bool")
    out = a.to_python()
    assert ast.unparse(ast.parse(out)) == ast.unparse(ast.parse("(~bool)"))


def test_unary_binary_pos():
    a = formulate.from_root("2.0 - -6")
    out = a.to_python()
    assert ast.unparse(ast.parse(out)) == ast.unparse(ast.parse("2.0--6"))


def test_complex_matrix():
    a = formulate.from_root("mat1[a**23][mat2[45 - -34]]")
    out = a.to_python()
    assert ast.unparse(ast.parse(out)) == ast.unparse(
        ast.parse("mat1[(a ** 23), mat2[(45 - -(34))]]")
    )


def test_complex_exp():
    a = formulate.from_root("!a**b*23/(var||45)")
    out = a.to_python()
    assert ast.unparse(ast.parse(out)) == ast.unparse(
        ast.parse("~(a**b)*23/(var | 45)")
    )


def test_multiple_or():
    a = formulate.from_root("a||b||c")
    out = a.to_python()
    assert ast.unparse(ast.parse(out)) == ast.unparse(ast.parse("a | b | c"))


def test_multiple_and():
    a = formulate.from_root("a&&b&&c")
    out = a.to_python()
    assert ast.unparse(ast.parse(out)) == ast.unparse(ast.parse("a & b & c"))


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


def test_multiple_or_four():
    a = formulate.from_root("a||b||c||d")
    out = a.to_python()
    assert ast.unparse(ast.parse(out)) == ast.unparse(ast.parse("a | b | c | d"))


def test_multiple_and_four():
    a = formulate.from_root("a&&b&&c&&d")
    out = a.to_python()
    assert ast.unparse(ast.parse(out)) == ast.unparse(ast.parse("a & b & c & d"))


def test_multiple_pow():
    a = formulate.from_root("a**b**c**d")
    out = a.to_python()
    assert ast.unparse(ast.parse(out)) == ast.unparse(ast.parse("a**b**c**d"))


def test_multiple_pow2():
    a = formulate.from_root("a^b^c^d")
    out = a.to_python()
    assert ast.unparse(ast.parse(out)) == ast.unparse(ast.parse("a**b**c**d"))
