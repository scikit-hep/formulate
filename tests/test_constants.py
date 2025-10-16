# Licensed under a 3-clause BSD style license, see LICENSE.
from __future__ import annotations

import numexpr
import numpy as np
import pytest

from formulate import from_numexpr, from_root

ROOT = pytest.importorskip("ROOT")


def root_eval(string, x=None, y=None, z=None, t=None):
    f = ROOT.TFormula("", string)
    f.Compile()
    if x is None:
        assert y is None and z is None and t is None
        return f.Eval(0)
    if y is None:
        assert z is None and t is None
        return f.Eval(x)
    if z is None:
        assert t is None
        return f.Eval(x, y)
    if t is None:
        return f.Eval(x, y, z)
    return f.Eval(x, y, z, t)


def numexpr_eval(string, **kwargs):
    return numexpr.evaluate(string, local_dict=kwargs)


def create_constant_test(input_string, input_backend="root", numexpr_raises=None):
    assert input_backend in ("root", "numexpr"), "Unrecognised backend specified"
    input_from_method = {
        "root": from_root,
        "numexpr": from_numexpr,
    }[input_backend]

    def test_constant():
        expression = input_from_method(input_string)

        root_result = expression.to_root()
        if input_backend == "root":
            if np.isnan(root_eval(input_string)):
                assert np.isnan(root_eval(root_result)), (
                    f"Evaluation was different: {root_eval(input_string)} != {root_eval(root_result)}"
                )
            else:
                assert np.isclose(root_eval(input_string), root_eval(root_result)), (
                    f"Evaluation was different: {root_eval(input_string)} != {root_eval(root_result)}"
                )

        if numexpr_raises:
            with pytest.raises(numexpr_raises):
                numexpr_result = expression.to_numexpr()
        else:
            numexpr_result = expression.to_numexpr()
            assert np.isclose(root_eval(root_result), numexpr_eval(numexpr_result)), (
                f"Evaluation was different: {root_eval(root_result)} != {numexpr_eval(numexpr_result)}"
            )

    return test_constant


# Test basic numexpr constants
test_numexpr_true = create_constant_test("True", input_backend="numexpr")
test_numexpr_false = create_constant_test("False", input_backend="numexpr")

# Test basic ROOT constants
test_true = create_constant_test("true")
test_false = create_constant_test("false")
test_infinity = create_constant_test("TMath::Infinity()", numexpr_raises=ValueError)
test_nan = create_constant_test("TMath::QuietNaN()", numexpr_raises=ValueError)

test_sqrt2_1 = create_constant_test("sqrt2")
test_sqrt2_2 = create_constant_test("TMath::Sqrt2()")
test_e_1 = create_constant_test("exp1", input_backend="numexpr")
test_e_2 = create_constant_test("TMath::E()")
test_pi_1 = create_constant_test("pi", input_backend="numexpr")
test_pi_2 = create_constant_test("TMath::Pi()")
test_pi_over_2 = create_constant_test("TMath::PiOver2()")
test_pi_over_4 = create_constant_test("TMath::PiOver4()")
test_two_pi = create_constant_test("TMath::TwoPi()")
test_inv_pi = create_constant_test("TMath::InvPi()")
test_ln10_1 = create_constant_test("ln10", input_backend="numexpr")
test_ln10_2 = create_constant_test("TMath::Ln10()")
test_log10e = create_constant_test("TMath::LogE()")
test_deg2rad = create_constant_test("TMath::DegToRad()")
test_rad2deg = create_constant_test("TMath::RadToDeg()")

test_na = create_constant_test("TMath::Na()")
test_k = create_constant_test("TMath::K()")
test_c = create_constant_test("TMath::C()")
test_qe = create_constant_test("TMath::Qe()")
test_h = create_constant_test("TMath::H()")
test_hbar = create_constant_test("TMath::Hbar()")
