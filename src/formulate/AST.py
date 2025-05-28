# Licensed under a 3-clause BSD style license, see LICENSE.

from __future__ import annotations

import hashlib
from abc import ABCMeta, abstractmethod
from dataclasses import dataclass

# Try to import ROOT, but don't fail if it's not available
try:
    import ROOT

    HAS_ROOT = True
except ImportError:
    HAS_ROOT = False


class AST(metaclass=ABCMeta):  # only three types (and a superclass to set them up)
    _fields = ()

    @abstractmethod
    def __str__(self):
        raise NotImplementedError(
            "__str__() not implemented, subclass must implement it"
        )

    @abstractmethod
    def to_numexpr(self):
        raise NotImplementedError(
            "to_numexpr() not implemented, subclass must implement it"
        )

    @abstractmethod
    def to_root(self):
        raise NotImplementedError(
            "to_root() not implemented, subclass must implement it"
        )

    def validate_root_formula(self, variables=None):
        """
        Validate if the ROOT formula is valid by attempting to compile it.

        Args:
            variables (dict, optional): Dictionary of variable names and values for evaluation.
                                       Defaults to None.

        Returns:
            bool: True if the formula is valid, False otherwise.
        """
        if not HAS_ROOT:
            return None  # ROOT not available

        try:
            root_expr = self.to_root()

            # Create variable declarations
            var_declarations = ""
            if variables:
                for name, value in variables.items():
                    var_declarations += f"double {name} = {value};\n"

            # Create a temporary C++ function
            func_name = f"TFormula____id{abs(hash(root_expr))}"
            cpp_code = f"""
            #include <TMath.h>
            double {func_name}() {{
                {var_declarations}
                return {root_expr};
            }}
            """

            # Compile the function
            ROOT.gInterpreter.Declare(cpp_code)

            # Try to call the function
            getattr(ROOT, func_name)()
            return True
        except Exception as e:
            print(f"ROOT validation error: {e}")
            return False

    def evaluate_root(self, variables=None):
        """
        Evaluate the ROOT formula with the given variables.

        Args:
            variables (dict, optional): Dictionary of variable names and values for evaluation.
                                       Defaults to None.

        Returns:
            float: The result of evaluating the formula, or None if ROOT is not available
                  or the formula is invalid.
        """
        if not HAS_ROOT:
            raise ImportError(
                "ROOT is not available or cannot be imported. Please install ROOT to use this feature."
            )

        # Validate the formula first
        if not self.validate_root_formula(variables):
            return None  # Invalid formula

        try:
            root_expr = self.to_root()

            # Create variable declarations
            var_declarations = ""
            if variables:
                for name, value in variables.items():
                    var_declarations += f"double {name} = {value};\n"

            # Create a temporary C++ function
            hashable_string = root_expr + var_declarations
            m = hashlib.sha256()
            m.update(hashable_string.encode())

            func_name = f"TFormula____eval_id{m.hexdigest()}"
            cpp_code = f"""
            #include <TMath.h>
            double {func_name}() {{
                {var_declarations}
                return {root_expr};
            }}
            """

            # Compile the function
            ROOT.gInterpreter.Declare(cpp_code)

            # Call the function
            result = getattr(ROOT, func_name)()
            return result
        except Exception as e:
            raise ValueError(f"ROOT evaluation error: {e}") from e
            # print(f"ROOT evaluation error: {e}")
            # return None  # Error during evaluation

    @abstractmethod
    def to_python(self):
        raise NotImplementedError(
            "to_python() not implemented, subclass must implement it"
        )


@dataclass
class Literal(AST):  # Literal: value that appears in the program text
    value: float
    index: int = None

    def __str__(self):
        return str(self.value)

    def to_numexpr(self):
        return repr(self.value)

    def to_root(self):
        return repr(self.value)

    def to_python(self):
        return repr(self.value)


@dataclass
class Symbol(AST):  # Symbol: value referenced by name
    symbol: str
    index: int = None

    def __str__(self):
        return self.symbol

    # def check_CNAME(self):
    #     regex = "((\.)\2{2,})"
    #     x = re.search(regex, self.symbol)
    #     print(x)
    #     return x

    def to_numexpr(self):
        return self.symbol

    def to_root(self):
        # ROOT uses TMath::Power() for exponentiation, not **
        return self.symbol

    def to_python(self):
        return self.symbol


