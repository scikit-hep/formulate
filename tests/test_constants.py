# Licensed under a 3-clause BSD style license, see LICENSE.
"""Numerical agreement with the real ROOT and NumExpr engines.

This is the only file that evaluates expressions with the systems formulate
translates between, so it is what proves the tables hold the right *values*
rather than merely the right spellings.  It is skipped unless ROOT is
importable (CI installs it on Linux only).

The cases are driven off the identifier tables rather than hand-listed, so a
constant or function added to ``identifiers.py`` is checked against ROOT
automatically instead of silently going untested.
"""

from __future__ import annotations

import numexpr
import numpy as np
import pytest

import formulate
from formulate.identifiers import (
    NUMEXPR_CONSTANTS,
    ROOT_CONSTANTS,
    ROOT_FUNCTIONS,
)

ROOT = pytest.importorskip("ROOT")

# TFormula's Eval() takes up to four positional variables, named x, y, z and t.
VARIABLE_VALUES = {"x": 2.0, "y": 3.0, "z": 4.0, "t": 5.0}

# The Python backend renders ROOT's '!' as NumPy's '~', which is only correct
# for NumPy operands -- '~' on a plain Python bool is deprecated since 3.13 and
# means bitwise inversion of the underlying int.  Evaluate with NumPy scalars,
# which is what the generated code is meant to be used with.
NUMPY_VARIABLE_VALUES = {
    name: np.float64(value) for name, value in VARIABLE_VALUES.items()
}


def root_eval(expression: str) -> float:
    formula = ROOT.TFormula("", expression)
    assert formula.Compile() == 0, f"ROOT failed to compile {expression!r}"
    return formula.Eval(*VARIABLE_VALUES.values())


def numexpr_eval(expression: str) -> float:
    return float(numexpr.evaluate(expression, local_dict=VARIABLE_VALUES))


def assert_same_value(left: float, right: float, context: str) -> None:
    if np.isnan(left):
        assert np.isnan(right), f"{context}: {left} != {right}"
    else:
        assert np.isclose(left, right), f"{context}: {left} != {right}"


# --- Constants ---


@pytest.mark.parametrize("canonical,root_repr", sorted(ROOT_CONSTANTS.items()))
def test_root_constant_survives_reserialization(canonical, root_repr):
    """Parsing ROOT's spelling and writing it back must not change its value."""
    assert_same_value(
        root_eval(root_repr),
        root_eval(formulate.from_root(root_repr).to_root()),
        f"ROOT round trip of {canonical}",
    )


@pytest.mark.parametrize(
    "canonical,root_repr",
    sorted(item for item in ROOT_CONSTANTS.items() if item[0] in NUMEXPR_CONSTANTS),
)
def test_root_and_numexpr_constants_hold_the_same_value(canonical, root_repr):
    """The number formulate inlines for NumExpr must be what ROOT computes."""
    assert_same_value(
        root_eval(root_repr),
        numexpr_eval(formulate.from_root(root_repr).to_numexpr()),
        f"ROOT vs NumExpr for {canonical}",
    )


@pytest.mark.parametrize(
    "canonical", sorted(set(ROOT_CONSTANTS) - set(NUMEXPR_CONSTANTS))
)
def test_constants_root_has_but_numexpr_lacks(canonical):
    """inf/neginf/nan evaluate in ROOT but cannot be written in NumExpr."""
    root_repr = ROOT_CONSTANTS[canonical]
    assert not np.isfinite(root_eval(root_repr))
    with pytest.raises(ValueError, match="not supported in NumExpr"):
        formulate.from_root(root_repr).to_numexpr()


@pytest.mark.parametrize(
    "source,language",
    [
        ("True", "numexpr"),
        ("False", "numexpr"),
        ("pi", "numexpr"),
        ("exp1", "numexpr"),
        ("ln10", "numexpr"),
        ("true", "root"),
        ("false", "root"),
        ("sqrt2", "root"),
        ("e_number", "root"),
        ("twopi", "root"),
    ],
)
def test_alternative_constant_spellings_reach_the_same_value(source, language):
    """Bare and aliased names take a different path through the parser than the
    ``TMath::Xxx()`` call form, so they are checked separately."""
    parse = {"root": formulate.from_root, "numexpr": formulate.from_numexpr}[language]
    expression = parse(source)
    assert_same_value(
        root_eval(expression.to_root()),
        numexpr_eval(expression.to_numexpr()),
        f"ROOT vs NumExpr for {source!r}",
    )


# --- Functions ---


