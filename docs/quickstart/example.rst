Simple Example
=====================

This page provides a quick example of how to use Formulate to convert between different expression formats.

Basic Usage
------------------------

The most basic usage involves calling ``from_$BACKEND`` and then ``to_$BACKEND``, where ``$BACKEND`` is the format you're converting from or to.

Converting from ROOT to numexpr
--------------------------------------------------------------------------------------------------------------------------------------------

Here's an example of converting a ROOT expression to numexpr:

.. jupyter-execute::
    :hide-code:

    import formulate

.. code-block:: python

    import formulate

    # TODO: this fails?
    # Create an expression object from a ROOT expression
    momentum = formulate.from_root('TMath::Sqrt(X_PX**2 + X_PY**2 + X_PZ**2)')

    # Convert to numexpr format
    numexpr_expression = momentum.to_numexpr()
    print(numexpr_expression)
    # Output: 'sqrt(((X_PX ** 2) + (X_PY ** 2) + (X_PZ ** 2)))'

    # You can also convert back to ROOT format
    root_expression = momentum.to_root()
    print(root_expression)
    # Output: 'TMath::Sqrt(((X_PX ** 2) + (X_PY ** 2) + (X_PZ ** 2)))'

Converting from numexpr to ROOT
--------------------------------------------------------------------------------------------------------------------------------------------

Similarly, you can convert from numexpr to ROOT:

.. code-block:: python



    # TODO: this fails?
    # Create an expression object from a numexpr expression
    selection = formulate.from_numexpr('X_PT > 5 & (Mu_NHits > 3 | Mu_PT > 10)')

    # Convert to ROOT format
    root_expression = selection.to_root()
    print(root_expression)
    # Output: '(X_PT > 5) && ((Mu_NHits > 3) || (Mu_PT > 10))'

    # You can also convert back to numexpr format
    numexpr_expression = selection.to_numexpr()
    print(numexpr_expression)
    # Output: '(X_PT > 5) & ((Mu_NHits > 3) | (Mu_PT > 10))'

Using the Converted Expressions
-------------------------------------------------------------------------------------------------------------------------------------------

Once you have converted an expression, you can use it with the appropriate backend:

With numexpr:

.. jupyter-execute::

    import numpy as np
    import numexpr as ne

    # Create some sample data
    data = {
        'X_PT': np.array([3, 6, 9, 12]),
        'Mu_NHits': np.array([2, 4, 1, 5]),
        'Mu_PT': np.array([8, 5, 12, 7])
    }

    # Use the converted numexpr expression
    selection = formulate.from_numexpr('X_PT > 5')  # TODO: remove, take from above
    result = ne.evaluate(selection.to_numexpr(), local_dict=data)
    print(result)
    # Output: [False  True  True  True]

With ROOT (pseudo-code, as actual implementation depends on your ROOT setup):

.. code-block:: python

    # Assuming you have a ROOT TTree with branches X_PT, Mu_NHits, and Mu_PT
    tree.Draw(">>eventList", selection.to_root())

    # Now you can use the eventList to process selected events
    # ...