@dataclass
class UnaryOperator(AST):  # Unary Operator: Operation with one operand
    sign: Symbol
    operand: Literal
    index: int = None

    def __str__(self):
        return f"{self.sign!s}({self.operand})"

    def unary_to_ufunc(self, sign):
        signmap = {"~": "np.invert", "!": "np.logical_not"}
        return signmap[str(sign)]

    def to_numexpr(self):
        return "(" + self.sign.to_root() + self.operand.to_numexpr() + ")"

    def to_root(self):
        return "(" + self.sign.to_root() + self.operand.to_root() + ")"

    def to_python(self):
        if str(self.sign) in {"~", "!"}:
            pycode = (
                self.unary_to_ufunc(self.sign)
                + "("
                + str(self.operand.to_python())
                + ")"
            )
        else:
            pycode = (
                "(" + str(self.sign.to_python()) + str(self.operand.to_python()) + ")"
            )
        return pycode


@dataclass
class BinaryOperator(AST):  # Binary Operator: Operation with two operands
    sign: Symbol
    left: AST
    right: AST
    index: int = None

    def __str__(self):
        return f"{self.sign!s}({self.left},{self.right})"

    def binary_to_ufunc(self, sign):
        sign_mapping = {
            "&": "np.bitwise_and",
            "|": "np.bitwise_or",
            "&&": "and",
            "||": "or",
        }
        return sign_mapping[str(sign)]

    def _is_complex_expression(self):
        """Check if this binary operator needs special parenthesis handling"""
        # Check if this is a bitwise/logical operator inside multiplication/division
        if str(self.sign) in {"&", "|", "&&", "||"}:
            parent_op = getattr(self, "_parent_op", None)
            if parent_op and str(parent_op) in {"/", "*"}:
                return True

        # Check if this is multiplication/division with bitwise/logical right operand
        if str(self.sign) in {"/", "*"}:
            if isinstance(self.right, BinaryOperator) and str(self.right.sign) in {
                "&",
                "|",
                "&&",
                "||",
            }:
                # Set a flag on the right operand to indicate it's part of a complex expression
                self.right._parent_op = self.sign
                return True

        return False

    def _strip_parentheses(self, code):
        """Remove outer parentheses if present"""
        if code.startswith("(") and code.endswith(")"):
            return code[1:-1]
        return code

    def _format_bitwise_logical(self, left_code, right_code):
        """Format bitwise/logical operations with smart parenthesis removal"""
        # If left operand is the same operator, remove its parentheses
        if isinstance(self.left, BinaryOperator) and str(self.left.sign) == str(
            self.sign
        ):
            left_code = self._strip_parentheses(left_code)

        # Remove parentheses from right operand if it's simple
        right_code = self._strip_parentheses(right_code)

        return left_code, right_code

    def _to_infix_format(self, method_name):
        """Common logic for to_numexpr and to_root methods"""
        is_complex = self._is_complex_expression()

        if str(self.sign) in {"&", "|", "&&", "||"} and not is_complex:
            # For standalone bitwise and logical operators, don't add extra parentheses
            left_code = getattr(self.left, method_name)()
            right_code = getattr(self.right, method_name)()

            # Format operands
            left_code, right_code = self._format_bitwise_logical(left_code, right_code)

            # Get operator string
            operator_str = str(getattr(self.sign, method_name)())

            return left_code + operator_str + right_code
        # For other operators or complex expressions, keep the parentheses
        left_code = getattr(self.left, method_name)()
        right_code = getattr(self.right, method_name)()
        operator_str = str(getattr(self.sign, method_name)())

        return "(" + left_code + operator_str + right_code + ")"

    def to_numexpr(self):
        return self._to_infix_format("to_numexpr")

    def _get_operator_precedence(self, op):
        """
        Get the operator precedence in C++ (ROOT).
        Lower numbers indicate higher precedence.
        """
        # C++ operator precedence (simplified for our needs)
        precedence = {
            "**": 2,  # Power (not a C++ operator, but we handle it specially)
            "*": 5,  # Multiplication
            "/": 5,  # Division
            "%": 5,  # Modulo
            "+": 6,  # Addition
            "-": 6,  # Subtraction
            "<": 8,  # Less than
            "<=": 8,  # Less than or equal
            ">": 8,  # Greater than
            ">=": 8,  # Greater than or equal
            "==": 9,  # Equal
            "!=": 9,  # Not equal
            "&": 10,  # Bitwise AND
            "^": 11,  # Bitwise XOR
            "|": 12,  # Bitwise OR
            "&&": 13,  # Logical AND
            "||": 14,  # Logical OR
        }
        return precedence.get(op, 99)  # Default to lowest precedence if unknown

    def _is_parenthesized_expression(self, expr_str):
        """
        Check if the expression string is already properly parenthesized.
        """
        if not (expr_str.startswith("(") and expr_str.endswith(")")):
            return False

        # Count opening and closing parentheses
        open_count = 0
        for i, char in enumerate(expr_str):
            if char == "(":
                open_count += 1
            elif char == ")":
                open_count -= 1
                # If we reach 0 before the end, it's not fully parenthesized
                if open_count == 0 and i < len(expr_str) - 1:
                    return False

        return True

    def to_root(self):
        # Special handling for power operator in ROOT
        if str(self.sign) == "**":
            left_code = self.left.to_root()
            right_code = self.right.to_root()

            # Remove outer parentheses from operands to avoid double parentheses
            if left_code.startswith("(") and left_code.endswith(")"):
                left_code = left_code[1:-1]
            if right_code.startswith("(") and right_code.endswith(")"):
                right_code = right_code[1:-1]

            return f"TMath::Power({left_code},{right_code})"

        # Get the current operator and its precedence
        current_op = str(self.sign)
        current_precedence = self._get_operator_precedence(current_op)

        # Get the left and right operands
        left_code = self.left.to_root()
        right_code = self.right.to_root()

        # Check if left operand needs parentheses
        if isinstance(self.left, BinaryOperator):
            left_op = str(self.left.sign)
            left_precedence = self._get_operator_precedence(left_op)

            # Add parentheses if left operator has lower precedence
            # or if they have the same precedence but the operation is not associative
            if left_precedence > current_precedence or (
                left_precedence == current_precedence and current_op in {"-", "/", "%"}
            ):
                if not self._is_parenthesized_expression(left_code):
                    left_code = "(" + left_code + ")"

        # Check if right operand needs parentheses
        if isinstance(self.right, BinaryOperator):
            right_op = str(self.right.sign)
            right_precedence = self._get_operator_precedence(right_op)

            # Add parentheses if right operator has lower precedence
            # or if they have the same precedence but the operation is not associative
            # or if current operator is non-commutative (-, /, %)
            if right_precedence > current_precedence or (
                right_precedence == current_precedence
                and (current_op in {"-", "/", "%"} or right_op in {"-", "/", "%"})
            ):
                if not self._is_parenthesized_expression(right_code):
                    right_code = "(" + right_code + ")"

        # For bitwise and logical operators, use the special formatting
        if current_op in {"&", "|", "&&", "||"}:
            left_code, right_code = self._format_bitwise_logical(left_code, right_code)

        # For all operators, don't add extra parentheses
        return left_code + str(self.sign.to_root()) + right_code

    def to_python(self):
        if str(self.sign) in {"&", "|"}:
            # For bitwise operators, create function calls
            left_code = self.left.to_python()
            right_code = self.right.to_python()
            func_name = self.binary_to_ufunc(self.sign)

            # Note: The original code had identical branches for this check,
            # so we can simplify it
            return f"{func_name}({left_code},{right_code})"

        if str(self.sign) in {"&&", "||"}:
            # Handle logical operators with infix notation
            left_code = self.left.to_python()
            right_code = self.right.to_python()

            # Format operands (remove unnecessary parentheses)
            left_code, right_code = self._format_bitwise_logical(left_code, right_code)

            # Use infix notation with spaces
            operator_str = " " + self.binary_to_ufunc(self.sign) + " "

            return left_code + operator_str + right_code

        pycode = (
            "("
            + str(self.left.to_python())
            + str(self.sign.to_python())
            + str(self.right.to_python())
            + ")"
        )
        return pycode


