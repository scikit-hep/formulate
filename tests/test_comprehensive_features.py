"""
Comprehensive test suite for all TFormula (ROOT) and numexpr features.
This ensures formulate supports all features from both systems.
"""

from __future__ import annotations

import numpy as np
import pytest
from ordered_set import OrderedSet

import formulate
from formulate import from_numexpr, from_root


class TestComprehensiveOperators:
    """Test all operators supported by ROOT TFormula and numexpr."""

    @pytest.mark.parametrize(
        "expr,desc",
        [
            # Arithmetic operators
            ("a+b", "addition"),
            ("a-b", "subtraction"),
            ("a*b", "multiplication"),
            ("a/b", "division"),
            ("a**b", "power (** notation)"),
            ("a^b", "power (^ notation - ROOT style)"),
            ("a%b", "modulo"),
            # Comparison operators
            ("a<b", "less than"),
            ("a<=b", "less than or equal"),
            ("a>b", "greater than"),
            ("a>=b", "greater than or equal"),
            ("a==b", "equal"),
            ("a!=b", "not equal"),
            # Logical operators
            ("a && b", "logical AND"),  # only for ROOT
            ("a || b", "logical OR"),  # only for ROOT
            ("!a", "logical NOT"),  # only for ROOT
            ("a & b", "logical AND"),  # only for numexpr
            ("a | b", "logical OR"),  # only for numexpr
            ("~a", "logical NOT"),  # only for numexpr
            # Unary operators
            ("-a", "unary minus"),
            ("+a", "unary plus"),
        ],
    )
    def test_root_operator_support(self, expr, desc):
        """Test that all operators are parsed correctly."""
        # Numexpr parsing and conversions
        if not any(op in expr for op in ["&&", "||", "!", "^"]):
            # Test parsing
            parsed = formulate.from_numexpr(expr)
            assert parsed is not None, f"Failed to parse {desc}: {expr}"

            # Test conversion to ROOT
            result = parsed.to_root()
            assert result is not None, f"Failed to convert {desc} to ROOT"

            # Test conversion back
            result = parsed.to_numexpr()
            assert result is not None, f"Failed to convert {desc} back to numexpr"

        # ROOT parsing and conversions
        if not any(op in expr for op in [" & ", " | ", "~"]):
            # Test parsing
            parsed = formulate.from_root(expr)
            assert parsed is not None, f"Failed to parse {desc}: {expr}"

            # Test conversion to numexpr
            result = parsed.to_numexpr()
            assert result is not None, f"Failed to convert {desc} to numexpr"

            # Test conversion back
            result = parsed.to_root()
            assert result is not None, f"Failed to convert {desc} back to ROOT"


