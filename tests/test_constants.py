# Licensed under a 3-clause BSD style license, see LICENSE.
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import pytest
import numpy as np

from formulate import from_numexpr, to_numexpr
from formulate import from_root, to_root

numexpr = pytest.importorskip("numexpr")
ROOT = pytest.importorskip("ROOT")


def root_eval(string, x=None, y=None, z=None, t=None):
    f = ROOT.TFormula('', string)
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
    return numexpr.evaluate(string, local_dict=kwargs)


def create_constant_test(input_string, input_backend='root', numexpr_raises=None):
    assert input_backend in ('root', 'numexpr'), 'Unrecognised backend specified'
    input_from_method = {
        'root': from_root,
        'numexpr': from_numexpr,
    }[input_backend]

    def test_constant():
        expression = input_from_method(input_string)

        root_result = to_root(expression)
        assert pytest.approx(root_eval(input_string), root_eval(root_result))

        if numexpr_raises:
            with pytest.raises(numexpr_raises):
                numexpr_result = to_numexpr(expression)
        else:
            numexpr_result = to_numexpr(expression)
            assert pytest.approx(root_eval(root_result), numexpr_eval(numexpr_result))

    return test_constant


# Test basic numexpr constants
test_numexpr_true = create_constant_test('True', input_backend='numexpr')
test_numexpr_false = create_constant_test('False', input_backend='numexpr')

# Test basic ROOT constants
test_true = create_constant_test('true')
test_false = create_constant_test('false')
test_infinity = create_constant_test('TMath::Infinity()', numexpr_raises=NotImplementedError)
test_nan = create_constant_test('TMath::QuietNaN()', numexpr_raises=NotImplementedError)

test_sqrt2_1 = create_constant_test('sqrt2')
test_sqrt2_2 = create_constant_test('TMath::Sqrt2()')
test_e_1 = create_constant_test('e')
test_e_2 = create_constant_test('TMath::E()')
test_pi_1 = create_constant_test('pi')
test_pi_2 = create_constant_test('TMath::Pi()')
test_pi_over_2 = create_constant_test('TMath::PiOver2()')
test_pi_over_4 = create_constant_test('TMath::PiOver4()')
test_two_pi = create_constant_test('TMath::TwoPi()')
test_inv_pi = create_constant_test('TMath::InvPi()')
test_ln10_1 = create_constant_test('ln10')
test_ln10_2 = create_constant_test('TMath::Ln10()')
test_log10e = create_constant_test('TMath::LogE()')
test_deg2rad = create_constant_test('TMath::DegToRad()')
test_rad2deg = create_constant_test('TMath::RadToDeg()')

test_na = create_constant_test('TMath::Na()')
test_nauncertainty = create_constant_test('TMath::NaUncertainty()', numexpr_raises=NotImplementedError)
test_k = create_constant_test('TMath::K()')
test_kcgs = create_constant_test('TMath::Kcgs()')
test_kuncertainty = create_constant_test('TMath::KUncertainty()', numexpr_raises=NotImplementedError)
test_c = create_constant_test('TMath::C()')
test_ccgs = create_constant_test('TMath::Ccgs()')
test_cuncertainty = create_constant_test('TMath::CUncertainty()')
test_rgair = create_constant_test('TMath::Rgair()')
test_qe = create_constant_test('TMath::Qe()')
test_qeuncertainty = create_constant_test('TMath::QeUncertainty()', numexpr_raises=NotImplementedError)
test_eulergamma = create_constant_test('TMath::EulerGamma()')
test_g = create_constant_test('TMath::G()')
test_gcgs = create_constant_test('TMath::Gcgs()')
test_guncertainty = create_constant_test('TMath::GUncertainty()', numexpr_raises=NotImplementedError)
test_ghbarc = create_constant_test('TMath::GhbarC()')
test_ghbarcuncertainty = create_constant_test('TMath::GhbarCUncertainty()', numexpr_raises=NotImplementedError)
test_gn = create_constant_test('TMath::Gn()')
test_gnuncertainty = create_constant_test('TMath::GnUncertainty()', numexpr_raises=NotImplementedError)
test_h = create_constant_test('TMath::H()')
test_hcgs = create_constant_test('TMath::Hcgs()')
test_huncertainty = create_constant_test('TMath::HUncertainty()', numexpr_raises=NotImplementedError)
test_hbar = create_constant_test('TMath::Hbar()')
test_hbarcgs = create_constant_test('TMath::Hbarcgs()')
test_hbaruncertainty = create_constant_test('TMath::HbarUncertainty()', numexpr_raises=NotImplementedError)
test_hc = create_constant_test('TMath::HC()')
test_hccgs = create_constant_test('TMath::HCcgs()')
test_mwair = create_constant_test('TMath::MWair()')
test_sigma = create_constant_test('TMath::Sigma()')
test_sigmauncertainty = create_constant_test('TMath::SigmaUncertainty()', numexpr_raises=NotImplementedError)
test_r = create_constant_test('TMath::R()')
test_runcertainty = create_constant_test('TMath::RUncertainty()', numexpr_raises=NotImplementedError)
