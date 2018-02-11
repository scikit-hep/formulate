🚧 **Formulate is currently under construction and not yet
ready for production use! Expect things to break!** 🚧

Formulate
=========

|Build Status| |Coverage Status| |PyPI|

Easy conversions between different styles of expressions. Formulate
currently supports converting between
`ROOT <https://root.cern.ch/doc/master/classTFormula.html>`__ and
`numexpr <https://numexpr.readthedocs.io/en/latest/user_guide.html>`__
style expressions.

.. |Build Status| image:: https://travis-ci.org/chrisburr/formulate.svg?branch=master
   :target: https://travis-ci.org/chrisburr/formulate
.. |Coverage Status| image:: https://coveralls.io/repos/github/chrisburr/formulate/badge.svg?branch=master
   :target: https://coveralls.io/github/chrisburr/formulate?branch=master
.. |PyPI| image:: https://badge.fury.io/py/formulate.svg
   :target: https://pypi.python.org/pypi/formulate/


Installation
------------

Install formulate like any other Python package:

.. code-block:: bash

    pip install --user formulate

or similar (use ``sudo``, ``virtualenv``, or ``conda`` if you wish).


Usage
-----

Command line usage
""""""""""""""""""

.. code-block:: bash

    $ python -m formulate --from-root '(A && B) || TMath::Sqrt(A)' --to-numexpr
    (A & B) | sqrt(A)

API
"""

**TODO**


The `Expression` Object
-----------------------

**TODO**
