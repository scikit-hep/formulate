# Licensed under a 3-clause BSD style license, see LICENSE.
import pytest

test_root_BesselI0 = pytest.helpers.create_formula_test(
    "TMath::BesselI0(A)", numexpr_raises=NotImplementedError
)
test_root_BesselI1 = pytest.helpers.create_formula_test(
    "TMath::BesselI1(A)", numexpr_raises=NotImplementedError
)
test_root_BesselJ0 = pytest.helpers.create_formula_test(
    "TMath::BesselJ0(A)", numexpr_raises=NotImplementedError
)
test_root_BesselJ1 = pytest.helpers.create_formula_test(
    "TMath::BesselJ1(A)", numexpr_raises=NotImplementedError
)
test_root_BesselK0 = pytest.helpers.create_formula_test(
    "TMath::BesselK0(A)", numexpr_raises=NotImplementedError
)
test_root_BesselK1 = pytest.helpers.create_formula_test(
    "TMath::BesselK1(A)", numexpr_raises=NotImplementedError
)
test_root_BesselY0 = pytest.helpers.create_formula_test(
    "TMath::BesselY0(A)", numexpr_raises=NotImplementedError
)
test_root_BesselY1 = pytest.helpers.create_formula_test(
    "TMath::BesselY1(A)", numexpr_raises=NotImplementedError
)
test_root_Ceil = pytest.helpers.create_formula_test(
    "TMath::Ceil(A)", numexpr_raises=NotImplementedError
)
test_root_CeilNint = pytest.helpers.create_formula_test(
    "TMath::CeilNint(A)", numexpr_raises=NotImplementedError
)
test_root_DiLog = pytest.helpers.create_formula_test(
    "TMath::DiLog(A)", numexpr_raises=NotImplementedError
)
test_root_Erf = pytest.helpers.create_formula_test(
    "TMath::Erf(A)", numexpr_raises=NotImplementedError
)
test_root_Erfc = pytest.helpers.create_formula_test(
    "TMath::Erfc(A)", numexpr_raises=NotImplementedError
)
test_root_ErfcInverse = pytest.helpers.create_formula_test(
    "TMath::ErfcInverse(A)", numexpr_raises=NotImplementedError
)
test_root_ErfInverse = pytest.helpers.create_formula_test(
    "TMath::ErfInverse(A)", numexpr_raises=NotImplementedError
)
test_root_Even = pytest.helpers.create_formula_test(
    "TMath::Even(A)", numexpr_raises=NotImplementedError
)
test_root_Factorial = pytest.helpers.create_formula_test(
    "TMath::Factorial(A)", numexpr_raises=NotImplementedError
)
test_root_Floor = pytest.helpers.create_formula_test(
    "TMath::Floor(A)", numexpr_raises=NotImplementedError
)
test_root_FloorNint = pytest.helpers.create_formula_test(
    "TMath::FloorNint(A)", numexpr_raises=NotImplementedError
)
test_root_Freq = pytest.helpers.create_formula_test(
    "TMath::Freq(A)", numexpr_raises=NotImplementedError
)
test_root_KolmogorovProb = pytest.helpers.create_formula_test(
    "TMath::KolmogorovProb(A)", numexpr_raises=NotImplementedError
)
test_root_LandauI = pytest.helpers.create_formula_test(
    "TMath::LandauI(A)", numexpr_raises=NotImplementedError
)
test_root_LnGamma = pytest.helpers.create_formula_test(
    "TMath::LnGamma(A)", numexpr_raises=NotImplementedError
)
test_root_NextPrime = pytest.helpers.create_formula_test(
    "TMath::NextPrime(A)", numexpr_raises=NotImplementedError
)
test_root_NormQuantile = pytest.helpers.create_formula_test(
    "TMath::NormQuantile(A)", numexpr_raises=NotImplementedError
)
test_root_Odd = pytest.helpers.create_formula_test(
    "TMath::Odd(A)", numexpr_raises=NotImplementedError
)
test_root_Sq = pytest.helpers.create_formula_test("TMath::Sq(1.234)")
test_root_StruveH0 = pytest.helpers.create_formula_test(
    "TMath::StruveH0(A)", numexpr_raises=NotImplementedError
)
test_root_StruveH1 = pytest.helpers.create_formula_test(
    "TMath::StruveH1(A)", numexpr_raises=NotImplementedError
)
test_root_StruveL0 = pytest.helpers.create_formula_test(
    "TMath::StruveL0(A)", numexpr_raises=NotImplementedError
)
test_root_StruveL1 = pytest.helpers.create_formula_test(
    "TMath::StruveL1(A)", numexpr_raises=NotImplementedError
)
test_root_BesselI = pytest.helpers.create_formula_test(
    "TMath::BesselI(A, B)", numexpr_raises=NotImplementedError
)
test_root_BesselK = pytest.helpers.create_formula_test(
    "TMath::BesselK(A, B)", numexpr_raises=NotImplementedError
)
test_root_Beta = pytest.helpers.create_formula_test(
    "TMath::Beta(A, B)", numexpr_raises=NotImplementedError
)
test_root_Binomial = pytest.helpers.create_formula_test(
    "TMath::Binomial(A, B)", numexpr_raises=NotImplementedError
)
test_root_ChisquareQuantile = pytest.helpers.create_formula_test(
    "TMath::ChisquareQuantile(A, B)", numexpr_raises=NotImplementedError
)
test_root_Ldexp = pytest.helpers.create_formula_test(
    "TMath::Ldexp(A, B)", numexpr_raises=NotImplementedError
)
test_root_Permute = pytest.helpers.create_formula_test(
    "TMath::Permute(A, B)", numexpr_raises=NotImplementedError
)
test_root_Poisson = pytest.helpers.create_formula_test(
    "TMath::Poisson(A, B)", numexpr_raises=NotImplementedError
)
test_root_PoissonI = pytest.helpers.create_formula_test(
    "TMath::PoissonI(A, B)", numexpr_raises=NotImplementedError
)
test_root_Prob = pytest.helpers.create_formula_test(
    "TMath::Prob(A, B)", numexpr_raises=NotImplementedError
)
test_root_Student = pytest.helpers.create_formula_test(
    "TMath::Student(A, B)", numexpr_raises=NotImplementedError
)
test_root_StudentI = pytest.helpers.create_formula_test(
    "TMath::StudentI(A, B)", numexpr_raises=NotImplementedError
)
test_root_AreEqualAbs = pytest.helpers.create_formula_test(
    "TMath::AreEqualAbs(A, B, C)", numexpr_raises=NotImplementedError
)
test_root_AreEqualRel = pytest.helpers.create_formula_test(
    "TMath::AreEqualRel(A, B, C)", numexpr_raises=NotImplementedError
)
test_root_BetaCf = pytest.helpers.create_formula_test(
    "TMath::BetaCf(A, B, C)", numexpr_raises=NotImplementedError
)
test_root_BetaDist = pytest.helpers.create_formula_test(
    "TMath::BetaDist(A, B, C)", numexpr_raises=NotImplementedError
)
test_root_BetaDistI = pytest.helpers.create_formula_test(
    "TMath::BetaDistI(A, B, C)", numexpr_raises=NotImplementedError
)
test_root_BetaIncomplete = pytest.helpers.create_formula_test(
    "TMath::BetaIncomplete(A, B, C)", numexpr_raises=NotImplementedError
)
test_root_BinomialI = pytest.helpers.create_formula_test(
    "TMath::BinomialI(A, B, C)", numexpr_raises=NotImplementedError
)
test_root_BubbleHigh = pytest.helpers.create_formula_test(
    "TMath::BubbleHigh(A, B, C)", numexpr_raises=NotImplementedError
)
test_root_BubbleLow = pytest.helpers.create_formula_test(
    "TMath::BubbleLow(A, B, C)", numexpr_raises=NotImplementedError
)
test_root_FDist = pytest.helpers.create_formula_test(
    "TMath::FDist(A, B, C)", numexpr_raises=NotImplementedError
)
test_root_FDistI = pytest.helpers.create_formula_test(
    "TMath::FDistI(A, B, C)", numexpr_raises=NotImplementedError
)
test_root_Vavilov = pytest.helpers.create_formula_test(
    "TMath::Vavilov(A, B, C)", numexpr_raises=NotImplementedError
)
test_root_VavilovI = pytest.helpers.create_formula_test(
    "TMath::VavilovI(A, B, C)", numexpr_raises=NotImplementedError
)
test_root_RootsCubic = pytest.helpers.create_formula_test(
    "TMath::RootsCubic(A, B, C, D)", numexpr_raises=NotImplementedError
)
test_root_Quantiles = pytest.helpers.create_formula_test(
    "TMath::Quantiles(A, B, C, D, E)", numexpr_raises=NotImplementedError
)
