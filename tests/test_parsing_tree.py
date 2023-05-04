from __future__ import annotations

import formulate


def test_simple_add():
    a = formulate.ttreeformula.exp_to_ptree("a+2")
    aa = []
    tree = formulate._utils._ptree_to_string(a, aa)
    out = "".join(tree)
    assert out == "(a+2)"


def test_simple_sub():
    a = formulate.ttreeformula.exp_to_ptree("a-2")
    aa = []
    tree = formulate._utils._ptree_to_string(a, aa)
    out = "".join(tree)
    assert out == "(a-2)"


def test_simple_mul():
    a = formulate.ttreeformula.exp_to_ptree("f*2")
    aa = []
    tree = formulate._utils._ptree_to_string(a, aa)
    out = "".join(tree)
    assert out == "(f*2)"


def test_simple_div():
    a = formulate.ttreeformula.exp_to_ptree("a/2")
    aa = []
    tree = formulate._utils._ptree_to_string(a, aa)
    out = "".join(tree)
    assert out == "(a/2)"


def test_simple_lt():
    a = formulate.ttreeformula.exp_to_ptree("a<2")
    aa = []
    tree = formulate._utils._ptree_to_string(a, aa)
    out = "".join(tree)
    assert out == "(a<2)"


def test_simple_lte():
    a = formulate.ttreeformula.exp_to_ptree("a<=2")
    aa = []
    tree = formulate._utils._ptree_to_string(a, aa)
    out = "".join(tree)
    assert out == "(a<=2)"


def test_simple_gt():
    a = formulate.ttreeformula.exp_to_ptree("a>2")
    aa = []
    tree = formulate._utils._ptree_to_string(a, aa)
    out = "".join(tree)
    assert out == "(a>2)"


def test_simple_gte():
    a = formulate.ttreeformula.exp_to_ptree("a>=2")
    aa = []
    tree = formulate._utils._ptree_to_string(a, aa)
    out = "".join(tree)
    assert out == "(a>=2)"


def test_simple_eq():
    a = formulate.ttreeformula.exp_to_ptree("a==2")
    aa = []
    tree = formulate._utils._ptree_to_string(a, aa)
    out = "".join(tree)
    assert out == "(a==2)"


def test_simple_neq():
    a = formulate.ttreeformula.exp_to_ptree("a!=2")
    aa = []
    tree = formulate._utils._ptree_to_string(a, aa)
    out = "".join(tree)
    assert out == "(a!=2)"


def test_simple_bor():
    a = formulate.ttreeformula.exp_to_ptree("a|b")
    aa = []
    tree = formulate._utils._ptree_to_string(a, aa)
    out = "".join(tree)
    assert out == "(a|b)"


def test_simple_band():
    a = formulate.ttreeformula.exp_to_ptree("a&c")
    aa = []
    tree = formulate._utils._ptree_to_string(a, aa)
    out = "".join(tree)
    assert out == "(a&c)"


def test_simple_bxor():
    a = formulate.ttreeformula.exp_to_ptree("a^2")
    aa = []
    tree = formulate._utils._ptree_to_string(a, aa)
    out = "".join(tree)
    assert out == "(a^2)"


def test_simple_land():
    a = formulate.ttreeformula.exp_to_ptree("a&&2")
    aa = []
    tree = formulate._utils._ptree_to_string(a, aa)
    out = "".join(tree)
    assert out == "(a&&2)"


def test_simple_lor():
    a = formulate.ttreeformula.exp_to_ptree("a||2")
    aa = []
    tree = formulate._utils._ptree_to_string(a, aa)
    out = "".join(tree)
    assert out == "(a||2)"


def test_simple_pow():
    a = formulate.ttreeformula.exp_to_ptree("a**2")
    aa = []
    tree = formulate._utils._ptree_to_string(a, aa)
    out = "".join(tree)
    assert out == "(a**2)"


def test_simple_matrix():
    a = formulate.ttreeformula.exp_to_ptree("a[45][1]")
    aa = []
    tree = formulate._utils._ptree_to_string(a, aa)
    out = "".join(tree)
    assert out == "a[45][1]"


def test_simple_function():
    a = formulate.ttreeformula.exp_to_ptree("Math::sqrt(4)")
    aa = []
    tree = formulate._utils._ptree_to_string(a, aa)
    out = "".join(tree)
    assert out == "Math::sqrt(4)"


def test_simple_function2():
    a = formulate.ttreeformula.exp_to_ptree("Math::sqrt::three(4)")
    aa = []
    tree = formulate._utils._ptree_to_string(a, aa)
    out = "".join(tree)
    assert out == "Math::sqrt::three(4)"


def test_simple_function3():
    a = formulate.ttreeformula.exp_to_ptree("Math::sqrt::three::four(4)")
    aa = []
    tree = formulate._utils._ptree_to_string(a, aa)
    out = "".join(tree)
    assert out == "Math::sqrt::three::four(4)"


def test_simple_unary_pos():
    a = formulate.ttreeformula.exp_to_ptree("+5")
    aa = []
    tree = formulate._utils._ptree_to_string(a, aa)
    out = "".join(tree)
    assert out == "(+5)"


def test_simple_unary_neg():
    a = formulate.ttreeformula.exp_to_ptree("-5")
    aa = []
    tree = formulate._utils._ptree_to_string(a, aa)
    out = "".join(tree)
    assert out == "(-5)"


def test_simple_unary_binv():
    a = formulate.ttreeformula.exp_to_ptree("~bool")
    aa = []
    tree = formulate._utils._ptree_to_string(a, aa)
    out = "".join(tree)
    assert out == "(~bool)"


def test_simple_unary_linv():
    a = formulate.ttreeformula.exp_to_ptree("!bool")
    aa = []
    tree = formulate._utils._ptree_to_string(a, aa)
    out = "".join(tree)
    assert out == "(!bool)"


def test_simple_matrix_unary_pos():
    a = formulate.ttreeformula.exp_to_ptree("Math::sqrt::three::four(-4)")
    aa = []
    tree = formulate._utils._ptree_to_string(a, aa)
    out = "".join(tree)
    assert out == "Math::sqrt::three::four((-4))"


def test_unary_binary_pos():
    a = formulate.ttreeformula.exp_to_ptree("2 - -6")
    aa = []
    tree = formulate._utils._ptree_to_string(a, aa)
    out = "".join(tree)
    assert out == "(2-(-6))"


def test_complex_matrix():
    a = formulate.ttreeformula.exp_to_ptree("mat1[a**23][mat2[45 - -34]]")
    aa = []
    tree = formulate._utils._ptree_to_string(a, aa)
    out = "".join(tree)
    assert out == "mat1[(a**23)][mat2[(45-(-34))]]"


def test_complex_exp():
    a = formulate.ttreeformula.exp_to_ptree("~a**b*23/(var||45)")
    aa = []
    tree = formulate._utils._ptree_to_string(a, aa)
    out = "".join(tree)
    assert out == "(~((a**b)*(23/(var||45))))"
