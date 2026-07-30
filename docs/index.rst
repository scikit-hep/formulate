
Welcome to Formulate's documentation!
====================================================================

.. image:: https://scikit-hep.org/assets/images/Scikit--HEP-Project-blue.svg
   :target: https://scikit-hep.org/

Formulate is a Python library for easy conversions between different styles of expressions.
It converts in either direction between `ROOT <https://root.cern.ch/doc/master/classTFormula.html>`_
(``TTreeFormula``) and `numexpr <https://numexpr.readthedocs.io/en/latest/user_guide.html>`_
syntax, and can also render any parsed expression as plain Python using NumPy functions.

.. code-block:: pycon

   >>> import formulate
   >>> formulate.from_root("TMath::Sqrt(px**2 + py**2) > 10").to_numexpr()
   '(sqrt(((px ** 2) + (py ** 2))) > 10)'

Install it with ``pip install formulate`` or ``conda install -c conda-forge formulate``,
then start with the :doc:`quickstart/introduction`.

.. toctree::
   :maxdepth: 2
   :caption: Quickstart

   quickstart/introduction
   quickstart/installation
   quickstart/example
   quickstart/whatsnew

.. toctree::
   :maxdepth: 2
   :caption: Guide

   guide/expressions
   guide/speed
   guide/issues

.. toctree::
   :maxdepth: 2
   :caption: API

   api/api

.. toctree::
   :maxdepth: 2
   :caption: Contributing

   contributing/contributing

.. toctree::
   :maxdepth: 2
   :caption: Project

   project/citations
   project/contact

.. toctree::
   :maxdepth: 2
   :caption: Ask a Question

   questions/questions

Indices and tables
==================================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
