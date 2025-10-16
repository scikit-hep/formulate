Installation
===================

Formulate can be installed using pip, conda, or by building from source.

Using pip
------------------------

The recommended way to install Formulate is using pip:

.. code-block:: bash

    pip install formulate

For development or to get the latest unreleased changes, you can install directly from GitHub:

.. code-block:: bash

    pip install git+https://github.com/scikit-hep/formulate.git

Using conda
------------------------

Formulate is also available on conda-forge (TODO: not yet:

.. code-block:: bash

    conda install -c conda-forge formulate

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


Verifying Installation
------------------------------------------------

To verify that Formulate is installed correctly, you can run:

.. jupyter-execute::

    import formulate

    print(formulate.__version__)
