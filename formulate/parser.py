# -*- coding: utf-8 -*-
# Licensed under a 3-clause BSD style license, see LICENSE.
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

from collections import defaultdict
from functools import wraps
import logging
import sys

import pyparsing
from pyparsing import Literal, Suppress, pyparsing_common, opAssoc

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
        logger.debug('Calling '+func.__qualname__+' with '+repr(args)+' and '+repr(kwargs))
        result = func(*args, **kwargs)
        logger.debug(' - Got result '+repr(result))
        return result
    return new_func


# EXPRESSION = pyparsing.Forward()
NUMBER = pyparsing.Or([pyparsing_common.number, pyparsing_common.sci_real])


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
        return '{name}<{n_args}>'.format(name=self._name, n_args=self._n_args)

    def __repr__(self):
        return '{class_name}<{id_name},{name},n_args={n_args}>'.format(
            class_name=self.__class__.__name__, id_name=self._id.name,
            name=self._name, n_args=self._n_args)

    @add_logging
    def __call__(self, *args):
        if len(args) != self._n_args:
            raise TypeError('Function({name}) requires {n} arguments, {x} given'
                            .format(name=self._name, n=self._n_args, x=len(args)))
        return Expression(self._id, *args)

    @property
    def id(self):
        return self._id

    @property
    def name(self):
        return self._name

    def get_parser(self, EXPRESSION):
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

    def to_string(self, expression, config):
        args = []
        for arg in expression.args:
            if isinstance(arg, Expression):
                arg = arg.to_string(config)
            else:
                arg = str(arg)
            args.append(arg)
        return self.name+'('+", ".join(args)+')'


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
        return self._name+'<'+str(self._n_args)+'>'

    def __repr__(self):
        return '{class_name}<{id_name},{op_name},rhs_only={rhs_only}>'.format(
            class_name=self.__class__.__name__, id_name=self._id.name,
            op_name=self._op, rhs_only=self._rhs_only)

    # Used to set order of operations
    def __gt__(self, other):
        return self.precedence > other.precedence

    def __lt__(self, other):
        return self.precedence < other.precedence

    @add_logging
    def __call__(self, *args):
        return Expression(self._id, *args)

    @property
    def id(self):
        return self._id

    @property
    def op(self):
        return self._op

    @property
    def rhs_only(self):
        return self._rhs_only

    @property
    def precedence(self):
        matches = [self.id in level for level in order_of_operations]
        assert matches.count(True) == 1, (self.id, matches)
        return matches.index(True)

    def _parse_action(self, string, location, result):
        assert len(result) == 1, result
        result = result[0]
        # TODO Replace with logging decorator
        assert len(result) >= 2 or self._rhs_only, result
        return self(*result)

    def to_string(self, expression, config):
        args = []
        for arg in expression.args:
            if isinstance(arg, Expression):
                arg = arg.to_string(config)
            else:
                arg = str(arg)
            args.append(arg)

        if self._rhs_only:
            assert len(args) == 1, args
            return self.op + args[0]
        else:
            assert len(args) >= 2, args
            return (' '+self.op+' ').join(args)


class Parser(object):
    def __init__(self, name, config):
        self._name = name
        self._config = config
        self._parser = create_parser(config)

    def to_expression(self, string):
        try:
            result = self._parser.parseString(string, parseAll=True)
            assert len(result) == 1, result
            result = result[0]
        except pyparsing.ParseException as e:
            logger.error('TODO TRACEBACK: '+repr(e.args))
            logger.error('Error parsing: '+e.line)
            logger.error('               '+' '*e.loc + '▲')
            logger.error('               '+' '*e.loc + '┃')
            logger.error('               '+' '*e.loc + '┗━━━━━━ Error here or shortly after')
            if sys.version_info < (3, 0):
                raise ParsingException()
            else:
                raise ParsingException() from None
        else:
            return result

    def to_string(self, expression):
        return expression.to_string({x.id: x for x in self._config})


class ParsingException(Exception):
    pass


def create_parser(config):
    EXPRESSION = pyparsing.Forward()

    COMPONENT = pyparsing.Or(
        [f.get_parser(EXPRESSION) for f in config if isinstance(f, Function)] +
        [NUMBER]
    )

    # TODO Generating operators_config should be rewritten
    operators = defaultdict(list)
    for operator in config:
        if not isinstance(operator, Operator):
            continue
        operators[operator.precedence].append(operator)

    operators_config = []
    for precedence, ops in sorted(operators.items()):
        assert all(ops[0].rhs_only == o.rhs_only for o in ops), ops

        # TODO This is a hack, is there a nicer way?
        from .identifiers import IDs
        if ops[0].id in (IDs.MINUS, IDs.PLUS):
            assert ops[0]._rhs_only
            parser = pyparsing.Or([Literal(o.op) + ~pyparsing.FollowedBy(NUMBER) for o in ops])
        else:
            parser = pyparsing.Or([Literal(o.op) for o in ops])

        if ops[0].rhs_only:
            def parse_action(string, location, result, op_map={o.op: o for o in ops}):
                assert len(result) == 1, result
                result = result[0]
                assert len(result) == 2, result
                return op_map[result[0]](result[1])
            operators_config.append((parser, 1, opAssoc.RIGHT, parse_action))
        else:
            def parse_action(string, location, result, op_map={o.op: o for o in ops}):
                assert len(result) == 1, result
                result = result[0]

                expression = result[0]
                expression_args = [result[2]]
                last_op_name = result[1]
                for op_name, value in zip(result[3::2], result[4::2]):
                    if op_name == last_op_name:
                        expression_args.append(value)
                    else:
                        expression = Expression(op_map[last_op_name].id, expression, *expression_args)
                        expression_args = [value]
                    last_op_name = op_name
                expression = Expression(op_map[last_op_name].id, expression, *expression_args)
                # for operator, value in zip(result[1::2], result[2::2]):
                #     operator = op_map[operator]
                #     expression = Expression(operator.id, expression, value)
                return expression
            operators_config.append((parser, 2, opAssoc.LEFT, parse_action))

    EXPRESSION << pyparsing.infixNotation(COMPONENT, operators_config)

    return EXPRESSION
