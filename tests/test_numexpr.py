from __future__ import annotations

import formulate

from formulate.toast import toast

import ast


def test_simple_add():
    a = toast(formulate.numexpr.exp_to_ptree("a+2.0"), nxp = True)
    out = a.to_python()
    assert ast.unparse(ast.parse(out)) == ast.unparse(ast.parse("(a+2.0)"))


def test_simple_sub():
    a = toast(formulate.numexpr.exp_to_ptree("a-2.0"), nxp = True)
    out = a.to_python()
    assert ast.unparse(ast.parse(out)) == ast.unparse(ast.parse("(a-2.0)"))


def test_simple_mul():
    a = toast(formulate.numexpr.exp_to_ptree("f*2.0"), nxp = True)
    out = a.to_python()
    assert ast.unparse(ast.parse(out)) == ast.unparse(ast.parse("(f*2.0)"))


def test_simple_div():
    a = toast(formulate.numexpr.exp_to_ptree("a/2.0"), nxp = True)
    out = a.to_python()
    assert ast.unparse(ast.parse(out)) == ast.unparse(ast.parse("(a/2.0)"))


def test_simple_lt():
    a = toast(formulate.numexpr.exp_to_ptree("a<2.0"), nxp = True)
    out = a.to_python()
    assert ast.unparse(ast.parse(out)) == ast.unparse(ast.parse("(a<2.0)"))


def test_simple_lte():
    a = toast(formulate.numexpr.exp_to_ptree("a<=2.0"), nxp = True)
    out = a.to_python()
    assert ast.unparse(ast.parse(out)) == ast.unparse(ast.parse("(a<=2.0)"))


def test_simple_gt():
    a = toast(formulate.numexpr.exp_to_ptree("a>2.0"), nxp = True)
    out = a.to_python()
    assert ast.unparse(ast.parse(out)) == ast.unparse(ast.parse("(a>2.0)"))


def test_simple_gte():
    a = toast(formulate.numexpr.exp_to_ptree("a>=2.0"), nxp = True)
    out = a.to_python()
    assert ast.unparse(ast.parse(out)) == ast.unparse(ast.parse("(a>=2.0)"))


def test_simple_eq():
    a = toast(formulate.numexpr.exp_to_ptree("a==2.0"), nxp = True)
    out = a.to_python()
    assert ast.unparse(ast.parse(out)) == ast.unparse(ast.parse("(a==2.0)"))


def test_simple_neq():
    a = toast(formulate.numexpr.exp_to_ptree("a!=2.0"), nxp = True)
    out = a.to_python()
    assert ast.unparse(ast.parse(out)) == ast.unparse(ast.parse("(a!=2.0)"))


def test_simple_bor():
    a = toast(formulate.numexpr.exp_to_ptree("a|b"), nxp = True)
    out = a.to_python()
    assert ast.unparse(ast.parse(out)) == ast.unparse(ast.parse("np.bitwise_or(a,b)"))


def test_simple_band():
    a = toast(formulate.numexpr.exp_to_ptree("a&c"), nxp = True)
    out = a.to_python()
    assert ast.unparse(ast.parse(out)) == ast.unparse(ast.parse("np.bitwise_and(a,c)"))


def test_simple_bxor():
    a = toast(formulate.numexpr.exp_to_ptree("a^2.0"), nxp = True)
    out = a.to_python()
    assert ast.unparse(ast.parse(out)) == ast.unparse(ast.parse("(a^2.0)"))

def test_simple_pow():
    a = toast(formulate.numexpr.exp_to_ptree("a**2.0"), nxp = True)
    out = a.to_python()
    assert ast.unparse(ast.parse(out)) == ast.unparse(ast.parse("(a**2.0)"))


def test_simple_function():
    a = toast(formulate.numexpr.exp_to_ptree("sqrt(4)"), nxp = True)
    out = a.to_python()
    assert ast.unparse(ast.parse(out)) == ast.unparse(ast.parse("np.sqrt(4.0)"))


def test_simple_unary_pos():
    a = toast(formulate.numexpr.exp_to_ptree("+5.0"), nxp = True)
    out = a.to_python()
    assert ast.unparse(ast.parse(out)) == ast.unparse(ast.parse("(+5.0)"))


def test_simple_unary_neg():
    a = toast(formulate.numexpr.exp_to_ptree("-5.0"), nxp = True)
    out = a.to_python()
    assert ast.unparse(ast.parse(out)) == ast.unparse(ast.parse("(-5.0)"))


def test_simple_unary_binv():
    a = toast(formulate.numexpr.exp_to_ptree("~bool"), nxp = True)
    out = a.to_python()
    assert ast.unparse(ast.parse(out)) == ast.unparse(ast.parse("np.invert(bool)"))



def test_unary_binary_pos():
    a = toast(formulate.numexpr.exp_to_ptree("2.0 - -6"), nxp = True)
    out = a.to_python()
    assert ast.unparse(ast.parse(out)) == ast.unparse(ast.parse("(2.0-(-6.0))"))


def test_complex_exp():
    a = toast(formulate.numexpr.exp_to_ptree("~a**b*23/(var|45)"), nxp = True)
    out = a.to_python()
    assert ast.unparse(ast.parse(out)) == ast.unparse(ast.parse("np.invert(((a**b)*(23.0/np.bitwise_or(var,45.0))))"))
