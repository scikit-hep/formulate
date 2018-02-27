# Licensed under a 3-clause BSD style license, see LICENSE.
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import numbers

from .identifiers import IDs
from .logging import add_logging


__all__ = [
    'ExpressionComponent',
    'SingleComponent',
    'NamedConstant',
    'UnnamedConstant',
    'Expression',
    'Variable',
]


class ExpressionComponent(object):
    def to_numexpr(self, *args, **kwargs):
        from .backends.numexpr import numexpr_parser
        return numexpr_parser.to_string(self, *args, **kwargs)

    def to_root(self, *args, **kwargs):
        from .backends.ROOT import root_parser
        return root_parser.to_string(self, *args, **kwargs)

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
        return Expression(IDs.ABS, self)

    def __pow__(self, other, modulo=None):
        if modulo is None:
            return Expression(IDs.POW, self, other)
        else:
            # TODO Can we keep this optimisation in one operation?
            return Expression(IDs.MOD, Expression(IDs.POW, self, other), modulo)

    def __mod__(self, other):
        return Expression(IDs.MOD, self, other)

    def __and__(self, other):
        return Expression(IDs.AND, self, other)

    def __xor__(self, other):
        return Expression(IDs.XOR, self, other)

    def __or__(self, other):
        return Expression(IDs.OR, self, other)

    def __lshift__(self, other):
        return Expression(IDs.LSHIFT, self, other)

    def __rshift__(self, other):
        return Expression(IDs.RSHIFT, self, other)

    def __neg__(self):
        return Expression(IDs.MINUS, self)

    def __pos__(self):
        return Expression(IDs.PLUS, self)

    def __invert__(self):
        return Expression(IDs.NOT, self)

    def __complex__(self):
        raise NotImplementedError()

    def __int__(self):
        raise NotImplementedError()

    def __long__(self):
        raise NotImplementedError()

    def __float__(self):
        raise NotImplementedError()

    def __oct__(self):
        raise NotImplementedError()

    def __hex__(self):
        raise NotImplementedError()

    def __lt__(self, other):
        return Expression(IDs.LT, self, other)

    def __le__(self, other):
        return Expression(IDs.LTEQ, self, other)

    def __eq__(self, other):
        return Expression(IDs.EQ, self, other)

    def __ne__(self, other):
        return Expression(IDs.NEQ, self, other)

    def __ge__(self, other):
        return Expression(IDs.GTEQ, self, other)

    def __gt__(self, other):
        return Expression(IDs.GT, self, other)

    # Functions
    def where(self):
        raise NotImplementedError()

    def sin(self):
        return Expression(IDs.SIN, self)

    def cos(self):
        return Expression(IDs.COS, self)

    def tan(self):
        return Expression(IDs.TAN, self)

    def arcsin(self):
        return Expression(IDs.ASIN, self)

    def arccos(self):
        return Expression(IDs.ACOS, self)

    def arctan(self):
        return Expression(IDs.ATAN, self)

    def arctan2(self, other):
        return Expression(IDs.ATAN2, self, other)

    def sinh(self):
        return Expression(IDs.ASINH, self)

    def cosh(self):
        return Expression(IDs.COSH, self)

    def tanh(self):
        return Expression(IDs.TANH, self)

    def arcsinh(self):
        return Expression(IDs.ASINH, self)

    def arccosh(self):
        return Expression(IDs.ACOSH, self)

    def arctanh(self):
        return Expression(IDs.ATANH, self)

    def log(self):
        return Expression(IDs.LOG, self)

    def log10(self):
        return Expression(IDs.LOG10, self)

    def log1p(self):
        return Expression(IDs.LOG1p, self)

    def exp(self):
        return Expression(IDs.EXP, self)

    def expm1(self):
        return Expression(IDs.EXPM1, self)

    def sqrt(self):
        return Expression(IDs.SQRT, self)

    def abs(self):
        return Expression(IDs.ABS, self)

    def conj(self):
        raise NotImplementedError()

    def real(self):
        raise NotImplementedError()

    def imag(self):
        raise NotImplementedError()

    def complex(self):
        raise NotImplementedError()