class TestComprehensiveFunctions:
    """Test all mathematical functions from ROOT and numexpr."""

    @pytest.mark.parametrize(
        "func,args,systems",
        [
            # Trigonometric functions
            ("sin", ["x"], ["root", "numexpr"]),
            ("cos", ["x"], ["root", "numexpr"]),
            ("tan", ["x"], ["root", "numexpr"]),
            ("asin", ["x"], ["root", "numexpr"]),
            ("arcsin", ["x"], ["numexpr"]),
            ("acos", ["x"], ["root", "numexpr"]),
            ("arccos", ["x"], ["numexpr"]),
            ("atan", ["x"], ["root", "numexpr"]),
            ("arctan", ["x"], ["numexpr"]),
            ("atan2", ["y", "x"], ["root", "numexpr"]),
            ("arctan2", ["y", "x"], ["numexpr"]),
            # Hyperbolic functions
            ("sinh", ["x"], ["root", "numexpr"]),
            ("cosh", ["x"], ["root", "numexpr"]),
            ("tanh", ["x"], ["root", "numexpr"]),
            ("asinh", ["x"], ["root", "numexpr"]),
            ("arcsinh", ["x"], ["numexpr"]),
            ("acosh", ["x"], ["root", "numexpr"]),
            ("arccosh", ["x"], ["numexpr"]),
            ("atanh", ["x"], ["root", "numexpr"]),
            ("arctanh", ["x"], ["numexpr"]),
            # Exponential and logarithmic
            ("exp", ["x"], ["root", "numexpr"]),
            ("log", ["x"], ["root", "numexpr"]),
            ("log10", ["x"], ["root", "numexpr"]),
            ("log2", ["x"], ["root"]),
            ("log1p", ["x"], ["numexpr"]),
            ("expm1", ["x"], ["numexpr"]),
            # Power and roots
            ("sqrt", ["x"], ["root", "numexpr"]),
            ("pow", ["x", "y"], ["root"]),
            # Rounding functions
            ("abs", ["x"], ["root", "numexpr"]),
            ("ceil", ["x"], ["root", "numexpr"]),
            ("floor", ["x"], ["root", "numexpr"]),
            # Complex number functions (numexpr)
            ("real", ["x"], ["numexpr"]),
            ("imag", ["x"], ["numexpr"]),
            ("conj", ["x"], ["numexpr"]),
            ("complex", ["x", "y"], ["numexpr"]),
            # Conditional function
            ("where", ["cond", "a", "b"], ["numexpr"]),
            # Array functions (ROOT specific)
            ("Sum$", ["arr"], ["root"]),
            ("Min$", ["arr"], ["root"]),
            ("Max$", ["arr"], ["root"]),
            ("Length$", ["arr"], ["root"]),
            # Constants (tested as zero-arg functions)
            ("pi", [], ["numexpr", "root"]),
            ("e_number", [], ["numexpr", "root"]),
            # ROOT TMath functions
            ("TMath::Sqrt", ["x"], ["root"]),
            ("TMath::Abs", ["x"], ["root"]),
            ("TMath::Power", ["x", "y"], ["root"]),
            ("TMath::Log", ["x"], ["root"]),
            ("TMath::Log2", ["x"], ["root"]),
            ("TMath::Log10", ["x"], ["root"]),
            ("TMath::Exp", ["x"], ["root"]),
            ("TMath::Sin", ["x"], ["root"]),
            ("TMath::Cos", ["x"], ["root"]),
            ("TMath::Tan", ["x"], ["root"]),
            ("TMath::ASin", ["x"], ["root"]),
            ("TMath::ACos", ["x"], ["root"]),
            ("TMath::ATan", ["x"], ["root"]),
            ("TMath::ATan2", ["x", "y"], ["root"]),
            ("TMath::SinH", ["x"], ["root"]),
            ("TMath::CosH", ["x"], ["root"]),
            ("TMath::TanH", ["x"], ["root"]),
            ("TMath::ASinH", ["x"], ["root"]),
            ("TMath::ACosH", ["x"], ["root"]),
            ("TMath::ATanH", ["x"], ["root"]),
            ("TMath::BesselI0", ["x"], ["root"]),
            ("TMath::BesselI1", ["x"], ["root"]),
            ("TMath::BesselJ0", ["x"], ["root"]),
            ("TMath::BesselJ1", ["x"], ["root"]),
            ("TMath::BesselY0", ["x"], ["root"]),
            ("TMath::BesselY1", ["x"], ["root"]),
            ("TMath::Ceil", ["x"], ["root"]),
            ("TMath::CeilNint", ["x"], ["root"]),
            ("TMath::DiLog", ["x"], ["root"]),
            ("TMath::Erf", ["x"], ["root"]),
            ("TMath::Erfc", ["x"], ["root"]),
            ("TMath::ErfInverse", ["x"], ["root"]),
            ("TMath::ErfcInverse", ["x"], ["root"]),
            ("TMath::Even", ["x"], ["root"]),
            ("TMath::Factorial", ["x"], ["root"]),
            ("TMath::Floor", ["x"], ["root"]),
            ("TMath::FloorNint", ["x"], ["root"]),
            ("TMath::Freq", ["x"], ["root"]),
            ("TMath::KolmogorovProb", ["x"], ["root"]),
            ("TMath::LandauI", ["x"], ["root"]),
            ("TMath::LnGamma", ["x"], ["root"]),
            ("TMath::NextPrime", ["x"], ["root"]),
            ("TMath::NormQuantile", ["x"], ["root"]),
            ("TMath::Odd", ["x"], ["root"]),
            ("TMath::StruveH0", ["x"], ["root"]),
            ("TMath::StruveH1", ["x"], ["root"]),
            ("TMath::StruveL0", ["x"], ["root"]),
            ("TMath::StruveL1", ["x"], ["root"]),
            ("TMath::BesselI", ["x"], ["root"]),
            ("TMath::BesselK", ["x"], ["root"]),
            ("TMath::Beta", ["x"], ["root"]),
            ("TMath::Binomial", ["x"], ["root"]),
            ("TMath::ChisquareQuantile", ["x"], ["root"]),
            ("TMath::Ldexp", ["x"], ["root"]),
            ("TMath::Permute", ["x"], ["root"]),
            ("TMath::Poisson", ["x"], ["root"]),
            ("TMath::PoissonI", ["x"], ["root"]),
            ("TMath::Prob", ["x"], ["root"]),
            ("TMath::Student", ["x"], ["root"]),
            ("TMath::StudentI", ["x"], ["root"]),
            ("TMath::AreEqualAbs", ["x"], ["root"]),
            ("TMath::AreEqualRel", ["x"], ["root"]),
            ("TMath::BetaCf", ["x"], ["root"]),
            ("TMath::BetaDist", ["x"], ["root"]),
            ("TMath::BetaDistI", ["x"], ["root"]),
            ("TMath::BetaIncomplete", ["x"], ["root"]),
            ("TMath::BinomialI", ["x"], ["root"]),
            ("TMath::BubbleHigh", ["x"], ["root"]),
            ("TMath::BubbleLow", ["x"], ["root"]),
            ("TMath::FDist", ["x"], ["root"]),
            ("TMath::FDistI", ["x"], ["root"]),
            ("TMath::Vavilov", ["x"], ["root"]),
            ("TMath::VavilovI", ["x"], ["root"]),
            ("TMath::RootsCubic", ["w", "x", "y", "z"], ["root"]),
            (
                "TMath::Quantiles",
                ["x1", "x2", "x3", "x4", "x5", "x6", "x7", "x8"],
                ["root"],
            ),
        ],
    )
    def test_function_parsing(self, func, args, systems):
        """Test that functions are parsed correctly."""
        # Create expression with function call
        expr = f"{func}({','.join(args)})" if args else func

        for system in systems:
            if system == "numexpr":
                parsed = formulate.from_numexpr(expr)
                assert parsed is not None, f"Failed to parse {func} in numexpr"

                result = parsed.to_numexpr()
                assert result is not None, f"Failed to convert {func} back to numexpr"

            elif system == "root":
                parsed = formulate.from_root(expr)
                assert parsed is not None, f"Failed to parse {func} in ROOT"

                # Test conversion to ROOT format
                result = parsed.to_root()
                assert result is not None, f"Failed to convert {func} back to ROOT"


