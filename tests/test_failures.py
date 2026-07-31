"""Error reporting: not just which inputs are rejected, but how helpfully.

Covers the quality of the failure: the exception type, the message, and the
suggestions attached to it.
"""

from __future__ import annotations

import lark
import pytest
from hypothesis import assume, given, settings
from hypothesis import strategies as st

import formulate
from formulate.exceptions import ParseError, _build_parse_error

# --- Semantic errors raised by the AST builder after a successful parse ---


def test_unknown_namespace_raises():
    # Only "tmath" is a recognized namespace; anything else is an error
    with pytest.raises(ValueError, match="Unknown namespace"):
        formulate.from_root("foo::sqrt(a)")


def test_too_many_namespace_parts_raises():
    # A::B::C has three namespace segments, which is not supported
    with pytest.raises(ValueError, match="Unknown function or constant"):
        formulate.from_root("A::B::C(a)")


def test_unknown_function_name_raises():
    # A syntactically valid call to a function formulate does not know
    with pytest.raises(ValueError, match="Unknown function or constant"):
        formulate.from_root("unknownfunc(a)")


def test_constant_called_with_arguments_raises():
    # pi is a constant; calling it like a function is an error
    with pytest.raises(SyntaxError, match="should not have arguments"):
        formulate.from_root("pi(a)")


@pytest.mark.parametrize("keyword", ["class", "lambda", "import", "None", "def"])
def test_python_keyword_as_symbol_raises(keyword):
    # Symbols become Python identifiers downstream, so keywords are rejected
    with pytest.raises(SyntaxError, match="not a valid symbol"):
        formulate.from_root(keyword)


def test_python_keyword_inside_a_dotted_name_raises():
    with pytest.raises(SyntaxError, match="not a valid symbol"):
        formulate.from_root("tree.class")


def test_unknown_dollar_suffix_raises():
    # foo$ ends with $ but "foo" is not a known array function
    with pytest.raises(SyntaxError, match="not a valid symbol"):
        formulate.from_root("foo$")


# --- Parse errors ---


@pytest.mark.parametrize("expr", ["", "   ", "\t\n"])
def test_blank_expressions_are_rejected(expr):
    with pytest.raises(ParseError):
        formulate.from_root(expr)
    with pytest.raises(ParseError):
        formulate.from_numexpr(expr)


@pytest.mark.parametrize(
    "expr",
    [
        pytest.param("a ? b : c", id="ternary-operator"),
        pytest.param("a ?? b", id="null-coalescing-operator"),
        pytest.param("a@b", id="matrix-multiplication-operator"),
        pytest.param("a#b", id="comment-character"),
        pytest.param("a`b", id="backtick"),
        pytest.param("a\\b", id="backslash"),
        pytest.param("a;b", id="statement-separator"),
        pytest.param("a$b", id="bare-dollar-sign"),
    ],
)
def test_unsupported_syntax_is_rejected(expr):
    with pytest.raises(ParseError):
        formulate.from_root(expr)
    with pytest.raises(ParseError):
        formulate.from_numexpr(expr)


def test_parse_error_keeps_the_underlying_lark_error():
    with pytest.raises(ParseError) as excinfo:
        formulate.from_root("a +")
    assert isinstance(excinfo.value.lark_error, lark.LarkError)
    assert excinfo.value.__cause__ is excinfo.value.lark_error


def test_parse_error_points_at_the_offending_location():
    with pytest.raises(ParseError) as excinfo:
        formulate.from_numexpr("a && b")
    message = str(excinfo.value)
    assert "at or near this location" in message
    # get_context() echoes the source with a caret under the bad token
    assert "a && b" in message
    assert "^" in message


def test_parse_error_says_so_when_it_has_no_suggestions():
    with pytest.raises(ParseError, match="No suggestions available"):
        formulate.from_root("a +")


# --- Suggestions ---


@pytest.mark.parametrize(
    "expr,suggestion",
    [
        ("a&b", "Use '&&' instead of '&'."),
        ("a&&b&c", "Use '&&' instead of '&'."),
        ("a|b", "Use '||' instead of '|'."),
        ("a||b|c", "Use '||' instead of '|'."),
        ("~a", "Use '!' instead of '~'."),
        ("(a:b)+c", "':' separates the expressions of a TTree::Draw"),
    ],
)
def test_root_suggestions(expr, suggestion):
    with pytest.raises(ParseError) as excinfo:
        formulate.from_root(expr)
    assert suggestion in str(excinfo.value)


@pytest.mark.parametrize(
    "expr,suggestion",
    [
        ("a && b", "Use '&' instead of '&&' or 'and'."),
        ("a and b", "Use '&' instead of '&&' or 'and'."),
        ("a || b", "Use '|' instead of '||' or 'or'."),
        ("a or b", "Use '|' instead of '||' or 'or'."),
        ("!a", "Use '~' instead of '!'."),
        ("a < b < c", "chained comparisons"),
    ],
)
def test_numexpr_suggestions(expr, suggestion):
    with pytest.raises(ParseError) as excinfo:
        formulate.from_numexpr(expr)
    assert suggestion in str(excinfo.value)


def test_namespace_colons_do_not_trigger_the_multi_out_suggestion():
    """'TMath::' is two colons, not the ':' separator, so a failure that merely
    mentions a namespace must not be blamed on multi-output syntax."""
    with pytest.raises(ParseError) as excinfo:
        formulate.from_root("TMath::Sqrt(x")
    assert "TTree::Draw" not in str(excinfo.value)


def test_not_equal_does_not_trigger_the_bang_suggestion():
    """'!=' contains a '!' but is perfectly valid, so suggesting '~' would be
    misleading."""
    with pytest.raises(ParseError) as excinfo:
        formulate.from_numexpr("a != ")
    assert "Use '~' instead of '!'." not in str(excinfo.value)


def test_several_suggestions_are_reported_together():
    with pytest.raises(ParseError) as excinfo:
        formulate.from_root("a & b | c")
    message = str(excinfo.value)
    assert "Use '&&' instead of '&'." in message
    assert "Use '||' instead of '|'." in message


def test_build_parse_error_without_unexpected_input():
    # When the lark error is not an UnexpectedInput subclass, _build_parse_error
    # should still produce a valid ParseError (just without the location context).
    error = lark.LarkError("some error")
    result = _build_parse_error("a + b", error, ["- Try this fix"])
    assert isinstance(result, ParseError)
    assert "- Try this fix" in str(result)
    assert "at or near" not in str(result)


# --- Fuzzing ---


@given(st.text(alphabet=st.characters(blacklist_categories=("L", "N")), min_size=1))
@settings(max_examples=1000)
def test_invalid_characters(s):
    """Text made only of punctuation should never parse."""
    # Skip strings that contain only whitespace or valid operators
    assume(not s.isspace())
    assume(not all(c in "+-*/()<>=!&|^~_\r " for c in s))  # TODO: why does _ not fail?

    with pytest.raises(ParseError):
        formulate.from_root(s)

    with pytest.raises(ParseError):
        formulate.from_numexpr(s)


@given(
    st.text(alphabet="(", min_size=1, max_size=10),
    st.text(alphabet=")", min_size=0, max_size=9),
)
@settings(max_examples=1000)
def test_unbalanced_parentheses(open_parens, close_parens):
    """Expressions with more '(' than ')' are always rejected."""
    assume(len(open_parens) > len(close_parens))

    expr = "a" + open_parens + "+b" + close_parens

    with pytest.raises(ParseError):
        formulate.from_root(expr)

    with pytest.raises(ParseError):
        formulate.from_numexpr(expr)