@dataclass
class Matrix(AST):  # Matrix: A matrix call
    var: Symbol
    paren: list[AST]
    index: int = None

    def __str__(self):
        return "{}[{}]".format(str(self.var), ",".join(str(x) for x in self.paren))

    def to_numexpr(self):
        raise ValueError(
            "Matrix operations are forbidden in Numexpr, please check the formula at index : "
            + str(self.index)
        )

    def to_root(self):
        index = ""
        for elem in self.paren:
            index += "[" + str(elem.to_root()) + "]"
        return self.var.to_root() + index

    def to_python(self):
        temp_str = ["," + elem.to_python() for elem in self.paren]
        return "(" + str(self.var.to_python()) + "[:" + "".join(temp_str) + "]" + ")"


@dataclass
class Slice(AST):  # Slice: The slice for matrix
    slices: AST
    index: int = None

    def __str__(self):
        return f"{self.slices}"

    def to_numexpr(self):
        raise ValueError(
            "Matrix operations are forbidden in Numexpr, please check the formula at index : "
            + str(self.index)
        )

    def to_root(self):
        return self.slices.to_root()

    def to_python(self):
        return self.slices.to_python()


@dataclass
class Empty(AST):  # Slice: The slice for matrix
    index: int = None

    def __str__(self):
        return ""

    def to_numexpr(self):
        raise ""

    def to_root(self):
        return ""

    def to_python(self):
        return ""