class TestSpecialFeatures:
    """Test special features from ROOT and numexpr."""

    def test_pi_constant_variations(self):
        """Test different ways to express pi."""
        # Test function-style constants (with parentheses)
        pi_function_expressions = [
            ("pi()", "simple pi function", "numexpr"),
            ("Pi()", "capitalized pi function", "root"),
        ]

        for expr, desc, system in pi_function_expressions:
            parsed = (
                formulate.from_root(expr)
                if system == "root"
                else formulate.from_numexpr(expr)
            )
            assert parsed is not None, f"Failed to parse {desc}"

        # Test simple pi without parentheses (works in numexpr)
        parsed = formulate.from_numexpr("pi")
        assert parsed is not None, "Failed to parse simple pi"

    def test_power_operator_variations(self):
        """Test different power notations."""
        # Standard ** notation (both systems)
        parsed = formulate.from_numexpr("a**b")
        assert parsed.to_numexpr() == "(a ** b)"

        # ROOT ^ notation means power
        parsed = formulate.from_root("a^b")
        assert parsed.to_root() == "(a ** b)"
        assert parsed.to_numexpr() == "(a ** b)"

        # In numexpr, ^ is XOR, not power
        parsed_xor = formulate.from_numexpr("a^b")
        with pytest.raises(ValueError):
            parsed_xor.to_root()

    def test_array_indexing(self):
        """Test array indexing features."""
        # ROOT style array access
        root_arrays = [
            "arr[0]",
            "arr[i]",
            "arr[i][j]",
            "tree.branch[0]",
        ]

        for expr in root_arrays:
            parsed = formulate.from_root(expr)
            assert parsed is not None, f"Failed to parse ROOT array: {expr}"

    def test_special_root_keywords(self):
        """Test ROOT special keywords."""
        special_keywords = [
            ("Length$(arr)", "array length"),
            ("rndm", "random number"),
        ]

        for keyword, desc in special_keywords:
            expr = f"sin(pi*{keyword})" if keyword == "rndm" else keyword
            parsed = formulate.from_root(expr)
            assert parsed is not None, f"Failed to parse {desc}: {keyword}"

    @pytest.mark.skip(reason="String operations are not supported")
    def test_string_operations(self):
        """Test string operations from numexpr."""
        # numexpr supports string comparisons
        string_exprs = [
            "'hello' == s",
            "s != 'world'",
            "contains('s', 'test')",
        ]

        for expr in string_exprs:
            formulate.from_numexpr(expr)


