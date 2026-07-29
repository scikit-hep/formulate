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


# Sizes below are bounded by C stack, not by the recursion limit raised above.
# Because that limit is raised, `toast` can recurse past the point where the C
# stack runs out, and the interpreter dies outright instead of raising
# RecursionError.
#
# The binding platform is Python 3.10 on Windows under coverage: 3.11 moved
# pure-Python calls off the C stack, so 3.11+ has orders of magnitude more room
# and never reaches this, and coverage's tracer adds a C frame per Python frame.
# Measured peak Python frames against what that job actually does:
#
#     one-way parse of 10,000 terms   2,565   passes
#     round trip of 1,000 terms       3,029   crashes
#     nesting of 100 levels           1,118   passes
#     round trip of 200 terms           713   passes
#
# So the budget there is somewhere between 2,500 and 3,000 frames. Keep new
# cases well under that, and measure rather than reason about it: frame counts
# are not obvious from the size of the expression.
NESTING_DEPTH = 100

# Round trips are far more expensive than one-way conversions of the same
# length, because the canonical form is fully parenthesized: a 1,000-term chain
# comes back as 251 levels of nesting, and re-parsing nesting costs about eleven
# frames per level (the grammar's precedence chain, expression -> disjunction ->
# ... -> atom, is eleven rules deep and none of them are inlined). That is why
# this is so much smaller than EXPRESSION_LENGTH.
ROUND_TRIP_LENGTH = 200


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
    expr = generate_long_expression(ROUND_TRIP_LENGTH)
    first_parse = (
        formulate.from_root if name.startswith("root") else formulate.from_numexpr
    )
    second_parse = (
        formulate.from_numexpr if name.startswith("root") else formulate.from_root
    )

    canonical = getattr(first_parse(expr), forward)()
    round_tripped = getattr(second_parse(canonical), backward)()
    assert getattr(first_parse(round_tripped), forward)() == canonical
