# Licensed under a 3-clause BSD style license, see LICENSE.
from __future__ import annotations

import sys

import pytest

import formulate
from formulate.cli import main, parse_args


@pytest.mark.parametrize(
    "args,expected",
    [
        (
            ["--from-root", "(A && B) || TMath::Sqrt(A)", "--to-numexpr"],
            "((A & B) | sqrt(A))",
        ),
        (
            ["--from-numexpr", "(A & B) | sqrt(A)", "--to-root"],
            "((A && B) || TMath::Sqrt(A))",
        ),
        (["--from-root", "TMath::Sqrt(A)", "--to-python"], "np.sqrt(A)"),
        (["--from-numexpr", "sqrt(A)", "--to-numexpr"], "sqrt(A)"),
        (["--from-root", "A && B", "--to-root"], "(A && B)"),
    ],
)
def test_conversions(args, expected):
    assert parse_args(args) == expected


@pytest.mark.parametrize(
    "args,expected",
    [
        # --variables
        (
            ["--from-numexpr", "(A & B) | sqrt(A) + 5.4**3.141592 ", "--variables"],
            "A\nB",
        ),
        (
            ["--from-root", "(A && B) || TMath::Sqrt(A) + 5.4**pi", "--variables"],
            "A\nB",
        ),
        (["--from-numexpr", "3.0", "--variables"], ""),
        # --named-constants
        (["--from-numexpr", "(A & B) | sqrt(A)", "--named-constants"], ""),
        (["--from-root", "(A && B) || TMath::Sqrt(A)", "--named-constants"], ""),
        (
            [
                "--from-numexpr",
                "(A & B) | sqrt(A) + 5.4**3.141592",
                "--named-constants",
            ],
            "",
        ),
        (
            [
                "--from-root",
                "(A && B) || TMath::Sqrt(A) + 5.4**pi",
                "--named-constants",
            ],
            "pi",
        ),
        (["--from-root", "pi + TMath::E()", "--named-constants"], "pi\nexp1"),
        # --unnamed-constants
        (["--from-numexpr", "(A & B) | sqrt(A)", "--unnamed-constants"], ""),
        (["--from-root", "(A && B) || TMath::Sqrt(A)", "--unnamed-constants"], ""),
        (
            [
                "--from-numexpr",
                "(A & B) | sqrt(A) + 5.4**3.141592",
                "--unnamed-constants",
            ],
            "5.4\n3.141592",
        ),
        (
            [
                "--from-root",
                "(A && B) || TMath::Sqrt(A) + 5.4**pi",
                "--unnamed-constants",
            ],
            "5.4",
        ),
    ],
)
def test_introspection_options(args, expected):
    assert parse_args(args) == expected


@pytest.mark.parametrize(
    "args",
    [
        ["--dsadasdsada"],
        # Neither side of the conversion may be omitted ...
        ["--to-root"],
        ["--from-root", "A"],
        [],
        # ... nor given twice
        ["--from-root", "A", "--from-numexpr", "A", "--to-root"],
        ["--from-root", "A", "--to-root", "--to-numexpr"],
    ],
)
def test_invalid_argument_combinations_exit(args):
    with pytest.raises(SystemExit):
        parse_args(args)


def test_version_flag_exits_successfully(capsys):
    with pytest.raises(SystemExit) as excinfo:
        parse_args(["--version"])
    assert excinfo.value.code == 0
    assert formulate.__version__ in capsys.readouterr().out


def test_parse_errors_are_not_swallowed():
    with pytest.raises(formulate.ParseError):
        parse_args(["--from-root", "a &", "--to-numexpr"])


def test_main_writes_result_to_stdout(monkeypatch, capsys):
    monkeypatch.setattr(
        sys, "argv", ["formulate", "--from-numexpr", "sqrt(A)", "--to-root"]
    )
    main()
    captured = capsys.readouterr()
    assert captured.out == "TMath::Sqrt(A)\n"