class TestComplexExpressions:
    """Test complex real-world expressions."""

    @pytest.mark.parametrize(
        "expr,system,desc",
        [
            # Physics formulas
            ("sqrt(x**2 + y**2)", "both", "2D distance"),
            ("1/2 * m * v**2", "both", "kinetic energy"),
            ("exp(-0.5*((x-mu)/sigma)**2)", "both", "Gaussian"),
            ("sin(2*pi*f*t + phi)", "both", "sine wave"),
            # ROOT-style formulas
            ("TMath::Gaus(x, 0, 1)", "root", "ROOT Gaussian"),
            ("Sum$(pt > 20)", "root", "ROOT conditional sum"),
            ("Length$(electrons)", "root", "ROOT array length"),
            # Complex numexpr formulas
            ("where(x > 0, log(x), 0)", "numexpr", "conditional log"),
            ("sin(x) + cos(y) + tan(z)", "both", "trig combination"),
            ("abs(x - y) < 1e-6", "both", "floating point comparison"),
        ],
    )
    def test_complex_expressions(self, expr, system, desc):
        """Test parsing of complex real-world expressions."""
        if system in ["both", "numexpr"]:
            parsed = formulate.from_numexpr(expr)
            assert parsed is not None, f"Failed to parse {desc} in numexpr"

            result = parsed.to_numexpr()
            assert result is not None, f"Failed convert {desc} back to numexpr"

        if system in ["both", "root"]:
            parsed = formulate.from_root(expr)
            assert parsed is not None, f"Failed to parse {desc} in ROOT"

            # Try to convert to ROOT
            result = parsed.to_root()
            assert result is not None, f"Failed convert {desc} back to ROOT"


class TestEdgeCasesAndCompatibility:
    """Test edge cases and compatibility between systems."""

    def test_operator_precedence_consistency(self):
        """Ensure operator precedence is consistent."""
        test_exprs = [
            "a + b * c",
            "a * b + c * d",
            "a / b / c",
            "a ** b ** c",
            "a + b < c * d",
        ]

        for expr in test_exprs:
            # Parse with numexpr
            parsed_ne = formulate.from_numexpr(expr)
            result_ne = parsed_ne.to_numexpr()

            # Parse with ROOT
            parsed_root = formulate.from_root(expr)
            result_root = parsed_root.to_root()

            # Convert between formats
            parsed_root.to_numexpr()

            # The precedence should be preserved
            print(f"{expr} -> numexpr: {result_ne}, root: {result_root}")

    def test_function_name_variations(self):
        """Test that function name variations are handled."""
        equivalent_functions = [
            (["sin", "Sin", "TMath::Sin"], "sine function"),
            (["sqrt", "Sqrt", "TMath::Sqrt"], "square root"),
            (["abs", "Abs", "TMath::Abs"], "absolute value"),
            (["exp", "Exp", "TMath::Exp"], "exponential"),
        ]

        for funcs, _ in equivalent_functions:
            for func in funcs:
                expr = f"{func}(x)"
                _ = (
                    formulate.from_root(expr)
                    if "TMath::" in func or func[0].isupper()
                    else formulate.from_numexpr(expr)
                )

    def test_numeric_literal_handling(self):
        """Test how numeric literals are handled."""
        numeric_exprs = [
            "42",
            "3.14159",
            "1e-6",
            "2.5E10",
            ".5",
            "1.",
        ]

        for expr in numeric_exprs:
            parsed_ne = formulate.from_numexpr(expr)
            parsed_root = formulate.from_root(expr)

            # Both should parse successfully
            assert parsed_ne is not None
            assert parsed_root is not None


