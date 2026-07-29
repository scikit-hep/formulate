"""Consistency of the identifier tables, and coverage of every entry in them.

``identifiers.py`` is a set of hand-maintained lookup tables.  Nothing in the
parser or serializer validates them, so a typo, a stale alias or a name that is
declared but never mapped to a backend would only show up as a confusing
runtime error for one particular expression.  These tests check the tables
against each other, and drive every single function and constant through the
parser so that a broken entry fails loudly.
"""

from __future__ import annotations

import numpy as np
import pytest

import formulate
from formulate.identifiers import (
    BINARY_OPERATORS,
    CONSTANTS,
    CONSTANTS_ALIASES,
    CONSTANTS_FUNCTION_ALIASES,
    FUNCTION_ALIASES,
    FUNCTIONS,
    NUMEXPR_CONSTANTS,
    NUMEXPR_FUNCTIONS,
    NUMEXPR_OPERATOR_SYMBOLS,
    PYTHON_CONSTANTS,
    PYTHON_FUNCTIONS,
    PYTHON_OPERATOR_SYMBOLS,
    ROOT_CONSTANTS,
    ROOT_FUNCTIONS,
    ROOT_OPERATOR_SYMBOLS,
    UNARY_OPERATORS,
)

BACKEND_FUNCTIONS = {
    "numexpr": NUMEXPR_FUNCTIONS,
    "root": ROOT_FUNCTIONS,
    "python": PYTHON_FUNCTIONS,
}
BACKEND_CONSTANTS = {
    "numexpr": NUMEXPR_CONSTANTS,
    "root": ROOT_CONSTANTS,
    "python": PYTHON_CONSTANTS,
}
BACKEND_OPERATORS = {
    "numexpr": NUMEXPR_OPERATOR_SYMBOLS,
    "root": ROOT_OPERATOR_SYMBOLS,
    "python": PYTHON_OPERATOR_SYMBOLS,
}

# NumExpr has no way to spell a non-finite value, so it is the one backend
# allowed to omit constants.
CONSTANTS_MISSING_FROM_NUMEXPR = {"inf", "neginf", "nan"}


# --- Cross-table consistency ---


@pytest.mark.parametrize("backend", sorted(BACKEND_FUNCTIONS))
def test_backend_function_tables_only_use_canonical_names(backend):
    assert set(BACKEND_FUNCTIONS[backend]) <= FUNCTIONS


@pytest.mark.parametrize("name", sorted(FUNCTIONS))
def test_every_function_is_available_in_at_least_one_backend(name):
    assert any(name in table for table in BACKEND_FUNCTIONS.values())


@pytest.mark.parametrize("backend", sorted(BACKEND_CONSTANTS))
def test_backend_constant_tables_only_use_canonical_names(backend):
    assert set(BACKEND_CONSTANTS[backend]) <= CONSTANTS


@pytest.mark.parametrize("backend", ["root", "python"])
def test_root_and_python_define_every_constant(backend):
    assert set(BACKEND_CONSTANTS[backend]) == CONSTANTS


def test_numexpr_omits_only_the_non_finite_constants():
    assert CONSTANTS - set(NUMEXPR_CONSTANTS) == CONSTANTS_MISSING_FROM_NUMEXPR


@pytest.mark.parametrize("backend", sorted(BACKEND_OPERATORS))
def test_backend_operator_tables_only_use_known_operators(backend):
    assert set(BACKEND_OPERATORS[backend]) <= UNARY_OPERATORS | BINARY_OPERATORS


def test_unary_and_binary_operator_names_do_not_overlap():
    assert not UNARY_OPERATORS & BINARY_OPERATORS


@pytest.mark.parametrize("alias,target", sorted(FUNCTION_ALIASES.items()))
def test_function_aliases_point_at_a_real_function(alias, target):
    assert target in FUNCTIONS
    assert alias not in FUNCTIONS, "an alias must not also be a canonical name"


@pytest.mark.parametrize("alias,target", sorted(CONSTANTS_ALIASES.items()))
def test_constant_aliases_point_at_a_real_constant(alias, target):
    assert target in CONSTANTS
    assert alias not in CONSTANTS, "an alias must not also be a canonical name"


@pytest.mark.parametrize("target", sorted(set(CONSTANTS_FUNCTION_ALIASES.values())))
def test_constant_function_aliases_point_at_a_real_constant(target):
    assert target in CONSTANTS


def test_function_and_constant_names_do_not_collide():
    assert not FUNCTIONS & CONSTANTS


# --- Every table entry actually works end to end ---


@pytest.mark.parametrize("canonical,root_name", sorted(ROOT_FUNCTIONS.items()))
def test_every_root_function_name_parses_and_round_trips(canonical, root_name):
    parsed = formulate.from_root(f"{root_name}(x)")
    assert parsed.function == canonical
    assert parsed.to_root() == f"{root_name}(x)"


