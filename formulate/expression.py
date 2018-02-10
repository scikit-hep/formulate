# Licensed under a 3-clause BSD style license, see LICENSE.
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

from .identifiers import IDs


__all__ = [
    'Expression'
]


class Expression(object):
    def __init__(self, id, *args):
        self._id = id
        self._args = args

    def __repr__(self):
        return f'{self.__class__.__name__}<{self._id.name}>({", ".join(map(repr, self._args))})'

    def __str__(self):
        return repr(self)

    def equivilent(self, other):
        """Check if two expression objects are the same"""
        raise NotImplementedError()
        if isinstance(other, self.__class__):
            return self._id == other._id and self._args == other._args
        return False

    # Binary arithmetic operators
    def __add__(self, value):
        return Expression(IDs.ADD, self, value)

    def __radd__(self, value):
        return Expression(IDs.ADD, value, self)

    def __sub__(self, value):
        return Expression(IDs.SUB, self, value)

    def __rsub__(self, value):
        return Expression(IDs.SUB, value, self)

    def __mul__(self, value):
        return Expression(IDs.MUL, self, value)

    def __rmul__(self, value):
        return Expression(IDs.MUL, value, self)

    def __truediv__(self, value):
        # TODO Is this correct for both Python 2 and 3?
        raise NotImplemented

    def __rtruediv__(self, value):
        # TODO Is this correct for both Python 2 and 3?
        raise NotImplemented

    def __floordiv__(self, value):
        # TODO Is this correct for both Python 2 and 3?
        raise NotImplemented

    def __rfloordiv__(self, value):
        # TODO Is this correct for both Python 2 and 3?
        raise NotImplemented

    def __abs__(self):
        raise NotImplemented

    def __pow__(self, other):
        raise NotImplemented

    def __mod__(self, other):
        raise NotImplemented

    def __lshift__(self, other):
        raise NotImplemented

    def __rshift__(self, other):
        raise NotImplemented

    # Functions
    def where(self):
        raise NotImplemented

    def sin(self):
        raise NotImplemented

    def cos(self):
        raise NotImplemented

    def tan(self):
        raise NotImplemented

    def arcsin(self):
        raise NotImplemented

    def arccos(self):
        raise NotImplemented

    def arctan(self):
        raise NotImplemented

    def arctan2(self, other):
        raise NotImplemented

    def sinh(self):
        raise NotImplemented

    def cosh(self):
        raise NotImplemented

    def tanh(self):
        raise NotImplemented

    def arcsinh(self):
        raise NotImplemented

    def arccosh(self):
        raise NotImplemented

    def arctanh(self):
        raise NotImplemented

    def log(self):
        raise NotImplemented

    def log10(self):
        raise NotImplemented

    def log1p(self):
        raise NotImplemented

    def exp(self):
        raise NotImplemented

    def expm1(self):
        raise NotImplemented

    def sqrt(self):
        raise NotImplemented

    def abs(self):
        raise NotImplemented

    def conj(self):
        raise NotImplemented

    def real(self):
        raise NotImplemented

    def imag(self):
        raise NotImplemented

    def complex(self):
        raise NotImplemented