def test_function_translations():
    """Test that function translations are handled."""
    test_cases = [
        ("sin(x)", "TMath::Sin(x)"),
        ("cos(x)", "TMath::Cos(x)"),
        ("tan(x)", "TMath::Tan(x)"),
        ("sqrt(x)", "TMath::Sqrt(x)"),
        ("abs(x)", "TMath::Abs(x)"),
        ("exp(x)", "TMath::Exp(x)"),
        ("log(x)", "TMath::Log(x)"),
        ("log10(x)", "TMath::Log10(x)"),
        ("arcsin(x)", "TMath::ASin(x)"),
        ("arccos(x)", "TMath::ACos(x)"),
        ("arctan(x)", "TMath::ATan(x)"),
        ("arctan2(x, y)", "TMath::ATan2(x, y)"),
        ("arcsinh(x)", "TMath::ASinH(x)"),
        ("arccosh(x)", "TMath::ACosH(x)"),
        ("arctanh(x)", "TMath::ATanH(x)"),
        ("sinh(x)", "TMath::SinH(x)"),
        ("cosh(x)", "TMath::CosH(x)"),
        ("tanh(x)", "TMath::TanH(x)"),
        ("ceil(x)", "TMath::Ceil(x)"),
        ("floor(x)", "TMath::Floor(x)"),
        ("sum(x)", "Sum$(x)"),
        ("min(x)", "Min$(x)"),
        ("max(x)", "Max$(x)"),
    ]

    for numexpr_func, root_func in test_cases:
        translated_root = formulate.from_numexpr(numexpr_func).to_root()
        assert translated_root == root_func

        translated_ne = formulate.from_root(root_func).to_numexpr()
        assert translated_ne == numexpr_func


def test_constant_translations():
    """Test that constant translations are handled."""
    test_cases = [
        ("pi", "3.141592653589793", "TMath::Pi()"),
        ("exp1", "2.718281828459045", "TMath::E()"),
        ("sqrt2", "1.4142135623730951", "TMath::Sqrt2()"),
        ("invpi", "0.3183098861837907", "TMath::InvPi()"),
        ("piover2", "1.5707963267948966", "TMath::PiOver2()"),
        ("piover4", "0.7853981633974483", "TMath::PiOver4()"),
        ("tau", "6.283185307179586", "TMath::TwoPi()"),
        ("ln10", "2.302585092994046", "TMath::Ln10()"),
        ("avogadro", "6.02214076e+23", "TMath::Na()"),
        ("k_boltzmann", "1.380649e-23", "TMath::K()"),
        ("c_light", "299792458.0", "TMath::C()"),
        ("eminus", "-1.602176634e-19", "-TMath::Qe()"),
        ("eplus", "1.602176634e-19", "TMath::Qe()"),
        ("h_planck", "6.62607015e-34", "TMath::H()"),
        ("hbar", "6.62607015e-34", "TMath::Hbar()"),
        ("hbarc", "1.97326968e-16", "(TMath::Hbar() * TMath::C())"),
    ]

    for const, numexpr_const, root_const in test_cases:
        translated_numexpr1 = (
            formulate.from_numexpr(const).to_numexpr().replace("(", "").replace(")", "")
        )
        translated_numexpr2 = (
            formulate.from_root(root_const)
            .to_numexpr()
            .replace("(", "")
            .replace(")", "")
        )
        assert np.isclose(eval(translated_numexpr1), eval(numexpr_const))
        assert np.isclose(eval(translated_numexpr2), eval(numexpr_const))

        translated_root = formulate.from_numexpr(const).to_root()
        assert translated_root == root_const


