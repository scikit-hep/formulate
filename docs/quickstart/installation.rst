Installation
===================

Formulate needs Python 3.10 or newer, and can be installed with pip, with
conda, or from source. It is a pure-Python package with three small
dependencies (``lark``, ``hepunits`` and ``ordered-set``); notably, it does
**not** require ROOT or NumExpr, since it only reads and writes their syntax.

Using pip
------------------------

The recommended way to install Formulate is using pip, ideally inside a virtual
environment:

.. code-block:: bash

    pip install formulate

For development or to get the latest unreleased changes, you can install directly from GitHub:

.. code-block:: bash

    pip install git+https://github.com/scikit-hep/formulate.git

Using conda
------------------------

Formulate is also available on conda-forge:

.. code-block:: bash

    conda install -c conda-forge formulate

The ``-c conda-forge`` is only needed if you do not already have the
conda-forge channel configured.

From Source
------------------------

To install Formulate from source:

1. Clone the repository:

   .. code-block:: bash

       git clone https://github.com/scikit-hep/formulate.git
       cd formulate

2. Install in development mode:

   .. code-block:: bash

       pip install -e .

   Add the ``dev`` extra — ``pip install -e ".[dev]"`` — if you intend to run
   the tests, the linters or the docs build. See
   :doc:`../contributing/contributing` for what that gets you.

Verifying Installation
------------------------------------------------

To verify that Formulate is installed correctly, you can run:

.. jupyter-execute::

    import formulate

    print(formulate.__version__)

The command-line interface is installed alongside the library:

.. code-block:: bash

    formulate --from-root 'TMath::Sqrt(x)' --to-numexpr
