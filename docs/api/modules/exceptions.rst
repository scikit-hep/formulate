Exceptions
=======================================

Parse failures, and the helpers that attach suggestions to them.

:class:`~formulate.exceptions.ParseError` is re-exported at the top level as
``formulate.ParseError``, which is how it should normally be caught. Note that
it covers *syntax* errors only: an expression that parses but uses a construct
the target language has no equivalent for raises ``ValueError`` when it is
rendered, not when it is parsed.

.. automodule:: formulate.exceptions
   :members:
   :show-inheritance:
