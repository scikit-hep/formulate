# Licensed under a 3-clause BSD style license, see LICENSE.
"""Numerical agreement with the real ROOT and NumExpr engines.

This is the only file that evaluates expressions with the systems formulate
translates between, so it is what proves the constant tables hold the right
*values* rather than merely the right spellings.  It is skipped unless ROOT is
importable (CI installs it on Linux only).
"""

from __future__ import annotations

import numexpr
import numpy as np
import pytest

from formulate import from_numexpr, from_root

ROOT = pytest.importorskip("ROOT")


def root_eval(expression: str) -> float:
    formula = ROOT.TFormula("", expression)
    formula.Compile()
    return formula.Eval(0)


def numexpr_eval(expression: str) -> float:
    return numexpr.evaluate(expression, local_dict={})


def assert_same_value(left: float, right: float, context: str) -> None:
    if np.isnan(left):
        assert np.isnan(right), f"{context}: {left} != {right}"
    else:
        assert np.isclose(left, right), f"{context}: {left} != {right}"


# (source expression, language it is written in, exception to_numexpr should raise)
CONSTANTS = [
    # NumExpr spellings
    ("True", "numexpr", None),
    ("False", "numexpr", None),
    ("exp1", "numexpr", None),
    ("pi", "numexpr", None),
    ("ln10", "numexpr", None),
    # ROOT spellings
    ("true", "root", None),
    ("false", "root", None),
    ("sqrt2", "root", None),
    ("TMath::Sqrt2()", "root", None),
    ("TMath::E()", "root", None),
    ("TMath::Pi()", "root", None),
    ("TMath::PiOver2()", "root", None),
    ("TMath::PiOver4()", "root", None),
    ("TMath::TwoPi()", "root", None),
    ("TMath::InvPi()", "root", None),
    ("TMath::Ln10()", "root", None),
    ("TMath::LogE()", "root", None),
    ("TMath::DegToRad()", "root", None),
    ("TMath::RadToDeg()", "root", None),
    ("TMath::Na()", "root", None),
    ("TMath::K()", "root", None),
    ("TMath::C()", "root", None),
    ("TMath::Qe()", "root", None),
    ("TMath::H()", "root", None),
    ("TMath::Hbar()", "root", None),
    # Non-finite values exist in ROOT but cannot be expressed in NumExpr
    ("TMath::Infinity()", "root", ValueError),
    ("TMath::QuietNaN()", "root", ValueError),
]


@pytest.mark.parametrize(
    "source,language,numexpr_raises", CONSTANTS, ids=[case[0] for case in CONSTANTS]
)
def test_constant_value_agrees_across_backends(source, language, numexpr_raises):
    parse = {"root": from_root, "numexpr": from_numexpr}[language]
    expression = parse(source)
    root_result = expression.to_root()

    if language == "root":
        # Re-serializing must not change what ROOT computes
        assert_same_value(
            root_eval(source), root_eval(root_result), f"ROOT round trip of {source!r}"
        )

    if numexpr_raises is not None:
        with pytest.raises(numexpr_raises):
            expression.to_numexpr()
        return

    numexpr_result = expression.to_numexpr()
    assert_same_value(
        root_eval(root_result),
        numexpr_eval(numexpr_result),
        f"ROOT vs NumExpr for {source!r}",
    )