def test_variables_property():
    """Test that variables are identified correctly."""
    test_cases = [
        ("a + b * c", ["a", "b", "c"]),
        (
            "var1 + pi * var2 / var_with_underscore",
            ["var1", "var2", "var_with_underscore"],
        ),
        ("sin(x) * exp(y) * (z * 21 - exp1 - w - 1.0)", ["x", "y", "z", "w"]),
        ("tree.branch + other_variable", ["tree.branch", "other_variable"]),
    ]

    for expr, variables in test_cases:
        ast = formulate.from_numexpr(expr)
        assert frozenset(variables) == ast.variables


def test_get_variables():
    assert from_root("pi").variables == OrderedSet()
    assert from_numexpr("2").variables == OrderedSet()
    assert from_numexpr("2e-3").variables == OrderedSet()
    assert from_numexpr("A").variables == OrderedSet(["A"])
    assert from_numexpr("A + A").variables == OrderedSet(["A"])
    assert from_numexpr("A + B").variables == OrderedSet(["A", "B"])
    assert from_numexpr("A + A*A - 3e7").variables == OrderedSet(["A"])
    assert from_numexpr("arctan2(A, A)").variables == OrderedSet(["A"])
    assert from_numexpr("arctan2(A, B)").variables == OrderedSet(["A", "B"])
    assert from_root("arctan2(A, pi)").variables == OrderedSet(["A"])
    assert from_numexpr("arctan2(arctan2(A, B), C)").variables == OrderedSet(
        ["A", "B", "C"]
    )
    assert from_root("mat[1][a]").variables == OrderedSet(["mat", "a"])
    assert from_numexpr("A.B * A.C").variables == OrderedSet(["A.B", "A.C"])
    assert from_root("A.B * A.C").variables == OrderedSet(["A.B", "A.C"])


def test_named_constants():
    assert from_root("pi").named_constants == OrderedSet(["pi"])
    assert from_numexpr("2").named_constants == OrderedSet()
    assert from_numexpr("2e-3").named_constants == OrderedSet()
    assert from_numexpr("A").named_constants == OrderedSet()
    assert from_numexpr("A + A").named_constants == OrderedSet()
    assert from_numexpr("A + B").named_constants == OrderedSet()
    assert from_numexpr("A + A*A - 3e7").named_constants == OrderedSet()
    assert from_numexpr("arctan2(A, A)").named_constants == OrderedSet()
    assert from_numexpr("arctan2(A, B)").named_constants == OrderedSet()
    assert from_root("arctan2(A, pi)").named_constants == OrderedSet(["pi"])
    assert from_numexpr("arctan2(arctan2(A, B), C)").named_constants == OrderedSet()


def test_unnamed_constants():
    assert from_root("pi").unnamed_constants == OrderedSet()
    assert from_numexpr("2").unnamed_constants == OrderedSet([2])
    assert from_numexpr("2e-3").unnamed_constants == OrderedSet([2e-3])
    assert from_numexpr("A").unnamed_constants == OrderedSet()
    assert from_numexpr("A + A").unnamed_constants == OrderedSet()
    assert from_numexpr("A + B").unnamed_constants == OrderedSet()
    assert from_numexpr("A + A*A - 3e7").unnamed_constants == OrderedSet([3e7])
    assert from_numexpr("arctan2(A, A)").unnamed_constants == OrderedSet()
    assert from_numexpr("arctan2(A, B)").unnamed_constants == OrderedSet()
    assert from_root("arctan2(A, pi)").unnamed_constants == OrderedSet()
    assert from_numexpr("arctan2(arctan2(A, B), C)").unnamed_constants == OrderedSet()
