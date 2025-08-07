# Licensed under a 3-clause BSD style license, see LICENSE.

from __future__ import annotations

from abc import ABCMeta, abstractmethod
from dataclasses import dataclass


class AST(metaclass=ABCMeta):  # only three types (and a superclass to set them up)
    _fields = ()

    @abstractmethod
    def __str__(self):
        msg = "__str__() not implemented, subclass must implement it"
        raise NotImplementedError(msg)

    @abstractmethod
    def to_numexpr(self):
        msg = "to_numexpr() not implemented, subclass must implement it"
        raise NotImplementedError(msg)

    @abstractmethod
    def to_root(self):
        msg = "to_root() not implemented, subclass must implement it"
        raise NotImplementedError(msg)

    @abstractmethod
    def to_python(self):
        msg = "to_python() not implemented, subclass must implement it"
        raise NotImplementedError(msg)


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
        if (
            str(self.sign) in {"/", "*"}
            and isinstance(self.right, BinaryOperator)
            and str(self.right.sign)
            in {
                "&",
                "|",
                "&&",
                "||",
            }
        ):
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

    def to_root(self):
        return self._to_infix_format("to_root")

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

        # For standard operators (+, -, *, /, etc.)
        left_code = self._strip_parentheses(str(self.left.to_python()))
        right_code = self._strip_parentheses(str(self.right.to_python()))

        return left_code + str(self.sign.to_python()) + right_code


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
        return ""

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
                msg = "NaN is not supported in NumExpr"
                raise ValueError(msg)
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
                return "np.log10(np.exp(1))"
            case "log":
                return f"log({self.arguments[0].to_numexpr()})"
            case "log10":
                return f"(log({self.arguments[0].to_numexpr()})/log(10))"
            case "degtorad":
                return f"np.radians({self.arguments[0].to_numexpr()})"
            case "radtodeg":
                return f"np.degrees({self.arguments[0].to_numexpr()})"
            case "exp":
                return f"np.exp({self.arguments[0].to_numexpr()})"
            case "sin":
                return f"sin({self.arguments[0].to_numexpr()})"
            case "asin":
                return f"arcsin({self.arguments[0].to_numexpr()})"
            case "sinh":
                return f"sinh({self.arguments[0].to_numexpr()})"
            case "asinh":
                return f"arcsinh({self.arguments[0].to_numexpr()})"
            case "cos":
                return f"cos({self.arguments[0].to_numexpr()})"
            case "arccos":
                return f"arccos({self.arguments[0].to_numexpr()})"
            case "cosh":
                return f"cosh({self.arguments[0].to_numexpr()})"
            case "acosh":
                return f"arccosh({self.arguments[0].to_numexpr()})"
            case "tan":
                return f"tan({self.arguments[0].to_numexpr()})"
            case "arctan":
                return f"arctan({self.arguments[0].to_numexpr()})"
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
                msg = "factorial is not supported in NumExpr"
                raise ValueError(msg)
            case "floor":
                return f"! np.floor({self.arguments[0]})"
            case "where":
                return f"where({self.arguments[0].to_numexpr()},{self.arguments[1].to_numexpr()},{self.arguments[2].to_numexpr()})"
            case _:
                msg = f"{self.function} is not supported in NumExpr"
                raise ValueError(msg)

    def to_root(self):
        match str(self.function):
            case "pi":
                return "TMath::Pi"
            case "e":
                return "TMath::E"
            case "inf":
                return "TMath::Infinity"
            case "nan":
                return "TMath::QuietNan"
            case "sqrt2":
                return "TMath::Sqrt2({self.arguments[0]})"
            case "piby2":
                return "TMath::PiOver4"
            case "piby4":
                return "TMath::PiOver4"
            case "2pi":
                return "TMath::TwoPi"
            case "ln10":
                return f"TMath::Ln10({self.arguments[0].to_root()})"
            case "loge":
                return f"TMath::LogE({self.arguments[0].to_root()})"
            case "log":
                return f"TMath::Log({self.arguments[0].to_root()})"
            case "log2":
                return f"TMath::Log2({self.arguments[0].to_root()})"
            case "degtorad":
                return f"TMath::DegToRad({self.arguments[0].to_root()})"
            case "radtodeg":
                return f"TMath::RadToDeg({self.arguments[0].to_root()})"
            case "exp":
                return f"TMath::Exp({self.arguments[0].to_root()})"
            case "sin":
                return f"TMath::Sin({self.arguments[0].to_root()})"
            case "asin":
                return f"TMath::ASin({self.arguments[0].to_root()})"
            case "sinh":
                return f"TMath::SinH({self.arguments[0].to_root()})"
            case "asinh":
                return f"TMath::ASinH({self.arguments[0].to_root()})"
            case "cos":
                return f"TMath::Cos({self.arguments[0].to_root()})"
            case "arccos":
                return f"TMath::ACos({self.arguments[0].to_root()})"
            case "cosh":
                return f"TMath::CosH({self.arguments[0].to_root()})"
            case "acosh":
                return f"TMath::ACosH({self.arguments[0].to_root()})"
            case "tan":
                return f"TMath::Tan({self.arguments[0].to_root()})"
            case "arctan":
                return f"TMath::ATan({self.arguments[0].to_root()})"
            case "tanh":
                return f"TMath::TanH({self.arguments[0].to_root()})"
            case "atanh":
                return f"TMath::ATanH({self.arguments[0].to_root()})"
            case "TMath::Sqrt":
                return f"TMath::Sqrt({self.arguments[0].to_root()})"
            case "sqrt":
                return f"TMath::Sqrt({self.arguments[0].to_root()})"
            case "ceil":
                return f"TMath::Ceil({self.arguments[0].to_root()})"
            case "abs":
                return f"TMath::Abs({self.arguments[0].to_root()})"
            case "even":
                return f"TMath::Even({self.arguments[0].to_root()})"
            case "factorial":
                return f"TMath::Factorial({self.arguments[0].to_root()})"
            case "floor":
                return f"TMath::Floor({self.arguments[0].to_root()})"
            case "abs":
                return f"TMath::Abs({self.arguments[0].to_root()})"
            case "max":
                return f"Max$({self.arguments[0].to_root()})"
            case "min":
                return f"Min$({self.arguments[0].to_root()})"
            case "sum":
                return f"Sum$({self.arguments[0].to_root()})"
            case "no_of_entries":
                return f"Length$({self.arguments[0].to_root()})"
            case "min_if":
                return f"MinIf$({self.arguments[0].to_root()})"
            case "max_if":
                return f"MaxIf$({self.arguments[0].to_root()})"
            case _:
                msg = f"{self.function} is not supported in ROOT"
                raise ValueError(msg)

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
                return "np.log10(np.exp(1))"
            case "log":
                return f"np.log10({self.arguments[0].to_python()})"
            case "log2":
                return f"(np.log({self.arguments[0].to_python()})/log(2))"
            case "degtorad":
                return f"np.radians({self.arguments[0].to_python()})"
            case "radtodeg":
                return f"np.degrees({self.arguments[0].to_python()})"
            case "exp":
                return f"np.exp({self.arguments[0].to_python()})"
            case "sin":
                return f"np.sin({self.arguments[0].to_python()})"
            case "asin":
                return f"np.arcsin({self.arguments[0].to_python()})"
            case "sinh":
                return f"np.sinh({self.arguments[0].to_python()})"
            case "asinh":
                return f"np.arcsinh({self.arguments[0].to_python()})"
            case "cos":
                return f"np.cos({self.arguments[0].to_python()})"
            case "arccos":
                return f"np.arccos({self.arguments[0].to_python()})"
            case "cosh":
                return f"np.cosh({self.arguments[0].to_python()})"
            case "acosh":
                return f"np.arccosh({self.arguments[0].to_python()})"
            case "tan":
                return f"np.tan({self.arguments[0].to_python()})"
            case "arctan":
                return f"np.arctan({self.arguments[0].to_python()})"
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
                return f"! ({self.arguments[0].to_python()} % 2)"
            case "factorial":
                return f"np.math.factorial({self.arguments[0].to_python()})"
            case "floor":
                return f"! np.floor({self.arguments[0].to_python()})"
            case "abs":
                return f"np.abs({self.arguments[0].to_python()})"
            case "max":
                return f"root_max({self.arguments[0].to_python()})"
            case "min":
                return f"root_min({self.arguments[0].to_python()})"
            case "sum":
                return f"root_sum({self.arguments[0].to_python()})"
            case "no_of_entries":
                return f"root_length({self.arguments[0].to_python()})"
            case "min_if":
                return f"root_min_if({self.arguments[0].to_python()}, {self.arguments[1].to_python()})"
            case "max_if":
                return f"root_max_if({self.arguments[0].to_python()}, {self.arguments[1].to_python()})"
            case _:
                msg = f"{self.function} is not supported in Python"
                raise ValueError(msg)