@dataclass
class Call(AST):  # Call: evaluate a function on arguments
    function: list[Symbol] | Symbol
    arguments: list[AST]
    index: int = None

    def __str__(self):
        return "{}({})".format(
            self.function,
            ", ".join(str(x) for x in self.arguments),
        )

    def to_numexpr(self):
        match str(self.function):
            case "pi":
                return "arccos(-1)"
            case "e":
                return "exp(1)"
            case "inf":
                return "inf"
            case "nan":
                raise ValueError("No equivalent in Numexpr!")
            case "sqrt2":
                return "sqrt(2)"
            case "piby2":
                return "(arccos(-1)/2)"
            case "piby4":
                return "(arccos(-1)/4)"
            case "2pi":
                return "(arccos(-1)*2.0)"
            case "ln10":
                return "log(10)"
            case "loge":
                return "np.log(np.exp(1))"
            case "log" | "TMath::Log":
                return f"log({self.arguments[0].to_numexpr()})"
            case "log10" | "TMath::Log10":
                return f"log10({self.arguments[0].to_numexpr()})"
            case "log2":
                return f"(log({self.arguments[0].to_numexpr()})/log(2))"
            case "degtorad":
                return f"degtorad({self.arguments[0].to_numexpr()})"
            case "radtodeg":
                return f"np.degrees({self.arguments[0].to_numexpr()})"
            case "exp":
                return f"exp({self.arguments[0].to_numexpr()})"
            case "sin":
                return f"sin({self.arguments[0].to_numexpr()})"
            case "asin" | "arcsin":
                return f"arcsin({self.arguments[0].to_numexpr()})"
            case "sinh":
                return f"sinh({self.arguments[0].to_numexpr()})"
            case "asinh":
                return f"arcsinh({self.arguments[0].to_numexpr()})"
            case "cos":
                return f"cos({self.arguments[0].to_numexpr()})"
            case "acos" | "arccos":
                return f"acos({self.arguments[0].to_numexpr()})"
            case "cosh":
                return f"cosh({self.arguments[0].to_numexpr()})"
            case "acosh":
                return f"arccosh({self.arguments[0].to_numexpr()})"
            case "tan":
                return f"tan({self.arguments[0].to_numexpr()})"
            case "atan" | "arctan":
                return f"arctan({self.arguments[0].to_numexpr()})"
            case "atan2" | "arctan2":
                return f"arctan2({self.arguments[0].to_numexpr()}, {self.arguments[1].to_numexpr()})"
            case "tanh":
                return f"tanh({self.arguments[0].to_numexpr()})"
            case "atanh":
                return f"arctanh({self.arguments[0].to_numexpr()})"
            case "Math::sqrt":
                return f"sqrt({self.arguments[0].to_numexpr()})"
            case "sqrt":
                return f"sqrt({self.arguments[0].to_numexpr()})"
            case "ceil":
                return f"ceil({self.arguments[0].to_numexpr()})"
            case "abs":
                return f"abs({self.arguments[0].to_numexpr()})"
            case "even":
                return f"not ({self.arguments[0].to_numexpr()} % 2)"
            case "factorial":
                raise ValueError("Cannot translate to Numexpr!")
            case "floor":
                return f"floor({self.arguments[0].to_numexpr()})"
            case "max":
                return f"maximum({self.arguments[0].to_numexpr()})"
            case "min":
                return f"minimum({self.arguments[0].to_numexpr()})"
            case "sum":
                return f"sum({self.arguments[0].to_numexpr()})"
            case "where":
                return f"where({self.arguments[0].to_numexpr()},{self.arguments[1].to_numexpr()},{self.arguments[2].to_numexpr()})"
            case ":":
                # Special case for multi_out
                return ", ".join(arg.to_numexpr() for arg in self.arguments)
            case "TMath::Power":
                # Handle ROOT's power function
                return f"({self.arguments[0].to_numexpr()}**{self.arguments[1].to_numexpr()})"
            case _:
                raise ValueError(f"Not a valid function: {self.function}")

    def to_root(self):
        # Helper function to process arguments
        def process_arg(arg):
            arg_code = arg.to_root()
            # Remove outer parentheses to avoid double parentheses
            if arg_code.startswith("(") and arg_code.endswith(")"):
                arg_code = arg_code[1:-1]
            return arg_code

        match str(self.function):
            case "pi":
                return "TMath::Pi()"
            case "e":
                return "TMath::E()"
            case "inf":
                return "TMath::Infinity()"
            case "nan":
                return "TMath::QuietNaN()"
            case "sqrt2":
                return "TMath::Sqrt2()"
            case "piby2":
                return "TMath::PiOver2()"
            case "piby4":
                return "TMath::PiOver4()"
            case "2pi":
                return "TMath::TwoPi()"
            case "ln10":
                return "TMath::Ln10()"
            case "loge":
                return "TMath::LogE()"
            case "log":
                return f"TMath::Log({process_arg(self.arguments[0])})"
            case "log10":
                return f"TMath::Log10({process_arg(self.arguments[0])})"
            case "log2":
                return f"TMath::Log2({process_arg(self.arguments[0])})"
            case "degtorad":
                return f"TMath::DegToRad({process_arg(self.arguments[0])})"
            case "radtodeg":
                return f"TMath::RadToDeg({process_arg(self.arguments[0])})"
            case "exp":
                return f"TMath::Exp({process_arg(self.arguments[0])})"
            case "sin":
                return f"TMath::Sin({process_arg(self.arguments[0])})"
            case "asin" | "arcsin":
                return f"TMath::ASin({process_arg(self.arguments[0])})"
            case "sinh":
                return f"TMath::SinH({process_arg(self.arguments[0])})"
            case "asinh":
                return f"TMath::ASinH({process_arg(self.arguments[0])})"
            case "cos":
                return f"TMath::Cos({process_arg(self.arguments[0])})"
            case "acos" | "arccos":
                return f"TMath::ACos({process_arg(self.arguments[0])})"
            case "cosh":
                return f"TMath::CosH({process_arg(self.arguments[0])})"
            case "acosh":
                return f"TMath::ACosH({process_arg(self.arguments[0])})"
            case "tan":
                return f"TMath::Tan({process_arg(self.arguments[0])})"
            case "atan" | "arctan":
                return f"TMath::ATan({process_arg(self.arguments[0])})"
            case "atan2" | "arctan2":
                return f"TMath::ATan2({process_arg(self.arguments[0])}, {process_arg(self.arguments[1])})"
            case "tanh":
                return f"TMath::TanH({process_arg(self.arguments[0])})"
            case "atanh":
                return f"TMath::ATanH({process_arg(self.arguments[0])})"
            case "Math::sqrt":
                return f"TMath::Sqrt({process_arg(self.arguments[0])})"
            case "sqrt":
                return f"TMath::Sqrt({process_arg(self.arguments[0])})"
            case "ceil":
                return f"TMath::Ceil({process_arg(self.arguments[0])})"
            case "abs":
                return f"TMath::Abs({process_arg(self.arguments[0])})"
            case "even":
                return f"TMath::Even({process_arg(self.arguments[0])})"
            case "factorial":
                return f"TMath::Factorial({process_arg(self.arguments[0])})"
            case "floor":
                return f"TMath::Floor({process_arg(self.arguments[0])})"
            case "max":
                return f"Max$({process_arg(self.arguments[0])})"
            case "min":
                return f"Min$({process_arg(self.arguments[0])})"
            case "sum":
                return f"Sum$({process_arg(self.arguments[0])})"
            case "no_of_entries":
                return f"Length$({process_arg(self.arguments[0])})"
            case "min_if":
                if len(self.arguments) >= 2:
                    return f"MinIf$({process_arg(self.arguments[0])}, {process_arg(self.arguments[1])})"
                return f"MinIf$({process_arg(self.arguments[0])})"
            case "max_if":
                if len(self.arguments) >= 2:
                    return f"MaxIf$({process_arg(self.arguments[0])}, {process_arg(self.arguments[1])})"
                return f"MaxIf$({process_arg(self.arguments[0])})"
            case ":":
                # Special case for multi_out
                return ", ".join(arg.to_root() for arg in self.arguments)
            case _:
                raise ValueError(f"Not a valid function: {self.function}")

    def to_python(self):
        match str(self.function):
            case "pi":
                return "np.pi"
            case "e":
                return "np.exp(1)"
            case "inf":
                return "np.inf"
            case "nan":
                return "np.nan"
            case "sqrt2":
                return "np.sqrt(2)"
            case "piby2":
                return "(np.pi/2)"
            case "piby4":
                return "(np.pi/4)"
            case "2pi":
                return "(np.pi*2.0)"
            case "ln10":
                return "np.log(10)"
            case "loge":
                return "np.log(np.exp(1))"
            case "log":
                return f"np.log({self.arguments[0].to_python()})"
            case "log10":
                return f"np.log10({self.arguments[0].to_python()})"
            case "log2":
                return f"np.log2({self.arguments[0].to_python()})"  # Fixed: simplify to log2
            case "degtorad":
                return f"np.radians({self.arguments[0].to_python()})"
            case "radtodeg":
                return f"np.degrees({self.arguments[0].to_python()})"
            case "exp":
                return f"np.exp({self.arguments[0].to_python()})"
            case "sin":
                return f"np.sin({self.arguments[0].to_python()})"
            case "asin" | "arcsin":
                return f"np.arcsin({self.arguments[0].to_python()})"
            case "sinh":
                return f"np.sinh({self.arguments[0].to_python()})"
            case "asinh":
                return f"np.arcsinh({self.arguments[0].to_python()})"
            case "cos":
                return f"np.cos({self.arguments[0].to_python()})"
            case "acos" | "arccos":
                return f"np.arccos({self.arguments[0].to_python()})"
            case "cosh":
                return f"np.cosh({self.arguments[0].to_python()})"
            case "acosh":
                return f"np.arccosh({self.arguments[0].to_python()})"
            case "tan":
                return f"np.tan({self.arguments[0].to_python()})"
            case "atan" | "arctan":
                return f"np.arctan({self.arguments[0].to_python()})"
            case "atan2" | "arctan2":
                return f"np.arctan2({self.arguments[0].to_python()}, {self.arguments[1].to_python()})"
            case "tanh":
                return f"np.tanh({self.arguments[0].to_python()})"
            case "atanh":
                return f"np.arctanh({self.arguments[0].to_python()})"
            case "Math::sqrt":
                return f"np.sqrt({self.arguments[0].to_python()})"
            case "sqrt":
                return f"np.sqrt({self.arguments[0].to_python()})"
            case "ceil":
                return f"np.ceil({self.arguments[0].to_python()})"
            case "abs":
                return f"np.abs({self.arguments[0].to_python()})"
            case "even":
                return f"not ({self.arguments[0].to_python()} % 2)"
            case "factorial":
                return f"np.math.factorial({self.arguments[0].to_python()})"
            case "floor":
                return (
                    f"np.floor({self.arguments[0].to_python()})"  # Fixed: was negated
                )
            case "max":
                return f"root_max({self.arguments[0].to_python()})"
            case "min":
                return f"root_min({self.arguments[0].to_python()})"
            case "sum":
                return f"root_sum({self.arguments[0].to_python()})"
            case "no_of_entries":
                return f"root_length({self.arguments[0].to_python()})"
            case "min_if":
                if len(self.arguments) >= 2:
                    return f"root_min_if({self.arguments[0].to_python()}, {self.arguments[1].to_python()})"
                return f"root_min_if({self.arguments[0].to_python()})"
            case "max_if":
                if len(self.arguments) >= 2:
                    return f"root_max_if({self.arguments[0].to_python()}, {self.arguments[1].to_python()})"
                return f"root_max_if({self.arguments[0].to_python()})"
            case ":":
                # Special case for multi_out
                return ", ".join(arg.to_python() for arg in self.arguments)
            case _:
                raise ValueError(f"Not a valid function: {self.function}")
