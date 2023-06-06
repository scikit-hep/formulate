"""
Copyright (c) 2023 Aryan Roy. All rights reserved.

formulate:  Easy conversions between different styles of expressions
"""
from __future__ import annotations

import lark


class AST:  # only three types (and a superclass to set them up)
    _fields = ()

    def __init__(self, *args, line=None):
        self.line = line
        for n, x in zip(self._fields, args):
            setattr(self, n, x)
            if self.line is None:
                if isinstance(x, list):
                    self.line = x[0].line
                else:
                    self.line = x.line


class Literal(AST):  # Literal: value that appears in the program text
    _fields = ("value",)

    def __str__(self):
        return str(self.value)


class Symbol(AST):  # Symbol: value referenced by name
    _fields = ("symbol",)

    def __str__(self):
        return self.symbol


class UnaryOperator(AST):  # Unary Operator: Operation with one operand
    _fields = ("sign", "operand")

    def __str__(self):
        return "{0}({1})".format(str(self.sign), self.operand)


class BinaryOperator(AST):  # Binary Operator: Operation with two operands
    _fields = ("sign", "left", "right")

    def __str__(self):
        return "{0}({1},{2})".format(str(self.sign), self.left, self.right)


class Matrix(AST):  # Matrix: A matrix call
    _fields = ("var", "paren")

    def __str__(self):
        return "{0}[{1}]".format(str(self.var), ",".join(str(x) for x in self.paren))


class Slice(AST):  # Slice: The slice for matrix
    _fields = ("slices",)

    def __str__(self):
        return "{0}".format(self.slices)


class Empty(AST):  # Slice: The slice for matrix
    _fields = ()

    def __str__(self):
        return ""


class Call(AST):  # Call: evaluate a function on arguments
    _fields = ("function", "arguments")

    def __str__(self):
        return "{0}({1})".format(
            "::".join(str(x) for x in self.function),
            ", ".join(str(x) for x in self.arguments),
        )


# Add data classes
# fix error handling
# get rid of non-functional elements
# come-up with a shared notation for functions
# make a  to_python function
