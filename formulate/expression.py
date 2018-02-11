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
        return '{class_name}<{id_name}>({args})'.format(
            class_name=self.__class__.__name__, id_name=self._id.name,
            args=", ".join(map(repr, self._args)))

    def __str__(self):
        return repr(self)

    def equivilent(self, other):
        """Check if two expression objects are the same"""
        raise NotImplementedError()
        if isinstance(other, self.__class__):
            return self.id == other.id and self._args == other._args
        return False

    @property
    def id(self):
        return self._id

    @property
    def args(self):
        return self._args

    def to_string(self, config):
        return config[self.id].to_string(self, config)

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
        raise NotImplementedError()

    def __rtruediv__(self, value):
        # TODO Is this correct for both Python 2 and 3?
        raise NotImplementedError()

    def __floordiv__(self, value):
        # TODO Is this correct for both Python 2 and 3?
        raise NotImplementedError()

    def __rfloordiv__(self, value):
        # TODO Is this correct for both Python 2 and 3?
        raise NotImplementedError()

    def __abs__(self):
        raise NotImplementedError()

    def __pow__(self, other):
        raise NotImplementedError()

    def __mod__(self, other):
        raise NotImplementedError()

    def __lshift__(self, other):
        raise NotImplementedError()

    def __rshift__(self, other):
        raise NotImplementedError()

    # Functions
    def where(self):
        raise NotImplementedError()

    def sin(self):
        raise NotImplementedError()

    def cos(self):
        raise NotImplementedError()

    def tan(self):
        raise NotImplementedError()

    def arcsin(self):
        raise NotImplementedError()

    def arccos(self):
        raise NotImplementedError()

    def arctan(self):
        raise NotImplementedError()

    def arctan2(self, other):
        raise NotImplementedError()

    def sinh(self):
        raise NotImplementedError()

    def cosh(self):
        raise NotImplementedError()

    def tanh(self):
        raise NotImplementedError()

    def arcsinh(self):
        raise NotImplementedError()

    def arccosh(self):
        raise NotImplementedError()

    def arctanh(self):
        raise NotImplementedError()

    def log(self):
        raise NotImplementedError()

    def log10(self):
        raise NotImplementedError()

    def log1p(self):
        raise NotImplementedError()

    def exp(self):
        raise NotImplementedError()

    def expm1(self):
        raise NotImplementedError()

    def sqrt(self):
        raise NotImplementedError()

    def abs(self):
        raise NotImplementedError()

    def conj(self):
        raise NotImplementedError()

    def real(self):
        raise NotImplementedError()

    def imag(self):
        raise NotImplementedError()

    def complex(self):
        raise NotImplementedError()
