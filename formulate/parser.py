# -*- coding: utf-8 -*-
# Licensed under a 3-clause BSD style license, see LICENSE.
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

from collections import defaultdict

import pyparsing
from pyparsing import Literal, Suppress, pyparsing_common, opAssoc, Word, delimitedList

from .expression import Expression, Variable, NamedConstant, UnnamedConstant, ExpressionComponent
from .identifiers import order_of_operations
from .logging import logger, add_logging


__all__ = [
    'PConstant',
    'PFunction',
    'POperator',
    'Parser',
    'ParsingException',
]


class PConstant(object):
    def __init__(self, id, value):
        """Represents a named constant

        Parameters
        ----------
        id : :ConstantIDs:
            Element of the ConstantIDs enum representing this constant
        value : int, float, str
            The representing this function as a string or number

        Examples
        --------
        >>> str(PConstant('sqrt2', 'TMath::Sqrt2()')())
        'TMath::Sqrt2()'
        >>> str(PConstant(ConstantIDS.SQRT2, 1.4142135624)())
        '1.4142135624'
        """
        self._id = id
        self._value = value

    @add_logging
    def __call__(self, string, location, result):
        return NamedConstant(self.id)

    @property
    def id(self):
        return self._id

    @property
    def value(self):
        return self._value

    def get_parser(self, EXPRESSION):
        if isinstance(self.value, str):
            result = Suppress(self.value)
            result.setName('NamedConstant({value})'.format(value=self.value))
            result.setParseAction(self)
            return result
        else:
            # TODO Detect constants?
            return None

    @add_logging
    def to_string(self):
        return str(self.value)


class PFunction(object):
    def __init__(self, id, name, n_args=1):
        """Represents a function call with augments

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
    def __call__(self, string, location, result):
        if len(result) != self._n_args:
            raise TypeError('Function({name}) requires {n} arguments, {x} given'
                            .format(name=self._name, n=self._n_args, x=len(result)))
        return Expression(self._id, *result)

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
        result.setParseAction(self)
        return result

    @add_logging(ignore_args=[2, 3])
    def to_string(self, expression, config, constants):
        args = []
        for arg in expression.args:
            if isinstance(arg, Expression):
                arg = arg.to_string(config, constants)
            else:
                arg = str(arg)
            args.append(arg)
        return self.name+'('+", ".join(args)+')'


class POperator(object):
    def __init__(self, id, op, rhs_only=False, lhs_only=False):
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
        assert lhs_only + rhs_only <= 1
        self._id = id
        self._op = op
        self._rhs_only = rhs_only
        self._lhs_only = lhs_only

    def __str__(self):
        return self._name+'<'+str(self._n_args)+'>'

    def __repr__(self):
        return '{class_name}<{id_name},{op_name},rhs_only={rhs_only},lhs_only={lhs_only}>'.format(
            class_name=self.__class__.__name__, id_name=self._id.name,
            op_name=self._op, rhs_only=self._rhs_only, lhs_only=self._lhs_only)

    @add_logging
    def __call__(self, *result):
        return Expression(self._id, *result)

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
    def lhs_only(self):
        return self._lhs_only

    @property
    def precedence(self):
        matches = [self.id in level for level in order_of_operations]
        assert matches.count(True) == 1, (self.id, matches)
        return matches.index(True)

    @add_logging(ignore_args=[2, 3])
    def to_string(self, expression, config, constants):
        args = []
        for arg in expression.args:
            arg = arg.to_string(config, constants)
            args.append(arg)

        if self._rhs_only:
            assert len(args) == 1, args
            return self.op + args[0]
        elif self._lhs_only:
            assert len(args) == 1, args
            return args[0] + self.op
        else:
            assert len(args) >= 2, args
            return '('+(' '+self.op+' ').join(args)+')'


class Parser(object):
    def __init__(self, name, config, constants):
        self._name = name
        self._config = config
        self._constants = constants
        self._parser = create_parser(config, constants)

    def to_expression(self, string):
        if not isinstance(string, str):
            raise ValueError('Can only convert string objects to strings but '+str(type(string))+' was passed')

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
            # Remove the context from the exception
            # Can't use "raise X from None" with Python 2
            exception = ParsingException()
            exception.__context__ = None
            raise exception
        else:
            return result

    def to_string(self, expression):
        if not isinstance(expression, ExpressionComponent):
            raise ValueError('Can only convert ExpressionComponent objects to strings but ' +
                             str(type(expression)) + ' was passed')

        result = expression.to_string(
            {x.id: x for x in self._config},
            {c.id: c for c in self._constants},
        )
        if result.startswith('(') and result.endswith(')'):
            result = result[1:-1]
        return result


class ParsingException(Exception):
    pass


def create_parser(config, constants):
    EXPRESSION = pyparsing.Forward()

    VARIABLE = delimitedList(Word(pyparsing.alphas+'_', pyparsing.alphanums+'_-'), delim='.', combine=True)
    VARIABLE.setName('Variable')
    VARIABLE.setParseAction(add_logging(lambda string, location, result: Variable(result[0])))

    REAL = pyparsing_common.real
    REAL.setParseAction(add_logging(lambda string, location, result: UnnamedConstant(result[0])))
    SCI_REAL = pyparsing_common.sci_real
    SCI_REAL.setParseAction(add_logging(lambda string, location, result: UnnamedConstant(result[0])))
    SIGNED_INTEGER = pyparsing_common.signed_integer
    SIGNED_INTEGER.setParseAction(add_logging(lambda string, location, result: UnnamedConstant(result[0])))
    NUMBER = pyparsing.Or([REAL, SCI_REAL, SIGNED_INTEGER])

    COMPONENT = pyparsing.Or(
        [f.get_parser(EXPRESSION) for f in config if isinstance(f, PFunction)] +
        [p for p in map(lambda c: c.get_parser(EXPRESSION), constants) if p is not None] +
        [NUMBER, VARIABLE]
    )

    # TODO Generating operators_config should be rewritten
    operators = defaultdict(list)
    for operator in config:
        if not isinstance(operator, POperator):
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
        elif ops[0].id in (IDs.SQUARE,):
            assert ops[0]._lhs_only
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
        elif ops[0].lhs_only:
            def parse_action(string, location, result, op_map={o.op: o for o in ops}):
                assert len(result) == 1, result
                result = result[0]
                assert len(result) == 2, result
                return op_map[result[0]](result[1])
            operators_config.append((parser, 1, opAssoc.LEFT, parse_action))
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
