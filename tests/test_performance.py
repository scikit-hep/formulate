"""Very long expressions must parse and convert quickly and without recursing
past Python's stack limit.

Both halves matter: the AST walk is recursive, so a 10,000-term expression is
also a regression test for stack depth, and the timing bound catches accidental
quadratic behaviour in the parser or the serializer.
"""

from __future__ import annotations

import random
import sys
import time

import pytest

import formulate

EXPRESSION_LENGTH = 10_000
TIME_LIMIT_SECONDS = 3.0

# The AST is walked recursively, so a long expression needs a deeper stack than
# CPython's default of 1000 frames.
sys.setrecursionlimit(50_000)

VARIABLES = ["a", "b", "c", "d", "x", "y", "z"]
CONSTANTS = ["1.0", "2.0", "3.14", "42.0", "0.5"]
# Operators that mean the same thing in both languages, so the generated
# expression can be fed to either parser.
BINARY_OPERATORS = ["+", "-", "*", "/"]


def generate_long_expression(length: int, seed: int = 0) -> str:
    """Build a valid expression with roughly `length` symbols and operators.

    The generator is seeded so a failure is reproducible.
    """
    rng = random.Random(seed)
    parts = [rng.choice(VARIABLES)]
    while len(parts) < length:
        parts.append(rng.choice(BINARY_OPERATORS))
        parts.append(rng.choice(VARIABLES + CONSTANTS))
    return "".join(parts)


def test_generated_expression_is_long_and_parseable():
    expr = generate_long_expression(EXPRESSION_LENGTH)
    assert len(expr) >= EXPRESSION_LENGTH

    parsed = formulate.from_root(expr)
    assert parsed.variables <= set(VARIABLES)


# Nesting costs far more stack than chaining. The grammar's precedence chain
# (expression -> disjunction -> ... -> atom) is eleven rules deep and none of
# them are inlined, so each "(" costs about eleven `toast` frames where each
# "+" in a flat chain costs one.
#
# Deep enough input exhausts the C stack and kills the interpreter outright
# rather than raising RecursionError, because the limit raised above lets Python
# outrun it. Measured against a 1 MB stack -- the tightest CI platform -- 300
# levels still parse and 500 crash, so this stays well below that.
NESTING_DEPTH = 100


def test_nested_parentheses_parse_at_moderate_depth():
    """Redundant nesting is a different shape from a long chain, and collapses
    away entirely once parsed."""
    expr = "(" * NESTING_DEPTH + "a" + ")" * NESTING_DEPTH
    assert formulate.from_root(expr).to_root() == "a"


@pytest.mark.parametrize(
    "name,length,parse,serialize",
    [
        ("root->python", EXPRESSION_LENGTH, formulate.from_root, "to_python"),
        ("numexpr->python", EXPRESSION_LENGTH, formulate.from_numexpr, "to_python"),
        ("root->numexpr", 1000, formulate.from_root, "to_numexpr"),
        ("numexpr->root", 1000, formulate.from_numexpr, "to_root"),
    ],
)
def test_parse_and_convert_stay_within_the_time_limit(name, length, parse, serialize):
    expr = generate_long_expression(length)

    start = time.perf_counter()
    converted = getattr(parse(expr), serialize)()
    elapsed = time.perf_counter() - start

    assert converted
    assert elapsed < TIME_LIMIT_SECONDS, (
        f"{name} took {elapsed:.2f}s for a {length}-term expression, "
        f"which exceeds the {TIME_LIMIT_SECONDS}s limit"
    )


@pytest.mark.parametrize(
    "name,forward,backward",
    [
        ("root->numexpr->root", "to_numexpr", "to_root"),
        ("numexpr->root->numexpr", "to_root", "to_numexpr"),
    ],
)
def test_long_expressions_survive_a_full_round_trip(name, forward, backward):
    expr = generate_long_expression(1000)
    first_parse = (
        formulate.from_root if name.startswith("root") else formulate.from_numexpr
    )
    second_parse = (
        formulate.from_numexpr if name.startswith("root") else formulate.from_root
    )

    canonical = getattr(first_parse(expr), forward)()
    round_tripped = getattr(second_parse(canonical), backward)()
    assert getattr(first_parse(round_tripped), forward)() == canonical
