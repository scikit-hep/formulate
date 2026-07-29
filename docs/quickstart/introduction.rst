Introduction
======================

What is Formulate?
-------------------------------

Formulate converts expressions between the syntaxes used by different analysis
tools. It is part of the `Scikit-HEP <https://scikit-hep.org/>`_ project, a
collection of Python packages for High Energy Physics data analysis.

It reads:

* `ROOT <https://root.cern.ch/doc/master/classTFormula.html>`_ expressions, as
  understood by ``TTreeFormula`` — ``TMath::Sqrt(x) && y > 2``
* `numexpr <https://numexpr.readthedocs.io/en/latest/user_guide.html>`_
  expressions — ``sqrt(x) & (y > 2)``

and writes either of those, plus plain Python using NumPy functions. The Python
backend is output-only.

The point is that a selection or a derived quantity written once, in whichever
syntax was natural at the time, can be used with whichever tool the analysis
needs later — without hand-translating it and hoping the precedence rules line
up. They do not line up: ``&&`` and ``&`` bind differently against comparisons,
and ``^`` means exponentiation in one language and XOR in the other. Formulate
knows the difference.

Simple example
-----------------------------

Parse with ``from_$BACKEND``, render with ``to_$BACKEND``:

.. jupyter-execute::

    import formulate

    momentum = formulate.from_root("TMath::Sqrt(X_PX**2 + X_PY**2 + X_PZ**2)")

    print(momentum.to_numexpr())
    print(momentum.to_python())

Parsing is separate from rendering, so one parsed expression can be converted as
many times as you like. See :doc:`example` for the same walkthrough in more
detail.

Key features
-------------------------

* Convert between ROOT and numexpr syntax, in either direction
* Render any parsed expression as Python/NumPy source
* Report the variables, named constants and numeric literals an expression uses,
  so you know what a selection will need to read
* Refuse, loudly, to convert what cannot be converted faithfully — the one
  documented exception being ``%``; see :doc:`../guide/issues`
* Parse errors that point at the problem and suggest the fix
* A command-line interface for the same conversions
* No dependency on ROOT or numexpr: Formulate reads and writes their syntax
  without either being installed

What Formulate is not
-------------------------

It is not an evaluator. Formulate translates the text of an expression; running
it against data is the job of ROOT, numexpr or NumPy afterwards. It also does no
simplification — ``2 + 2`` converts to ``(2 + 2)`` — and it does not know the
types of your branches, which is why a handful of constructs are refused rather
than guessed at.