@pytest.mark.parametrize(
    "root_name",
    sorted(name for name in ROOT_FUNCTIONS.values() if name.startswith("TMath::")),
)
def test_every_tmath_name_exists_in_root(root_name):
    """A typo in ROOT_FUNCTIONS would otherwise only surface as a ROOT
    compilation failure for whoever happened to use that function."""
    assert hasattr(ROOT.TMath, root_name.removeprefix("TMath::"))


# --- Whole expressions ---

# '%' is excluded on purpose: formulate translates it faithfully, but TFormula
# compiles to C++ where '%' is integer-only and so rejects it on doubles.
SHARED_EXPRESSIONS = [
    # Arithmetic and precedence
    "x+y*z",
    "(x+y)*z",
    "x/y/z",
    "x-y-z",
    "x**2",
    "x^2",
    "x**y**2",
    "-x+y",
    "x - -y",
    "pow(x, 2)",
    "TMath::Power(x, y)",
    # Functions
    "TMath::Sqrt(x*x + y*y)",
    "TMath::Abs(x-y)",
    "TMath::Exp(-x)",
    "TMath::Log(x+1)",
    "TMath::Log10(z)",
    "TMath::Sin(x)+TMath::Cos(y)",
    "TMath::ATan2(x, y)",
    "TMath::Tanh(x)",
    "TMath::Ceil(x/y)",
    "TMath::Floor(x/y)",
    "TMath::Sqrt(TMath::Abs(-x))",
    # Comparisons and logic
    "x>y",
    "x<y",
    "x>=y",
    "x<=y",
    "x==y",
    "x!=y",
    "(x>1)&&(y<2)",
    "(x>1)||(y<2)",
    "!(x>1)",
    # Constants mixed with variables
    "TMath::Pi()*x",
    "x/TMath::Sqrt2()",
    "TMath::Exp(-0.5*((x-y)/z)**2)",
]


@pytest.mark.parametrize("expr", SHARED_EXPRESSIONS, ids=lambda x: x)
def test_translated_expression_evaluates_the_same_in_root_and_numexpr(expr):
    """The real test of a translator: both engines must agree on the answer."""
    expression = formulate.from_root(expr)
    assert_same_value(
        root_eval(expression.to_root()),
        numexpr_eval(expression.to_numexpr()),
        f"ROOT vs NumExpr for {expr!r}",
    )


@pytest.mark.parametrize("expr", SHARED_EXPRESSIONS, ids=lambda x: x)
def test_translated_expression_evaluates_the_same_in_root_and_python(expr):
    expression = formulate.from_root(expr)
    rendered = expression.to_python()
    assert_same_value(
        root_eval(expression.to_root()),
        float(eval(rendered, {"np": np, **NUMPY_VARIABLE_VALUES})),
        f"ROOT vs Python for {expr!r}",
    )


@pytest.mark.parametrize("expr", SHARED_EXPRESSIONS, ids=lambda x: x)
def test_root_expression_keeps_its_value_through_a_round_trip(expr):
    """ROOT -> NumExpr -> ROOT must not change what ROOT computes."""
    canonical = formulate.from_root(expr).to_root()
    round_tripped = formulate.from_numexpr(
        formulate.from_root(expr).to_numexpr()
    ).to_root()
    assert_same_value(
        root_eval(canonical), root_eval(round_tripped), f"round trip of {expr!r}"
    )


def test_element_wise_min_max_are_not_translated_to_numexpr():
    """NumExpr's min/max reduce an array, so they cannot express TMath::Min.

    Emitting ``min(a, b)`` would produce NumExpr that fails at evaluation time,
    which is why the mapping is absent; ROOT and Python both keep working.
    """
    # Establish the premise: NumExpr really does reject the two-argument form.
    # The exception type is not part of NumExpr's API, so only the failure is
    # asserted.
    with pytest.raises(Exception):
        numexpr.evaluate("min(x, y)", local_dict=VARIABLE_VALUES)

    for expr in ("TMath::Min(x, y)", "TMath::Max(x, y)"):
        with pytest.raises(ValueError, match="not supported in NumExpr"):
            formulate.from_root(expr).to_numexpr()

    assert root_eval("TMath::Min(x, y)") == min(
        VARIABLE_VALUES["x"], VARIABLE_VALUES["y"]
    )
    assert eval(
        formulate.from_root("TMath::Min(x, y)").to_python(),
        {"np": np, **NUMPY_VARIABLE_VALUES},
    ) == min(VARIABLE_VALUES["x"], VARIABLE_VALUES["y"])
