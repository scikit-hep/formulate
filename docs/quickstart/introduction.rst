Introduction
======================

What is Formulate?
-------------------------------

Formulate is a Python library that provides easy conversions between different styles of expressions. It is part of the `Scikit-HEP <https://scikit-hep.org/>`_ project, a collection of Python packages for High Energy Physics (HEP) data analysis.

Currently, Formulate supports converting between:

* `ROOT <https://root.cern.ch/doc/master/classTFormula.html>`_ style expressions (used in the TTreeFormula class)
* `numexpr <https://numexpr.readthedocs.io/en/latest/user_guide.html>`_ style expressions

This allows physicists and data analysts to write expressions in their preferred syntax and convert them to other formats as needed, facilitating interoperability between different analysis tools and frameworks.

Simple example
-----------------------------

The most basic usage involves calling ``from_$BACKEND`` and then ``to_$BACKEND``, where ``$BACKEND`` is the format you're converting from or to.

.. code-block:: python

    import formulate

    # Create an expression object from a ROOT expression
    momentum = formulate.from_root("TMath::Sqrt(X_PX**2 + X_PY**2 + X_PZ**2)")
    # Convert to numexpr format
    numexpr_expression = momentum.to_numexpr()
    print(numexpr_expression)

    # ... and vice versa

Key Features
-------------------------

* Convert expressions from ROOT to numexpr format
* Convert expressions from numexpr to ROOT format
* Maintain the semantic meaning of expressions during conversion
* Support for mathematical operations, logical operations, and function calls
* Python API for programmatic conversion
