Formulate
=========

|Build Status| |Coverage Status| |PyPI|

Easy conversions between different styles of expressions. Formulate
currently supports converting between
`ROOT <https://root.cern.ch/doc/master/classTFormula.html>`__ and
`numexpr <https://numexpr.readthedocs.io/en/latest/user_guide.html>`__
style expressions.

.. |Build Status| image:: https://travis-ci.org/scikit-hep/formulate.svg?branch=master
   :target: https://travis-ci.org/scikit-hep/formulate
.. |Coverage Status| image:: https://coveralls.io/repos/github/scikit-hep/formulate/badge.svg?branch=master&service=github
   :target: https://coveralls.io/github/scikit-hep/formulate?branch=master
.. |PyPI| image:: https://badge.fury.io/py/formulate.svg
   :target: https://pypi.python.org/pypi/formulate/


Installation
------------

Install formulate like any other Python package:

.. code-block:: bash

    pip install --user formulate

or similar (use ```sudo``, ```virtualenv``, or ```conda``` if you wish).


Usage
-----

Command line usage
""""""""""""""""""

.. code-block:: bash

    $ python -m formulate --from-root '(A && B) || TMath::Sqrt(A)' --to-numexpr
    (A & B) | sqrt(A)

    $ python -m formulate --from-numexpr '(A & B) | sqrt(A)' --to-root
    (A && B) || TMath::Sqrt(A)

    $ python -m formulate --from-root '(A && B) || TMath::Sqrt(1.23) * e**1.2 + 5*pi' --variables
    A
    B

    $ python -m formulate --from-root '(A && B) || TMath::Sqrt(1.23) * e**1.2 + 5*pi' --named-constants
    E
    PI

    $ python -m formulate --from-root '(A && B) || TMath::Sqrt(1.23) * e**1.2 + 5*pi' --unnamed-constants
    1.2
    1.23
    5

API
"""

The most basic usage involves calling ``from_$BACKEND`` and then ``to_$BACKEND``, for example when starting with a ROOT style expression:

.. code-block:: python

    >>> import formulate
    >>> momentum = formulate.from_root('TMath::Sqrt(X_PX**2 + X_PY**2 + X_PZ**2)')
    >>> momentum
    Expression<SQRT>(Expression<ADD>(Expression<POW>(Variable(X_PX), UnnamedConstant(2)), Expression<POW>(Variable(X_PY), UnnamedConstant(2)), Expression<POW>(Variable(X_PZ), UnnamedConstant(2))))
    >>> momentum.to_numexpr()
    'sqrt(((X_PX ** 2) + (X_PY ** 2) + (X_PZ ** 2)))'
    >>> momentum.to_root()
    'TMath::Sqrt(((X_PX ** 2) + (X_PY ** 2) + (X_PZ ** 2)))'

Similarly, when starting with a ``numexpr`` style expression:

.. code-block:: python

    >>> my_selection = formulate.from_numexpr('X_PT > 5 & (Mu_NHits > 3 | Mu_PT > 10)')
    >>> my_selection.to_root()
    '(X_PT > 5) && ((Mu_NHits > 3) || (Mu_PT > 10))'
    >>> my_selection.to_numexpr()
    '(X_PT > 5) & ((Mu_NHits > 3) | (Mu_PT > 10))'

If the the type of expression isn't known in advance ``formulate`` can also auto detect it:

.. code-block:: python

    >>> my_sum = formulate.from_auto('True + False')
    >>> my_sum.to_root()
    'true + false'
    >>> my_sum.to_numexpr()
    'True + False'


The ``Expression`` Object
"""""""""""""""""""""""""

When calling ``from_*`` the returned object is derived from ``formulate.ExpressionComponent``. From this object you can inspect the expression to find it's dependencies:

.. code-block:: python

    >>> my_check = formulate.from_auto('(X_THETA*TMath::DegToRad() > pi/4) && D_PE > 9.2')
    >>> my_check.variables
    {'D_PE', 'X_THETA'}
    >>> my_check.named_constants
    {'DEG2RAD', 'PI'}
    >>> my_check.unnamed_constants
    {'4', '9.2'}

Additionally ``ExpressionComponent`` s can be combined using both operators and ``numpy`` functions:

.. code-block:: python

    >>> new_selection = (momentum > 100) and (my_check or (numpy.sqrt(my_sum) < 1))
    >>> new_selection.to_numexpr()
    '((X_THETA * 0.017453292519943295) > (3.141592653589793 / 4)) & (D_PE > 9.2)'

As the ``==`` operator returns a new expression, it can't be used to check for equality. Instead the ``.equivalent`` method should be used:

**TODO: Implement this using** ``expression.equivalent`` **!**
