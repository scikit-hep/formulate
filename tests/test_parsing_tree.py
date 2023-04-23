import formulate

def test_simple_add():
    a = formulate.ttreeformula.exp_to_ptree("a+2")
    aa=[]
    tree = formulate._utils._ptree_to_string(a,aa)
    out = "".join(tree)
    assert "(a+2)" == out

def test_simple_sub():
    a = formulate.ttreeformula.exp_to_ptree("a-2")
    aa=[]
    tree = formulate._utils._ptree_to_string(a,aa)
    out = "".join(tree)
    assert "(a-2)" == out

def test_simple_mul():
    a = formulate.ttreeformula.exp_to_ptree("f*2")
    aa=[]
    tree = formulate._utils._ptree_to_string(a,aa)
    out = "".join(tree)
    assert "(f*2)" == out

def test_simple_div():
    a = formulate.ttreeformula.exp_to_ptree("a/2")
    aa=[]
    tree = formulate._utils._ptree_to_string(a,aa)
    out = "".join(tree)
    assert "(a/2)" == out

def test_simple_lt():
    a = formulate.ttreeformula.exp_to_ptree("a<2")
    aa=[]
    tree = formulate._utils._ptree_to_string(a,aa)
    out = "".join(tree)
    assert "(a<2)" == out
def test_simple_lte():
    a = formulate.ttreeformula.exp_to_ptree("a<=2")
    aa=[]
    tree = formulate._utils._ptree_to_string(a,aa)
    out = "".join(tree)
    assert "(a<=2)" == out
def test_simple_gt():
    a = formulate.ttreeformula.exp_to_ptree("a>2")
    aa=[]
    tree = formulate._utils._ptree_to_string(a,aa)
    out = "".join(tree)
    assert "(a>2)" == out
def test_simple_gte():
    a = formulate.ttreeformula.exp_to_ptree("a>=2")
    aa=[]
    tree = formulate._utils._ptree_to_string(a,aa)
    out = "".join(tree)
    assert "(a>=2)" == out
def test_simple_eq():
    a = formulate.ttreeformula.exp_to_ptree("a==2")
    aa=[]
    tree = formulate._utils._ptree_to_string(a,aa)
    out = "".join(tree)
    assert "(a==2)" == out
def test_simple_neq():
    a = formulate.ttreeformula.exp_to_ptree("a!=2")
    aa=[]
    tree = formulate._utils._ptree_to_string(a,aa)
    out = "".join(tree)
    assert "(a!=2)" == out
def test_simple_bor():
    a = formulate.ttreeformula.exp_to_ptree("a|b")
    aa=[]
    tree = formulate._utils._ptree_to_string(a,aa)
    out = "".join(tree)
    assert "(a|b)" == out
def test_simple_band():
    a = formulate.ttreeformula.exp_to_ptree("a&c")
    aa=[]
    tree = formulate._utils._ptree_to_string(a,aa)
    out = "".join(tree)
    assert "(a&c)" == out
def test_simple_bxor():
    a = formulate.ttreeformula.exp_to_ptree("a^2")
    aa=[]
    tree = formulate._utils._ptree_to_string(a,aa)
    out = "".join(tree)
    assert "(a^2)" == out
def test_simple_land():
    a = formulate.ttreeformula.exp_to_ptree("a&&2")
    aa=[]
    tree = formulate._utils._ptree_to_string(a,aa)
    out = "".join(tree)
    assert "(a&&2)" == out
def test_simple_lor():
    a = formulate.ttreeformula.exp_to_ptree("a||2")
    aa=[]
    tree = formulate._utils._ptree_to_string(a,aa)
    out = "".join(tree)
    assert "(a||2)" == out
def test_simple_matrix(): #this test sometimes fails and sometimes it passes
    a = formulate.ttreeformula.exp_to_ptree("a[45][1]")
    aa=[]
    tree = formulate._utils._ptree_to_string(a,aa)
    out = "".join(tree)
    assert "a[45][1]" == out