@pytest.mark.parametrize("numexpr_name", sorted(set(NUMEXPR_FUNCTIONS.values())))
def test_every_numexpr_function_name_parses_and_round_trips(numexpr_name):
    parsed = formulate.from_numexpr(f"{numexpr_name}(x)")
    assert parsed.to_numexpr() == f"{numexpr_name}(x)"


@pytest.mark.parametrize("alias,target", sorted(FUNCTION_ALIASES.items()))
def test_every_function_alias_resolves_when_parsed(alias, target):
    assert formulate.from_root(f"{alias}(x)").function == target


@pytest.mark.parametrize("arity", [0, 1, 2, 3, 8])
def test_functions_accept_any_number_of_arguments(arity):
    """formulate translates names, it does not type-check calls.

    ROOT has functions taking anywhere from zero to eight arguments, and the
    tables record no arity, so a wrong argument count is deliberately left for
    the target engine to reject.
    """
    arguments = ", ".join(f"x{i}" for i in range(arity))
    assert formulate.from_root(f"TMath::Sqrt({arguments})").to_root() == (
        f"TMath::Sqrt({arguments})"
    )


@pytest.mark.parametrize("numpy_name", sorted(set(PYTHON_FUNCTIONS.values())))
def test_python_backend_names_exist_in_numpy(numpy_name):
    """Every name the Python backend emits must be a real NumPy attribute,
    otherwise `to_python` produces code that fails with a NameError."""
    assert hasattr(np, numpy_name), f"np.{numpy_name} does not exist"


def test_contains_is_not_offered_by_the_python_backend():
    # NumExpr's substring test has no single-name NumPy equivalent, so it must
    # be refused rather than rendered as a call to a function that is not there
    assert "contains" not in PYTHON_FUNCTIONS
    with pytest.raises(ValueError, match="not supported in Python"):
        formulate.from_numexpr("contains(s, t)").to_python()


@pytest.mark.parametrize(
    "rendering",
    [pytest.param(value, id=name) for name, value in sorted(PYTHON_CONSTANTS.items())],
)
def test_python_constant_renderings_are_evaluable(rendering):
    value = eval(str(rendering), {"np": np})
    assert isinstance(value, (bool, int, float))


@pytest.mark.parametrize("canonical", sorted(CONSTANTS))
def test_every_canonical_constant_name_parses_as_that_constant(canonical):
    parsed = formulate.from_root(canonical)
    assert parsed.name == canonical
    assert parsed.named_constants == {canonical}
    assert parsed.variables == set()


@pytest.mark.parametrize("alias,target", sorted(CONSTANTS_ALIASES.items()))
def test_every_constant_alias_resolves_when_parsed(alias, target):
    assert formulate.from_root(alias).name == target


@pytest.mark.parametrize("alias,target", sorted(CONSTANTS_FUNCTION_ALIASES.items()))
def test_every_constant_function_alias_resolves_when_called(alias, target):
    # These spellings only exist in ROOT's function form, e.g. TMath::E()
    assert formulate.from_root(f"TMath::{alias}()").name == target


@pytest.mark.parametrize("canonical,root_repr", sorted(ROOT_CONSTANTS.items()))
def test_every_root_constant_spelling_parses_back_to_its_canonical_name(
    canonical, root_repr
):
    parsed = formulate.from_root(root_repr)
    if root_repr.startswith("-"):
        # -TMath::Qe() and -TMath::Infinity() parse as a negation of the
        # positive constant rather than as an atom of their own.
        assert parsed.operator == "neg"
        assert ROOT_CONSTANTS[parsed.operand.name] == root_repr.removeprefix("-")
        assert parsed.to_root() == f"({root_repr})"
    elif root_repr.startswith("("):
        # hbarc is spelled as a product of two other constants
        assert parsed.to_root() == root_repr
    else:
        assert parsed.name == canonical
        assert parsed.to_root() == root_repr


@pytest.mark.parametrize("canonical", sorted(NUMEXPR_CONSTANTS))
def test_every_numexpr_constant_is_inlined_as_a_literal(canonical):
    rendered = formulate.from_root(canonical).to_numexpr()
    assert rendered == str(NUMEXPR_CONSTANTS[canonical])


@pytest.mark.parametrize("canonical", sorted(CONSTANTS_MISSING_FROM_NUMEXPR))
def test_constants_absent_from_numexpr_raise_a_clear_error(canonical):
    with pytest.raises(ValueError, match="not supported in NumExpr"):
        formulate.from_root(canonical).to_numexpr()


# --- Function names are case insensitive ---


@pytest.mark.parametrize("spelling", ["sqrt", "Sqrt", "SQRT", "sQrT", "TMath::sqrt"])
def test_function_names_are_case_insensitive(spelling):
    assert formulate.from_root(f"{spelling}(x)").to_root() == "TMath::Sqrt(x)"


@pytest.mark.parametrize("spelling", ["Sum$", "sum$", "SUM$", "sum"])
def test_array_function_names_are_case_insensitive(spelling):
    assert formulate.from_root(f"{spelling}(x)").to_root() == "Sum$(x)"
