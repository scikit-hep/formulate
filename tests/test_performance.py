"""Very long expressions must parse and convert quickly and without recursing
past Python's stack limit.

Both halves matter. Every walk over the parse tree and the AST — `toast`,
`_to_backend`, `str()` and the `variables` family — uses an explicit stack, so
peak frame depth is a small constant no matter how big the expression is. These
tests deliberately run at CPython's default recursion limit so that
reintroducing a recursive walk fails here rather than in a user's traceback. The
timing bound catches accidental quadratic behaviour in the parser or the
serializer.
"""

from __future__ import annotations

import random
import time

import pytest

import formulate

EXPRESSION_LENGTH = 10_000
TIME_LIMIT_SECONDS = 3.0

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


def test_every_walk_handles_a_long_expression():
    """`str()` and the `variables` family walk the AST as well, and used to be
    the deepest recursion in the package."""
    parsed = formulate.from_root(generate_long_expression(EXPRESSION_LENGTH))

    assert str(parsed)
    assert parsed.to_python()
    assert parsed.variables <= set(VARIABLES)
    assert not parsed.named_constants
    assert parsed.unnamed_constants <= {float(value) for value in CONSTANTS}


# Deep enough that a single recursive frame per level would exhaust CPython's
# default limit of 1000 frames. The sizes in this file are bounded by the time
# limit rather than by the stack now, and the slowest job in the matrix is
# Windows/3.10 under coverage, so keep them modest.
DEEP_NESTING = 1_000

# Redundant parentheses, which the parser has to chew through but which leave
# nothing behind in the AST.
NESTING_DEPTH = 100

# Round trips are far more expensive than one-way conversions of the same
# length, because the canonical form is fully parenthesized: a 1,000-term chain
# comes back as 251 levels of nesting and a much longer string to re-parse. That
# is why this is so much smaller than EXPRESSION_LENGTH.
ROUND_TRIP_LENGTH = 200


def test_nested_parentheses_parse_at_moderate_depth():
    """Redundant nesting is a different shape from a long chain, and collapses
    away entirely once parsed."""
    expr = "(" * NESTING_DEPTH + "a" + ")" * NESTING_DEPTH
    assert formulate.from_root(expr).to_root() == "a"


def test_deeply_nested_calls_survive_every_walk():
    """Nesting that survives parsing, unlike redundant parentheses: one AST
    level per `sqrt`, so a recursive walk would run out of stack here."""
    parsed = formulate.from_root("sqrt(" * DEEP_NESTING + "a" + ")" * DEEP_NESTING)

    assert str(parsed).count("sqrt") == DEEP_NESTING
    assert parsed.to_python().count("np.sqrt") == DEEP_NESTING
    assert parsed.to_root().count("TMath::Sqrt") == DEEP_NESTING
    assert parsed.variables == {"a"}


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
