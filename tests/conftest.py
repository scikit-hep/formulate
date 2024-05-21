import pytest


def root_eval(string, x=None, y=None, z=None, t=None):
    import ROOT

    f = ROOT.TFormula("", string)
    f.Compile()
    if x is None:
        assert y is None and z is None and t is None
        return f.Eval(0)
    elif y is None:
        assert z is None and t is None
        return f.Eval(x)
    elif z is None:
        assert t is None
        return f.Eval(x, y)
    elif t is None:
        return f.Eval(x, y, z)
    else:
        return f.Eval(x, y, z, t)


def numexpr_eval(string, **kwargs):
    import numexpr

    return numexpr.evaluate(string, local_dict=kwargs)


@pytest.helpers.register
def create_formula_test(
    input_string, input_backend="root", root_raises=None, numexpr_raises=None
):
    assert input_backend in ("root", "numexpr"), "Unrecognised backend specified"
    from formulate import from_root, from_numexpr

    input_from_method = {
        "root": from_root,
        "numexpr": from_numexpr,
    }[input_backend]

    def test_constant():
        from formulate import to_root, to_numexpr

        expression = input_from_method(input_string)

        if input_backend == "root":
            from formulate import to_root

            root_result = to_root(expression)
            assert input_string, root_result

            if numexpr_raises:
                with pytest.raises(numexpr_raises):
                    from formulate import to_numexpr

                    to_numexpr(expression)
            else:
                numexpr_result = to_numexpr(expression)
                assert root_eval(root_result) == pytest.approx(
                    numexpr_eval(numexpr_result)
                )
        else:
            numexpr_result = to_numexpr(expression)
            assert input_string, numexpr_result

            if root_raises:
                with pytest.raises(root_raises):
                    to_root(expression)
            else:
                root_result = to_root(expression)
                assert numexpr_eval(numexpr_result) == pytest.approx(
                    root_eval(root_result)
                )

    return test_constant
