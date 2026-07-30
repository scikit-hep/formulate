[![Actions Status][actions-badge]][actions-link]
[![Documentation Status][rtd-badge]][rtd-link]
[![codecov](https://codecov.io/gh/scikit-hep/formulate/graph/badge.svg?token=W5wXQ9wcvN)](https://codecov.io/gh/scikit-hep/formulate)

[![PyPI version][pypi-version]][pypi-link]
[![Conda-Forge][conda-badge]][conda-link]
[![PyPI platforms][pypi-platforms]][pypi-link]

[![GitHub Discussion][github-discussions-badge]][github-discussions-link]
[![Scikit-HEP][sk-badge]](https://scikit-hep.org/)

<!-- prettier-ignore-start -->
[actions-badge]:            https://github.com/scikit-hep/formulate/actions/workflows/ci.yml/badge.svg
[actions-link]:             https://github.com/Scikit-HEP/formulate/actions
[conda-badge]:              https://img.shields.io/conda/vn/conda-forge/formulate
[conda-link]:               https://github.com/conda-forge/formulate-feedstock
[github-discussions-badge]: https://img.shields.io/static/v1?label=Discussions&message=Ask&color=blue&logo=github
[github-discussions-link]:  https://github.com/Scikit-HEP/formulate/discussions
[pypi-link]:                https://pypi.org/project/formulate/
[pypi-platforms]:           https://img.shields.io/pypi/pyversions/formulate
[pypi-version]:             https://img.shields.io/pypi/v/formulate
[rtd-badge]:                https://readthedocs.org/projects/formulate/badge/?version=latest
[rtd-link]:                 https://formulate.readthedocs.io/latest/?badge=latest
[sk-badge]:                 https://scikit-hep.org/assets/images/Scikit--HEP-Project-blue.svg

<!-- prettier-ignore-end -->

# Formulate

Easy conversions between different styles of expressions. Formulate converts in
either direction between
[ROOT](https://root.cern.ch/doc/master/classTFormula.html) (`TTreeFormula`) and
[numexpr](https://numexpr.readthedocs.io/en/latest/user_guide.html) style
expressions, and can also render a parsed expression as plain Python using
NumPy functions.

It needs neither ROOT nor numexpr installed — it reads and writes their syntax,
it does not evaluate anything — and it knows the places where the two languages
disagree, such as `&&` and `&` binding differently against comparisons, or `^`
meaning exponentiation in one and XOR in the other.

Full documentation: <https://formulate.readthedocs.io/>

## Installation

Install formulate like any other Python package, ideally inside a virtual environment:

```bash
pip install formulate
```

or using conda:

```bash
conda install -c conda-forge formulate
```

(`-c conda-forge` is only needed if you don't have the `conda-forge` channel already configured)

## Roadmap and releases

For the roadmap, planned features, breaking changes and versioning please see the [roadmap](https://github.com/scikit-hep/formulate/discussions/61).

## Usage

### API

The most basic usage involves calling `from_$BACKEND` and then `to_$BACKEND`, for example when starting with a ROOT style expression:

```pycon
>>> import formulate
>>> momentum = formulate.from_root("TMath::Sqrt(X_PX**2 + X_PY**2 + X_PZ**2)")
>>> momentum
Call(function='sqrt', arguments=[BinaryOperator(operator='add', left=BinaryOperator(operator='add', left=BinaryOperator(operator='pow', left=Symbol(name='X_PX'), right=Literal(value=2)), right=BinaryOperator(operator='pow', left=Symbol(name='X_PY'), right=Literal(value=2))), right=BinaryOperator(operator='pow', left=Symbol(name='X_PZ'), right=Literal(value=2)))])
>>> momentum.to_numexpr()
'sqrt((((X_PX ** 2) + (X_PY ** 2)) + (X_PZ ** 2)))'
>>> momentum.to_root()
'TMath::Sqrt((((X_PX ** 2) + (X_PY ** 2)) + (X_PZ ** 2)))'
```

Similarly, when starting with a `numexpr` style expression:

```pycon
>>> my_selection = formulate.from_numexpr("(X_PT > 5) & ((Mu_NHits > 3) | (Mu_PT > 10))")
>>> my_selection.to_root()
'((X_PT > 5) && ((Mu_NHits > 3) || (Mu_PT > 10)))'
>>> my_selection.to_numexpr()
'((X_PT > 5) & ((Mu_NHits > 3) | (Mu_PT > 10)))'
```

Any parsed expression can also be rendered as Python, using NumPy for the
functions. This direction is output-only — there is no `from_python`:

```pycon
>>> momentum.to_python()
'np.sqrt((((X_PX ** 2) + (X_PY ** 2)) + (X_PZ ** 2)))'
```

Parsing is separate from rendering, so parse once and convert as many times as
you like. An expression also reports what it refers to, which is how you work
out what a selection needs to read:

```pycon
>>> expression = formulate.from_root("TMath::Sqrt(px**2 + py**2) > 5 * TMath::Pi() + 1.5")
>>> list(expression.variables)
['px', 'py']
>>> list(expression.named_constants)
['pi']
>>> list(expression.unnamed_constants)
[2, 5, 1.5]
```

### CLI

The package also provides a command-line interface for converting expressions between different styles. To use it, simply run the `formulate` command followed by the input expression and the desired output.

```bash
$ formulate --from-root '(A && B) || TMath::Sqrt(A)' --to-numexpr
((A & B) | sqrt(A))

$ formulate --from-numexpr '(A & B) | sqrt(A)' --to-root
((A && B) || TMath::Sqrt(A))

$ formulate --from-root 'TMath::Sqrt(A)' --to-python
np.sqrt(A)

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
```

Run `formulate --help` for the full list of options.

## Documentation

- [Full documentation](https://formulate.readthedocs.io/)
- [Supported expressions](https://formulate.readthedocs.io/latest/guide/expressions.html) —
  every operator, function and constant, and how each is spelled in each language
- [Common issues](https://formulate.readthedocs.io/latest/guide/issues.html) —
  where the languages disagree, and what formulate does about it
- [API reference](https://formulate.readthedocs.io/latest/api/api.html)
- [Contributing](https://formulate.readthedocs.io/latest/contributing/contributing.html)
