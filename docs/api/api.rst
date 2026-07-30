API Reference
======================

Formulate's public interface is small: two functions that parse, and one class
whose methods and properties do everything else.

.. code-block:: pycon

   >>> import formulate
   >>> expression = formulate.from_root("TMath::Sqrt(x**2 + y**2) > 10")
   >>> expression.to_numexpr()
   '(sqrt(((x ** 2) + (y ** 2))) > 10)'
   >>> list(expression.variables)
   ['x', 'y']

:doc:`modules/formulate` covers the parsing functions, and
:doc:`modules/ast` the expression objects they return. The remaining pages
document the internals: the lookup tables that decide how each name is spelled
in each language, the parse-tree conversion, and the exceptions.

.. toctree::
   :maxdepth: 1
   :caption: Modules

   modules/formulate
   modules/ast
   modules/identifiers
   modules/toast
   modules/exceptions
