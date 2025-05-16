# formulate

[![Actions Status][actions-badge]][actions-link]
[![Documentation Status][rtd-badge]][rtd-link]

[![PyPI version][pypi-version]][pypi-link]
[![Conda-Forge][conda-badge]][conda-link]
[![PyPI platforms][pypi-platforms]][pypi-link]

[![GitHub Discussion][github-discussions-badge]][github-discussions-link]
[![Scikit-HEP][sk-badge]](https://scikit-hep.org/)

<!-- prettier-ignore-start -->
[actions-badge]:            https://github.com/scikit-hep/formulate/workflows/unittests/badge.svg
[actions-link]:             https://github.com/Scikit-HEP/formulate/actions
[conda-badge]:              https://img.shields.io/conda/vn/conda-forge/formulate
[conda-link]:               https://github.com/conda-forge/formulate-feedstock
[github-discussions-badge]: https://img.shields.io/static/v1?label=Discussions&message=Ask&color=blue&logo=github
[github-discussions-link]:  https://github.com/Scikit-HEP/formulate/discussions
[pypi-link]:                https://pypi.org/project/formulate/
[pypi-platforms]:           https://img.shields.io/pypi/pyversions/formulate
[pypi-version]:             https://img.shields.io/pypi/v/formulate
[rtd-badge]:                https://readthedocs.org/projects/formulate/badge/?version=latest
[rtd-link]:                 https://formulate.readthedocs.io/en/latest/?badge=latest
[sk-badge]:                 https://scikit-hep.org/assets/images/Scikit--HEP-Project-blue.svg

<!-- prettier-ignore-end -->

Formulate
=========

Easy conversions between different styles of expressions. Formulate
currently supports converting between
[ROOT](https://root.cern.ch/doc/master/classTFormula.html) and
[numexpr](https://numexpr.readthedocs.io/en/latest/user_guide.html)
style expressions.



Installation
------------

Install formulate like any other Python package:

```bash
pip install --user formulate
```
or similar (use `sudo`, `virtualenv`, or `conda` if you wish).


Usage
-----

### API


The most basic usage involves calling `from_$BACKEND` and then `to_$BACKEND`, for example when starting with a ROOT style expression:

```python
>>> import formulate
>>> momentum = formulate.from_root('TMath::Sqrt(X_PX**2 + X_PY**2 + X_PZ**2)')
>>> momentum
Expression<SQRT>(Expression<ADD>(Expression<POW>(Variable(X_PX), UnnamedConstant(2)), Expression<POW>(Variable(X_PY), UnnamedConstant(2)), Expression<POW>(Variable(X_PZ), UnnamedConstant(2))))
>>> momentum.to_numexpr()
'sqrt(((X_PX ** 2) + (X_PY ** 2) + (X_PZ ** 2)))'
>>> momentum.to_root()
'TMath::Sqrt(((X_PX ** 2) + (X_PY ** 2) + (X_PZ ** 2)))'
```
Similarly, when starting with a `numexpr` style expression:

```python
>>> my_selection = formulate.from_numexpr('X_PT > 5 & (Mu_NHits > 3 | Mu_PT > 10)')
>>> my_selection.to_root()
'(X_PT > 5) && ((Mu_NHits > 3) || (Mu_PT > 10))'
>>> my_selection.to_numexpr()
'(X_PT > 5) & ((Mu_NHits > 3) | (Mu_PT > 10))'
```
