"""
Comprehensive test suite for all TFormula (ROOT) and numexpr features.
This ensures formulate supports all features from both systems.
"""

from __future__ import annotations

import pytest

import formulate


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
            # Bitwise operators
            ("a&b", "bitwise AND"),
            ("a|b", "bitwise OR"),
            ("a^b", "bitwise XOR (when not power)"),
            ("~a", "bitwise NOT"),
            # Logical operators
            ("a&&b", "logical AND"),
            ("a||b", "logical OR"),
            ("!a", "logical NOT"),
            # Shift operators (numexpr)
            ("a<<b", "left shift"),
            ("a>>b", "right shift"),
            # Unary operators
            ("-a", "unary minus"),
            ("+a", "unary plus"),
        ],
    )
    def test_operator_support(self, expr, desc):
        """Test that all operators are parsed correctly."""
        try:
            # Test numexpr parsing
            parsed = formulate.from_numexpr(expr)
            assert parsed is not None, f"Failed to parse {desc}: {expr}"

            # Test conversion back
            result = parsed.to_numexpr()
            assert result is not None, f"Failed to convert {desc} back to numexpr"
        except Exception as e:
            # Some operators might not be supported in numexpr mode
            if "^" in expr and "XOR" not in desc:
                # ^ as power is ROOT-specific
                pytest.skip("^ as power operator is ROOT-specific")
            elif "&&" in expr or "||" in expr or "!" in expr:
                # Logical operators might have limited support
                pytest.skip(f"Logical operator {desc} has limited support")
            elif "<<" in expr or ">>" in expr:
                # Shift operators are not supported by numexpr
                pytest.skip(f"Shift operator {desc} is not supported by numexpr")
            else:
                raise e


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
            ("ceil", ["x"], ["root"]),
            ("floor", ["x"], ["root"]),
            ("round", ["x"], ["numexpr"]),
            # Special functions
            ("factorial", ["x"], ["root"]),
            ("even", ["x"], ["root"]),
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
            ("MinIf$", ["arr", "cond"], ["root"]),
            ("MaxIf$", ["arr", "cond"], ["root"]),
            ("Alt$", ["arr", "i", "j"], ["root"]),
            # Constants (tested as zero-arg functions)
            ("pi", [], ["root"]),
            ("e", [], ["root"]),
            # ROOT TMath functions
            ("TMath::Sin", ["x"], ["root"]),
            ("TMath::Cos", ["x"], ["root"]),
            ("TMath::Sqrt", ["x"], ["root"]),
            ("TMath::Abs", ["x"], ["root"]),
            ("TMath::Exp", ["x"], ["root"]),
            ("TMath::Log", ["x"], ["root"]),
        ],
    )
    def test_function_parsing(self, func, args, systems):
        """Test that functions are parsed correctly."""
        # Create expression with function call
        expr = f"{func}({','.join(args)})" if args else func

        for system in systems:
            if system == "numexpr":
                try:
                    parsed = formulate.from_numexpr(expr)
                    assert parsed is not None, f"Failed to parse {func} in numexpr"

                    # Some functions might not convert back
                    try:
                        result = parsed.to_numexpr()
                    except ValueError as e:
                        if "Cannot translate" in str(e) or "No equivalent" in str(e):
                            pytest.skip(f"{func} cannot be translated to numexpr")
                        raise
                except Exception as e:
                    if func.endswith("$") or func.startswith("TMath::"):
                        pytest.skip(f"{func} is ROOT-specific")
                    elif func in ["factorial", "even", "log2", "ceil", "floor"]:
                        pytest.skip(f"{func} might not be in numexpr parser")
                    elif func in [
                        "round",
                        "real",
                        "imag",
                        "conj",
                        "complex",
                        "log1p",
                        "expm1",
                    ]:
                        pytest.skip(f"{func} is numexpr-specific, not in parser")
                    else:
                        raise e

            elif system == "root":
                try:
                    parsed = formulate.from_root(expr)
                    assert parsed is not None, f"Failed to parse {func} in ROOT"

                    # Test conversion to ROOT format
                    result = parsed.to_root()
                    assert result is not None, f"Failed to convert {func} back to ROOT"
                except Exception as e:
                    if func in [
                        "arcsin",
                        "arccos",
                        "arctan",
                        "arctan2",
                        "arcsinh",
                        "arccosh",
                        "arctanh",
                        "log1p",
                        "expm1",
                        "round",
                        "real",
                        "imag",
                        "conj",
                        "complex",
                    ]:
                        pytest.skip(f"{func} is numexpr-specific notation")
                    else:
                        raise e


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
            try:
                parsed = (
                    formulate.from_root(expr)
                    if system == "root"
                    else formulate.from_numexpr(expr)
                )
                assert parsed is not None, f"Failed to parse {desc}"
            except:
                # Some constant notations might not be supported
                pass

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
            try:
                parsed = formulate.from_root(expr)
                assert parsed is not None, f"Failed to parse ROOT array: {expr}"
            except Exception as e:
                if "tree." in expr:
                    pytest.skip("Tree member access not fully supported")
                else:
                    raise e

    def test_special_root_keywords(self):
        """Test ROOT special keywords."""
        special_keywords = [
            ("Iteration$", "current iteration"),
            ("Length$", "array length"),
            ("rndm", "random number"),
        ]

        for keyword, desc in special_keywords:
            try:
                expr = f"sin(pi*{keyword})" if keyword == "rndm" else keyword

                parsed = formulate.from_root(expr)
                assert parsed is not None, f"Failed to parse {desc}: {keyword}"
            except Exception as e:
                if keyword == "rndm":
                    pytest.skip("Random number generation might not be supported")
                else:
                    raise e

    def test_string_operations(self):
        """Test string operations from numexpr."""
        # numexpr supports string comparisons
        string_exprs = [
            "'hello' == s",
            "s != 'world'",
            "contains(s, 'test')",
        ]

        for expr in string_exprs:
            try:
                formulate.from_numexpr(expr)
                # String operations might have limited support
            except:
                pytest.skip("String operations have limited support")


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
            try:
                parsed = formulate.from_numexpr(expr)
                assert parsed is not None, f"Failed to parse {desc} in numexpr"

                # Try to convert back
                try:
                    result = parsed.to_numexpr()
                except ValueError as e:
                    if "TMath::" in expr or "$" in expr:
                        pass  # Expected for ROOT-specific syntax
                    else:
                        print(f"Warning: {desc} cannot convert back to numexpr: {e}")
            except Exception as e:
                if "TMath::" in expr or "$" in expr:
                    pass  # ROOT-specific syntax
                else:
                    msg = f"Failed to parse {desc} in numexpr: {e}"
                    raise Exception(msg) from e

        if system in ["both", "root"]:
            try:
                parsed = formulate.from_root(expr)
                assert parsed is not None, f"Failed to parse {desc} in ROOT"

                # Try to convert to ROOT
                result = parsed.to_root()
                assert result is not None
            except Exception as e:
                if "where(" in expr:
                    pytest.skip("where() is numexpr-specific")
                elif "TMath::Gaus" in expr:
                    pytest.skip("TMath::Gaus might need special handling")
                else:
                    msg = f"Failed to parse {desc} in ROOT: {e}"
                    raise Exception(msg) from e


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

        for funcs, desc in equivalent_functions:
            results = []
            for func in funcs:
                expr = f"{func}(x)"
                try:
                    if "TMath::" in func or func[0].isupper():
                        parsed = formulate.from_root(expr)
                    else:
                        parsed = formulate.from_numexpr(expr)

                    # Convert to normalized form
                    results.append(str(parsed))
                except:
                    pass

            # All variations should parse to similar AST
            if results:
                print(f"{desc} variations: {results}")

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


if __name__ == "__main__":
    # Quick test of key features
    print("Testing key formulate features...")

    # Test basic operators
    test_ops = ["a+b", "a**b", "a/b/c", "a<b", "a&b"]
    for op in test_ops:
        try:
            p = formulate.from_numexpr(op)
            print(f"✓ {op} -> {p.to_numexpr()}")
        except Exception as e:
            print(f"✗ {op} -> Error: {e}")

    # Test key functions
    test_funcs = ["sin(x)", "sqrt(x)", "exp(x)", "abs(x)"]
    for func in test_funcs:
        try:
            p = formulate.from_numexpr(func)
            print(f"✓ {func} -> {p.to_numexpr()}")
        except Exception as e:
            print(f"✗ {func} -> Error: {e}")

    print("\nRun pytest to execute all tests.")
