from __future__ import annotations

import formulate

from formulate.toast import toast

import ast


def test_simple_add():
    a = toast(formulate.ttreeformula.exp_to_ptree("a+2.0"))
    out = a.to_python()
    assert ast.unparse(ast.parse(out)) == ast.unparse(ast.parse("(a+2.0)"))


def test_simple_sub():
    a = toast(formulate.ttreeformula.exp_to_ptree("a-2.0"))
    out = a.to_python()
    assert ast.unparse(ast.parse(out)) == ast.unparse(ast.parse("(a-2.0)"))


def test_simple_mul():
    a = toast(formulate.ttreeformula.exp_to_ptree("f*2.0"))
    out = a.to_python()
    assert ast.unparse(ast.parse(out)) == ast.unparse(ast.parse("(f*2.0)"))


def test_simple_div():
    a = toast(formulate.ttreeformula.exp_to_ptree("a/2.0"))
    out = a.to_python()
    assert ast.unparse(ast.parse(out)) == ast.unparse(ast.parse("(a/2.0)"))


def test_simple_lt():
    a = toast(formulate.ttreeformula.exp_to_ptree("a<2.0"))
    out = a.to_python()
    assert ast.unparse(ast.parse(out)) == ast.unparse(ast.parse("(a<2.0)"))


def test_simple_lte():
    a = toast(formulate.ttreeformula.exp_to_ptree("a<=2.0"))
    out = a.to_python()
    assert ast.unparse(ast.parse(out)) == ast.unparse(ast.parse("(a<=2.0)"))


def test_simple_gt():
    a = toast(formulate.ttreeformula.exp_to_ptree("a>2.0"))
    out = a.to_python()
    assert ast.unparse(ast.parse(out)) == ast.unparse(ast.parse("(a>2.0)"))


def test_simple_gte():
    a = toast(formulate.ttreeformula.exp_to_ptree("a>=2.0"))
    out = a.to_python()
    assert ast.unparse(ast.parse(out)) == ast.unparse(ast.parse("(a>=2.0)"))


def test_simple_eq():
    a = toast(formulate.ttreeformula.exp_to_ptree("a==2.0"))
    out = a.to_python()
    assert ast.unparse(ast.parse(out)) == ast.unparse(ast.parse("(a==2.0)"))


def test_simple_neq():
    a = toast(formulate.ttreeformula.exp_to_ptree("a!=2.0"))
    out = a.to_python()
    assert ast.unparse(ast.parse(out)) == ast.unparse(ast.parse("(a!=2.0)"))


def test_simple_bor():
    a = toast(formulate.ttreeformula.exp_to_ptree("a|b"))
    out = a.to_python()
    assert ast.unparse(ast.parse(out)) == ast.unparse(ast.parse("np.bitwise_or(a,b)"))


def test_simple_band():
    a = toast(formulate.ttreeformula.exp_to_ptree("a&c"))
    out = a.to_python()
    assert ast.unparse(ast.parse(out)) == ast.unparse(ast.parse("np.bitwise_and(a,c)"))


def test_simple_bxor():
    a = toast(formulate.ttreeformula.exp_to_ptree("a^2.0"))
    out = a.to_python()
    assert ast.unparse(ast.parse(out)) == ast.unparse(ast.parse("(a^2.0)"))


def test_simple_land():
    a = toast(formulate.ttreeformula.exp_to_ptree("a&&2.0"))
    out = a.to_python()
    assert ast.unparse(ast.parse(out)) == ast.unparse(ast.parse("(a and 2.0)"))


def test_simple_lor():
    a = toast(formulate.ttreeformula.exp_to_ptree("a||2.0"))
    out = a.to_python()
    assert ast.unparse(ast.parse(out)) == ast.unparse(ast.parse("(a or 2.0)"))


def test_simple_pow():
    a = toast(formulate.ttreeformula.exp_to_ptree("a**2.0"))
    out = a.to_python()
    assert ast.unparse(ast.parse(out)) == ast.unparse(ast.parse("(a**2.0)"))


def test_simple_matrix():
    a = toast(formulate.ttreeformula.exp_to_ptree("a[45][1]"))
    out = a.to_python()
    assert ast.unparse(ast.parse(out)) == ast.unparse(ast.parse("a[:, 45.0, 1.0]"))


def test_simple_function():
    a = toast(formulate.ttreeformula.exp_to_ptree("Math::sqrt(4)"))
    out = a.to_python()
    assert ast.unparse(ast.parse(out)) == ast.unparse(ast.parse("np.sqrt(4.0)"))


def test_simple_unary_pos():
    a = toast(formulate.ttreeformula.exp_to_ptree("+5.0"))
    out = a.to_python()
    assert ast.unparse(ast.parse(out)) == ast.unparse(ast.parse("(+5.0)"))


def test_simple_unary_neg():
    a = toast(formulate.ttreeformula.exp_to_ptree("-5.0"))
    out = a.to_python()
    assert ast.unparse(ast.parse(out)) == ast.unparse(ast.parse("(-5.0)"))


def test_simple_unary_binv():
    a = toast(formulate.ttreeformula.exp_to_ptree("~bool"))
    out = a.to_python()
    assert ast.unparse(ast.parse(out)) == ast.unparse(ast.parse("np.invert(bool)"))


def test_simple_unary_linv():
    a = toast(formulate.ttreeformula.exp_to_ptree("!bool"))
    out = a.to_python()
    assert ast.unparse(ast.parse(out)) == ast.unparse(ast.parse("np.logical_not(bool)"))


def test_unary_binary_pos():
    a = toast(formulate.ttreeformula.exp_to_ptree("2.0 - -6"))
    out = a.to_python()
    assert ast.unparse(ast.parse(out)) == ast.unparse(ast.parse("(2.0-(-6.0))"))


def test_complex_matrix():
    a = toast(formulate.ttreeformula.exp_to_ptree("mat1[a**23][mat2[45 - -34]]"))
    out = a.to_python()
    assert ast.unparse(ast.parse(out)) == ast.unparse(ast.parse("(mat1[:,(a**23.0),(mat2[:,(45.0-(-34.0))])])"))


def test_complex_exp():
    a = toast(formulate.ttreeformula.exp_to_ptree("~a**b*23/(var||45)"))
    out = a.to_python()
    assert ast.unparse(ast.parse(out)) == ast.unparse(ast.parse("np.invert(((a**b)*(23.0/(var or 45.0))))"))
