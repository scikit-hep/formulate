Identifiers
=======================================

.. automodule:: formulate.identifiers

For the list of what is actually supported, in a form meant for reading, see
:doc:`../../guide/expressions`. The tables below are the definitions that page
describes; their contents are not reproduced here, since they are long and the
guide already lays them out side by side.

.. autodata:: formulate.identifiers.FUNCTIONS
.. autodata:: formulate.identifiers.CONSTANTS
.. autodata:: formulate.identifiers.UNARY_OPERATORS
.. autodata:: formulate.identifiers.BINARY_OPERATORS
.. autodata:: formulate.identifiers.NAMESPACES

Backend spellings
---------------------------------------

One map per language, from canonical name to how that language writes it. A
canonical name missing from a map is not supported by that language, and
rendering it raises ``ValueError``.

.. autodata:: formulate.identifiers.ROOT_FUNCTIONS
.. autodata:: formulate.identifiers.NUMEXPR_FUNCTIONS
.. autodata:: formulate.identifiers.PYTHON_FUNCTIONS
.. autodata:: formulate.identifiers.ROOT_CONSTANTS
.. autodata:: formulate.identifiers.NUMEXPR_CONSTANTS
.. autodata:: formulate.identifiers.PYTHON_CONSTANTS
.. autodata:: formulate.identifiers.ROOT_OPERATOR_SYMBOLS
.. autodata:: formulate.identifiers.NUMEXPR_OPERATOR_SYMBOLS
.. autodata:: formulate.identifiers.PYTHON_OPERATOR_SYMBOLS
.. autodata:: formulate.identifiers.PYTHON_UNARY_FUNCTIONS

Aliases
---------------------------------------

Alternative spellings a parser may encounter, mapped onto one canonical name.

.. autodata:: formulate.identifiers.FUNCTION_ALIASES
.. autodata:: formulate.identifiers.CONSTANTS_ALIASES
.. autodata:: formulate.identifiers.CONSTANTS_FUNCTION_ALIASES
.. autodata:: formulate.identifiers.FUNCTION_DISPLAY_NAMES
