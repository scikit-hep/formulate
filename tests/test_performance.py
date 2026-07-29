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


def test_deeply_nested_expression_does_not_overflow_the_stack():
    """Nesting, rather than chaining, is what drives recursion depth."""
    expr = "((((" * 500 + "a" + "))))" * 500
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
