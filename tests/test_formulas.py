# Licensed under a 3-clause BSD style license, see LICENSE.
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import pytest

from formulate import from_root, to_root
from formulate import from_numexpr, to_numexpr

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


def create_formula_test(input_string, input_backend='root', numexpr_raises=None):
    assert input_backend in ('root', 'numexpr'), 'Unrecognised backend specified'
    input_from_method = {
        'root': from_root,
        'numexpr': from_numexpr,
    }[input_backend]

    def test_constant():
        expression = input_from_method(input_string)

        if input_backend == 'root':
            root_result = to_root(expression)
            assert input_string, root_result

            if numexpr_raises:
                with pytest.raises(numexpr_raises):
                    to_numexpr(expression)
            else:
                numexpr_result = to_numexpr(expression)
                assert pytest.approx(root_eval(root_result), numexpr_eval(numexpr_result))
        else:
            raise NotImplementedError()

    return test_constant


test_root_BesselI0 = create_formula_test('TMath::BesselI0(A)', numexpr_raises=NotImplementedError)
test_root_BesselI1 = create_formula_test('TMath::BesselI1(A)', numexpr_raises=NotImplementedError)
test_root_BesselJ0 = create_formula_test('TMath::BesselJ0(A)', numexpr_raises=NotImplementedError)
test_root_BesselJ1 = create_formula_test('TMath::BesselJ1(A)', numexpr_raises=NotImplementedError)
test_root_BesselK0 = create_formula_test('TMath::BesselK0(A)', numexpr_raises=NotImplementedError)
test_root_BesselK1 = create_formula_test('TMath::BesselK1(A)', numexpr_raises=NotImplementedError)
test_root_BesselY0 = create_formula_test('TMath::BesselY0(A)', numexpr_raises=NotImplementedError)
test_root_BesselY1 = create_formula_test('TMath::BesselY1(A)', numexpr_raises=NotImplementedError)
test_root_Ceil = create_formula_test('TMath::Ceil(A)', numexpr_raises=NotImplementedError)
test_root_CeilNint = create_formula_test('TMath::CeilNint(A)', numexpr_raises=NotImplementedError)
test_root_DiLog = create_formula_test('TMath::DiLog(A)', numexpr_raises=NotImplementedError)
test_root_Erf = create_formula_test('TMath::Erf(A)', numexpr_raises=NotImplementedError)
test_root_Erfc = create_formula_test('TMath::Erfc(A)', numexpr_raises=NotImplementedError)
test_root_ErfcInverse = create_formula_test('TMath::ErfcInverse(A)', numexpr_raises=NotImplementedError)
test_root_ErfInverse = create_formula_test('TMath::ErfInverse(A)', numexpr_raises=NotImplementedError)
test_root_Even = create_formula_test('TMath::Even(A)', numexpr_raises=NotImplementedError)
test_root_Factorial = create_formula_test('TMath::Factorial(A)', numexpr_raises=NotImplementedError)
test_root_Floor = create_formula_test('TMath::Floor(A)', numexpr_raises=NotImplementedError)
test_root_FloorNint = create_formula_test('TMath::FloorNint(A)', numexpr_raises=NotImplementedError)
test_root_Freq = create_formula_test('TMath::Freq(A)', numexpr_raises=NotImplementedError)
test_root_KolmogorovProb = create_formula_test('TMath::KolmogorovProb(A)', numexpr_raises=NotImplementedError)
test_root_LandauI = create_formula_test('TMath::LandauI(A)', numexpr_raises=NotImplementedError)
test_root_LnGamma = create_formula_test('TMath::LnGamma(A)', numexpr_raises=NotImplementedError)
test_root_NextPrime = create_formula_test('TMath::NextPrime(A)', numexpr_raises=NotImplementedError)
test_root_NormQuantile = create_formula_test('TMath::NormQuantile(A)', numexpr_raises=NotImplementedError)
test_root_Odd = create_formula_test('TMath::Odd(A)', numexpr_raises=NotImplementedError)
test_root_Sq = create_formula_test('TMath::Sq(1.234)')
test_root_StruveH0 = create_formula_test('TMath::StruveH0(A)', numexpr_raises=NotImplementedError)
test_root_StruveH1 = create_formula_test('TMath::StruveH1(A)', numexpr_raises=NotImplementedError)
test_root_StruveL0 = create_formula_test('TMath::StruveL0(A)', numexpr_raises=NotImplementedError)
test_root_StruveL1 = create_formula_test('TMath::StruveL1(A)', numexpr_raises=NotImplementedError)
test_root_BesselI = create_formula_test('TMath::BesselI(A, B)', numexpr_raises=NotImplementedError)
test_root_BesselK = create_formula_test('TMath::BesselK(A, B)', numexpr_raises=NotImplementedError)
test_root_Beta = create_formula_test('TMath::Beta(A, B)', numexpr_raises=NotImplementedError)
test_root_Binomial = create_formula_test('TMath::Binomial(A, B)', numexpr_raises=NotImplementedError)
test_root_ChisquareQuantile = create_formula_test('TMath::ChisquareQuantile(A, B)', numexpr_raises=NotImplementedError)
test_root_Ldexp = create_formula_test('TMath::Ldexp(A, B)', numexpr_raises=NotImplementedError)
test_root_Permute = create_formula_test('TMath::Permute(A, B)', numexpr_raises=NotImplementedError)
test_root_Poisson = create_formula_test('TMath::Poisson(A, B)', numexpr_raises=NotImplementedError)
test_root_PoissonI = create_formula_test('TMath::PoissonI(A, B)', numexpr_raises=NotImplementedError)
test_root_Prob = create_formula_test('TMath::Prob(A, B)', numexpr_raises=NotImplementedError)
test_root_Student = create_formula_test('TMath::Student(A, B)', numexpr_raises=NotImplementedError)
test_root_StudentI = create_formula_test('TMath::StudentI(A, B)', numexpr_raises=NotImplementedError)
test_root_AreEqualAbs = create_formula_test('TMath::AreEqualAbs(A, B, C)', numexpr_raises=NotImplementedError)
test_root_AreEqualRel = create_formula_test('TMath::AreEqualRel(A, B, C)', numexpr_raises=NotImplementedError)
test_root_BetaCf = create_formula_test('TMath::BetaCf(A, B, C)', numexpr_raises=NotImplementedError)
test_root_BetaDist = create_formula_test('TMath::BetaDist(A, B, C)', numexpr_raises=NotImplementedError)
test_root_BetaDistI = create_formula_test('TMath::BetaDistI(A, B, C)', numexpr_raises=NotImplementedError)
test_root_BetaIncomplete = create_formula_test('TMath::BetaIncomplete(A, B, C)', numexpr_raises=NotImplementedError)
test_root_BinomialI = create_formula_test('TMath::BinomialI(A, B, C)', numexpr_raises=NotImplementedError)
test_root_BubbleHigh = create_formula_test('TMath::BubbleHigh(A, B, C)', numexpr_raises=NotImplementedError)
test_root_BubbleLow = create_formula_test('TMath::BubbleLow(A, B, C)', numexpr_raises=NotImplementedError)
test_root_FDist = create_formula_test('TMath::FDist(A, B, C)', numexpr_raises=NotImplementedError)
test_root_FDistI = create_formula_test('TMath::FDistI(A, B, C)', numexpr_raises=NotImplementedError)
test_root_Vavilov = create_formula_test('TMath::Vavilov(A, B, C)', numexpr_raises=NotImplementedError)
test_root_VavilovI = create_formula_test('TMath::VavilovI(A, B, C)', numexpr_raises=NotImplementedError)
test_root_RootsCubic = create_formula_test('TMath::RootsCubic(A, B, C, D)', numexpr_raises=NotImplementedError)
test_root_Quantiles = create_formula_test('TMath::Quantiles(A, B, C, D, E)', numexpr_raises=NotImplementedError)
