# Licensed under a 3-clause BSD style license, see LICENSE.
import pytest

# Test basic numexpr constants
test_numexpr_true = pytest.helpers.create_formula_test("True", input_backend="numexpr")
test_numexpr_false = pytest.helpers.create_formula_test(
    "False", input_backend="numexpr"
)

# Test basic ROOT constants
test_true = pytest.helpers.create_formula_test("true")
test_false = pytest.helpers.create_formula_test("false")
test_infinity = pytest.helpers.create_formula_test(
    "TMath::Infinity()", numexpr_raises=NotImplementedError
)
test_nan = pytest.helpers.create_formula_test(
    "TMath::QuietNaN()", numexpr_raises=NotImplementedError
)

test_sqrt2_1 = pytest.helpers.create_formula_test("sqrt2")
test_sqrt2_2 = pytest.helpers.create_formula_test("TMath::Sqrt2()")
test_e_1 = pytest.helpers.create_formula_test("e")
test_e_2 = pytest.helpers.create_formula_test("TMath::E()")
test_pi_1 = pytest.helpers.create_formula_test("pi")
test_pi_2 = pytest.helpers.create_formula_test("TMath::Pi()")
test_pi_over_2 = pytest.helpers.create_formula_test("TMath::PiOver2()")
test_pi_over_4 = pytest.helpers.create_formula_test("TMath::PiOver4()")
test_two_pi = pytest.helpers.create_formula_test("TMath::TwoPi()")
test_inv_pi = pytest.helpers.create_formula_test("TMath::InvPi()")
test_ln10_1 = pytest.helpers.create_formula_test("ln10")
test_ln10_2 = pytest.helpers.create_formula_test("TMath::Ln10()")
test_log10e = pytest.helpers.create_formula_test("TMath::LogE()")
test_deg2rad = pytest.helpers.create_formula_test("TMath::DegToRad()")
test_rad2deg = pytest.helpers.create_formula_test("TMath::RadToDeg()")

test_na = pytest.helpers.create_formula_test("TMath::Na()")
test_nauncertainty = pytest.helpers.create_formula_test(
    "TMath::NaUncertainty()", numexpr_raises=NotImplementedError
)
test_k = pytest.helpers.create_formula_test("TMath::K()")
test_kcgs = pytest.helpers.create_formula_test("TMath::Kcgs()")
test_kuncertainty = pytest.helpers.create_formula_test(
    "TMath::KUncertainty()", numexpr_raises=NotImplementedError
)
test_c = pytest.helpers.create_formula_test("TMath::C()")
test_ccgs = pytest.helpers.create_formula_test("TMath::Ccgs()")
test_cuncertainty = pytest.helpers.create_formula_test("TMath::CUncertainty()")
test_rgair = pytest.helpers.create_formula_test("TMath::Rgair()")
test_qe = pytest.helpers.create_formula_test("TMath::Qe()")
test_qeuncertainty = pytest.helpers.create_formula_test(
    "TMath::QeUncertainty()", numexpr_raises=NotImplementedError
)
test_eulergamma = pytest.helpers.create_formula_test("TMath::EulerGamma()")
test_g = pytest.helpers.create_formula_test("TMath::G()")
test_gcgs = pytest.helpers.create_formula_test("TMath::Gcgs()")
test_guncertainty = pytest.helpers.create_formula_test(
    "TMath::GUncertainty()", numexpr_raises=NotImplementedError
)
test_ghbarc = pytest.helpers.create_formula_test("TMath::GhbarC()")
test_ghbarcuncertainty = pytest.helpers.create_formula_test(
    "TMath::GhbarCUncertainty()", numexpr_raises=NotImplementedError
)
test_gn = pytest.helpers.create_formula_test("TMath::Gn()")
test_gnuncertainty = pytest.helpers.create_formula_test(
    "TMath::GnUncertainty()", numexpr_raises=NotImplementedError
)
test_h = pytest.helpers.create_formula_test("TMath::H()")
test_hcgs = pytest.helpers.create_formula_test("TMath::Hcgs()")
test_huncertainty = pytest.helpers.create_formula_test(
    "TMath::HUncertainty()", numexpr_raises=NotImplementedError
)
test_hbar = pytest.helpers.create_formula_test("TMath::Hbar()")
test_hbarcgs = pytest.helpers.create_formula_test("TMath::Hbarcgs()")
test_hbaruncertainty = pytest.helpers.create_formula_test(
    "TMath::HbarUncertainty()", numexpr_raises=NotImplementedError
)
test_hc = pytest.helpers.create_formula_test("TMath::HC()")
test_hccgs = pytest.helpers.create_formula_test("TMath::HCcgs()")
test_mwair = pytest.helpers.create_formula_test("TMath::MWair()")
test_sigma = pytest.helpers.create_formula_test("TMath::Sigma()")
test_sigmauncertainty = pytest.helpers.create_formula_test(
    "TMath::SigmaUncertainty()", numexpr_raises=NotImplementedError
)
test_r = pytest.helpers.create_formula_test("TMath::R()")
test_runcertainty = pytest.helpers.create_formula_test(
    "TMath::RUncertainty()", numexpr_raises=NotImplementedError
)
