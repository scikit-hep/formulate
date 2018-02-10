from selections import Expression
from selections import from_numexpr
from selections.identifiers import IDs


def assert_equal_expressions(lhs, rhs):
    assert isinstance(lhs, Expression)
    assert isinstance(rhs, Expression)
    assert lhs._id == rhs._id
    assert len(lhs._args) == len(rhs._args)
    for a, b in zip(lhs._args, rhs._args):
        assert isinstance(b, a.__class__)
        if isinstance(a, Expression):
            assert_equal_expressions(a, b)
        else:
            assert a == b
    # TODO Check the equivalent method always gets it right
    # assert lhs.equivilent(rhs)
    # assert rhs.equivilent(lhs)


# def test_empty():
#     from_numexpr('')

# TODO What should this do? Just a number?
# assert_equal_expressions(from_numexpr('-1'), Expression(ID, 1, 1))

def test_basic_parsing():
    assert_equal_expressions(from_numexpr('1 + 1'), Expression(IDs.ADD, 1, 1))
    assert_equal_expressions(from_numexpr('sqrt(1)'), Expression(IDs.SQRT, 1))
    assert_equal_expressions(from_numexpr('arctan2(1, 1)'), Expression(IDs.ATAN2, 1, 1))


def test_nested_parsing():
    assert_equal_expressions(
        from_numexpr('-(1 + 1)'),
        Expression(IDs.MINUS, Expression(IDs.ADD, 1, 1))
    )
    assert_equal_expressions(
        from_numexpr('+sqrt(3)'),
        Expression(IDs.PLUS, Expression(IDs.SQRT, 3))
    )
    assert_equal_expressions(
        from_numexpr('-(4) * (3)'),
        Expression(IDs.MUL, Expression(IDs.MINUS, 4), 3)
    )
    assert_equal_expressions(
        from_numexpr('-(1 + 1) * +(5 + 4)'),
        Expression(IDs.MUL,
                   Expression(IDs.MINUS, Expression(IDs.ADD, 1, 1)),
                   Expression(IDs.PLUS, Expression(IDs.ADD, 5, 4)))
    )
    assert_equal_expressions(
        from_numexpr('-sqrt(3 + 4) / arctan2(5 + sqrt(4), 1)'),
        Expression(IDs.DIV,
                   Expression(IDs.MINUS, Expression(IDs.SQRT, Expression(IDs.ADD, 3, 4))),
                   Expression(IDs.ATAN2, Expression(IDs.ADD, 5, Expression(IDs.SQRT, 4)), 1))
    )
