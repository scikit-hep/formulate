# Licensed under a 3-clause BSD style license, see LICENSE.
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

from functools import wraps
import logging

import pyparsing
from pyparsing import Suppress, pyparsing_common, opAssoc

from .expression import Expression
from .identifiers import order_of_operations


__all__ = [
    'Constant',
    'Function',
    'Operator',
    'Parser',
    'ParsingException',
]

import colorlog

handler = colorlog.StreamHandler()
handler.setFormatter(colorlog.ColoredFormatter(
    '%(log_color)s%(levelname)s:%(name)s:%(message)s'))

logger = colorlog.getLogger('formulate.parser')
logger.addHandler(handler)
logger.setLevel(logging.DEBUG)


def add_logging(func):
    @wraps(func)
    def new_func(*args, **kwargs):
        logger.debug(f'Calling {func.__qualname__} with {args} and {kwargs}')
        result = func(*args, **kwargs)
        logger.debug(f' - Got result {result}')
        return result
    return new_func


EXPRESSION = pyparsing.Forward()


class Constant(object):
    def __init__(self, value):
        raise NotImplemented


class Function(object):
    def __init__(self, id, name, n_args=1):
        """Represents an function call with augments

        Parameters
        ----------
        id : :IDs:
            Element of the IDs enum representing this operation
        name : str
            String representing this function
        n_args : int
            Number of arguments required by this function

        Examples
        --------
        >>> str(Function('sqrt', 1)(4))
        'sqrt(4)'
        >>> str(Function('arctan2', 2)(2, 4))
        'arctan2(a, b)'
        """
        assert n_args >= 1, n_args
        self._id = id
        self._name = name
        self._n_args = n_args

    def __str__(self):
        return f'{self._name}<{self._n_args}>'

    def __repr__(self):
        return f'{self.__class__.__name__}<{self._id.name},{self._name},n_args={self._n_args}>'

    @add_logging
    def __call__(self, *args):
        if len(args) != self._n_args:
            raise TypeError('Function({name}) requires {n} arguments, {x} given'
                            .format(name=self._name, n=self._n_args, x=len(args)))
        # return f'F[{self._name}({", ".join(map(str, args))})]'
        return Expression(self._id, *args)

    @property
    def parser(self):
        result = Suppress(self._name) + Suppress('(') + EXPRESSION
        for i in range(1, self._n_args):
            result += Suppress(',') + EXPRESSION
        result += Suppress(')')
        result.setName('Function({name})'.format(name=self._name))
        result.setParseAction(self._parse_action)
        return result

    def _parse_action(self, string, location, result):
        # TODO Replace with logging decorator
        return self(*result)


class Operator(object):
    def __init__(self, id, op, rhs_only=False):
        """Represents an operator of the form "A x B"

        Parameters
        ----------
        id : :IDs:
            Element of the IDs enum representing this operation
        op : str
            String representing this operator
        rhs_only : bool
            Apply this operation to the right hand side only

        Examples
        --------
        >>> str(Operator(IDs.MUL, '*')(4, 5))
        '4 * 5'
        >>> str(Operator(IDs.SUB, '-', allow_lhs_zero=True)(2))
        '-2'
        """
        self._id = id
        self._op = op
        self._rhs_only = rhs_only

    def __str__(self):
        return f'{self._name}<{self._n_args}>'

    def __repr__(self):
        return f'{self.__class__.__name__}<{self._id.name},{self._op},rhs_only={self._rhs_only}>'

    # Set order of operations
    def __gt__(self, other):
        return self.__class__.__lt__(other, self)

    def __lt__(self, other):
        return order_of_operations.index(self._id) < order_of_operations.index(other._id)

    @add_logging
    def __call__(self, a, b=None):
        if self._rhs_only:
            assert b is None
            return Expression(self._id, a)
        else:
            assert b is not None
            return Expression(self._id, a, b)

    @property
    def parser_description(self):
        if self._rhs_only:
            return (Suppress(self._op), 1, opAssoc.RIGHT, self._parse_action)
        else:
            return (Suppress(self._op), 2, opAssoc.LEFT, self._parse_action)

    def _parse_action(self, string, location, result):
        # TODO Replace with logging decorator
        assert len(result) == 1, result
        result = result[0]
        assert len(result) in [1, 2], result
        assert len(result) == 2 or self._rhs_only, result
        return self(*result)


class Parser(object):
    def __init__(self, name, config):
        self._name = name
        self._parser = create_parser(config)

    def to_expression(self, string):
        try:
            result = self._parser.parseString(string, parseAll=True)
            assert len(result) == 1, result
            result = result[0]
        except pyparsing.ParseException as e:
            logger.error('TODO TRACEBACK:', e.args)
            logger.error('Error parsing:', e.line)
            logger.error('              ', ' '*e.loc + '▲')
            logger.error('              ', ' '*e.loc + '┃')
            logger.error('              ', ' '*e.loc + '┗━━━━━━ Error here or shortly after')
            raise ParsingException()
        else:
            return result

    def to_string():
        raise NotImplemented


class ParsingException(Exception):
    pass


def create_parser(config):
    COMPONENT = pyparsing.Or(
        [f.parser for f in config if isinstance(f, Function)] +
        [pyparsing_common.number, pyparsing_common.sci_real]
    )

    # Sort the order of operations as appropriate
    # TODO should this be in the backend configuration?
    operations = [o for o in config if isinstance(o, Operator)]
    operations = [o.parser_description for o in sorted(operations)]
    EXPRESSION << pyparsing.infixNotation(COMPONENT, operations)

    return EXPRESSION
