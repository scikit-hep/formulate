Simple Example
=====================

This page walks through the whole of Formulate's interface on one small example.
Every output below is produced by running the code shown, so it is what you will
get too.

Basic Usage
------------------------

The library has two entry points, ``from_root`` and ``from_numexpr``. Each
parses a string and returns an expression object, which then knows how to render
itself in any of the supported styles.

Converting from ROOT to numexpr
--------------------------------------------------

.. jupyter-execute::

    import formulate

    momentum = formulate.from_root("TMath::Sqrt(X_PX**2 + X_PY**2 + X_PZ**2)")

    print(momentum.to_numexpr())

Nothing about the object remembers where it came from, so it converts back just
as happily:

.. jupyter-execute::

    print(momentum.to_root())

Note that the output is fully parenthesized. Formulate does not try to reproduce
your spacing or drop redundant brackets — the three languages disagree about
precedence, and being explicit is how a conversion stays correct.

Converting from numexpr to ROOT
--------------------------------------------------

The same in the other direction:

.. jupyter-execute::

    selection = formulate.from_numexpr("(X_PT > 5) & ((Mu_NHits > 3) | (Mu_PT > 10))")

    print(selection.to_root())
    print(selection.to_numexpr())

Converting to Python
--------------------------------------------------

There is a third output style: plain Python, using NumPy for the functions.
There is no ``from_python`` — this direction is output-only.

.. jupyter-execute::

    print(momentum.to_python())

Function names come out prefixed with ``np.``, so the result is meant to be
evaluated somewhere ``numpy`` has been imported as ``np``.

Inspecting an expression
--------------------------------------------------

An expression also reports what it refers to, which is how you find out what to
read from a file before you read it:

.. jupyter-execute::

    expr = formulate.from_root("TMath::Sqrt(px**2 + py**2) > 5 * TMath::Pi() + 1.5")

    print(list(expr.variables))
    print(list(expr.named_constants))
    print(list(expr.unnamed_constants))

Using the Converted Expressions
--------------------------------------------------

Once converted, an expression is just a string that the target engine accepts.
With numexpr:

.. jupyter-execute::

    import numpy as np
    import numexpr as ne

    data = {
        "X_PT": np.array([3, 6, 9, 12]),
        "Mu_NHits": np.array([2, 4, 1, 5]),
        "Mu_PT": np.array([8, 5, 12, 7]),
    }

    print(ne.evaluate(selection.to_numexpr(), local_dict=data))

The Python output can be handed to ``eval`` in the same way:

.. jupyter-execute::

    print(eval(selection.to_python(), {"np": np}, data))

With ROOT, the converted string goes wherever a ``TTreeFormula`` would:

.. code-block:: python

    # Assuming a TTree with branches X_PT, Mu_NHits and Mu_PT
    tree.Draw(">>eventList", selection.to_root())

When a conversion is not possible
--------------------------------------------------

Not everything has an equivalent everywhere. Rather than emit something that
looks right and computes something else, Formulate raises:

.. jupyter-execute::

    try:
        formulate.from_root("TMath::Infinity()").to_numexpr()
    except ValueError as error:
        print(error)

The :doc:`../guide/issues` page lists the cases worth knowing about in advance.

CLI Usage
--------------------------------------------------

The same conversions are available from the shell. One option says what to
parse, one says what to print:

.. code-block:: bash

    $ formulate --from-root '(A && B) || TMath::Sqrt(A)' --to-numexpr
    ((A & B) | sqrt(A))

    $ formulate --from-numexpr '(A & B) | sqrt(A)' --to-root
    ((A && B) || TMath::Sqrt(A))

    $ formulate --from-root 'TMath::Sqrt(A)' --to-python
    np.sqrt(A)

The introspection properties have flags too, printing one name per line so the
output can be piped into something else:

.. code-block:: bash

    $ formulate --from-root '(A && B) || TMath::Sqrt(1.23) * e_num**1.2 + 5*pi' --variables
    A
    B

    $ formulate --from-root '(A && B) || TMath::Sqrt(1.23) * e_num**1.2 + 5*pi' --named-constants
    exp1
    pi

    $ formulate --from-root '(A && B) || TMath::Sqrt(1.23) * e_num**1.2 + 5*pi' --unnamed-constants
    1.23
    1.2
    5

Run ``formulate --help`` for the full list.