class SingleComponent(ExpressionComponent):
    pass


class Expression(ExpressionComponent):
    def __init__(self, id, *args):
        checked_args = []
        for arg in args:
            if isinstance(arg, numbers.Number):
                checked_args.append(UnnamedConstant(str(arg)))
            elif isinstance(arg, str):
                checked_args.append(Variable(str(arg)))
            elif isinstance(arg, ExpressionComponent):
                checked_args.append(arg)
            else:
                raise ValueError(repr(arg)+' is not a valid type')
        self._id = id
        self._args = checked_args

    def __repr__(self):
        try:
            class_name = self.__class__.__qualname__
        except AttributeError:
            # Python < 3.3 doesn't have __qualname__
            class_name = self.__class__.__name__

        return '{class_name}<{id_name}>({args})'.format(
            class_name=class_name, id_name=self.id.name,
            args=", ".join(map(repr, self.args)))

    def __str__(self):
        return repr(self)

    def _search_for(self, class_to_find):
        result = set()
        components_to_check = [self]
        while components_to_check:
            current_component = components_to_check.pop()
            if isinstance(current_component, Variable):
                if class_to_find is Variable:
                    result.add(str(current_component))
            elif isinstance(current_component, NamedConstant):
                if class_to_find is NamedConstant:
                    result.add(str(current_component))
            elif isinstance(current_component, UnnamedConstant):
                if class_to_find is UnnamedConstant:
                    result.add(str(current_component))
            elif isinstance(current_component, Expression):
                components_to_check.extend(current_component.args)
            else:
                raise ValueError('Unrecognised component "'+repr(current_component)+'" in expression')
        return result

    @property
    def variables(self):
        return self._search_for(Variable)

    @property
    def named_constants(self):
        return self._search_for(NamedConstant)

    @property
    def unnamed_constants(self):
        return self._search_for(UnnamedConstant)

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

    @add_logging(ignore_args=[1, 2])
    def to_string(self, config, constants):
        try:
            return config[self.id].to_string(self, config, constants)
        except KeyError:
            raise NotImplementedError('No known conversion for: '+str(self))


class Variable(SingleComponent):
    def __init__(self, name):
        self._name = name

    def __repr__(self):
        return '{class_name}({name})'.format(
            class_name=self.__class__.__name__, name=self.name)

    def __str__(self):
        return self.name

    @property
    def variables(self):
        return set([str(self)])

    @property
    def named_constants(self):
        return set()

    @property
    def unnamed_constants(self):
        return set()

    @property
    def name(self):
        return self._name

    @add_logging(ignore_args=[1, 2])
    def to_string(self, config, constants):
        return self.name


class NamedConstant(SingleComponent):
    def __init__(self, id):
        self._id = id

    def __repr__(self):
        return '{class_name}({id})'.format(
            class_name=self.__class__.__name__, id=self.id)

    def __str__(self):
        return self.id.name

    @property
    def variables(self):
        return set()

    @property
    def named_constants(self):
        return set([str(self)])

    @property
    def unnamed_constants(self):
        return set()

    @property
    def id(self):
        return self._id

    @add_logging(ignore_args=[1, 2])
    def to_string(self, config, constants):
        try:
            return str(constants[self.id].value)
        except KeyError:
            raise NotImplementedError('No known conversion for constant: '+str(self))


class UnnamedConstant(SingleComponent):
    def __init__(self, value):
        assert isinstance(value, str)
        self._value = value

    def __repr__(self):
        return '{class_name}({value})'.format(
            class_name=self.__class__.__name__, value=self.value)

    def __str__(self):
        return self.value

    @property
    def variables(self):
        return set()

    @property
    def named_constants(self):
        return set()

    @property
    def unnamed_constants(self):
        return set([str(self)])

    @property
    def value(self):
        return self._value

    @add_logging(ignore_args=[1, 2])
    def to_string(self, config, constants):
        return str(self)
