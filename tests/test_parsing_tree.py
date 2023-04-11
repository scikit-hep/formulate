import formulate

def test_simple_add():
    a = formulate.ttreeformula.from_ROOT("a+2")
    aa=[]
    tree = formulate._utils._ptree_to_string(a,aa)
    out = "".join(tree)
    assert "(a+2)" == out

def test_simple_sub():
    a = formulate.ttreeformula.from_ROOT("a-2")
    aa=[]
    tree = formulate._utils._ptree_to_string(a,aa)
    out = "".join(tree)
    assert "(a-2)" == out