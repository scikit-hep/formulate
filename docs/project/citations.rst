Citing Formulate
======================

If formulate was useful in work you are publishing, please cite it. There are
two things worth citing: the package itself, and the Scikit-HEP project it
belongs to.

Citing the package
----------------------------------------------

formulate does not yet have its own DOI, so cite it as software, giving the
version you used. You can get that from the package:

.. jupyter-execute::

    import formulate

    print(formulate.__version__)

.. code-block:: bibtex

    @software{formulate,
      author  = {Burr, Chris and Roy, Aryan and Eschle, Jonas and
                 {The Scikit-HEP admins}},
      title   = {formulate: easy conversions between different styles of expressions},
      url     = {https://github.com/scikit-hep/formulate},
      version = {1.0.1},
      year    = {2025},
    }

Replace ``version`` and ``year`` with the ones you actually used — conversions
and constant names have changed between releases, so the version is the part
that makes the citation reproducible. The :doc:`../quickstart/whatsnew` page
records what changed when.

Citing Scikit-HEP
----------------------------------------------

formulate is part of `Scikit-HEP <https://scikit-hep.org/>`_. If you are citing
the ecosystem as a whole, or several of its packages, the project paper is the
reference to use:

    E. Rodrigues et al., *The Scikit-HEP Project — overview and prospects*,
    EPJ Web Conf. **245**, 06028 (2020),
    `doi:10.1051/epjconf/202024506028 <https://doi.org/10.1051/epjconf/202024506028>`_,
    `arXiv:2007.03577 <https://arxiv.org/abs/2007.03577>`_.

.. code-block:: bibtex

    @article{scikit-hep,
      author    = {Rodrigues, Eduardo and others},
      title     = {The Scikit HEP Project -- overview and prospects},
      journal   = {EPJ Web Conf.},
      volume    = {245},
      pages     = {06028},
      year      = {2020},
      doi       = {10.1051/epjconf/202024506028},
      eprint    = {2007.03577},
      archivePrefix = {arXiv},
    }

The Scikit-HEP `citation page <https://scikit-hep.org/citing>`_ has the
up-to-date version of this, and covers the other packages in the project.

Citing what formulate converts *to*
----------------------------------------------

formulate translates expressions; the evaluation is done by something else. If
the analysis you are describing leaned on that engine's behaviour, cite it as
well — `ROOT <https://root.cern/>`_ or
`NumExpr <https://numexpr.readthedocs.io/>`_ as appropriate, and
`NumPy <https://numpy.org/citing-numpy/>`_ for :meth:`~formulate.AST.AST.to_python`
output.
