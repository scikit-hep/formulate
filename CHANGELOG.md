# Changelog

## Unreleased

No breaking changes. This is a bug-fix and maintenance release.

### Bug fixes

- `to_python()` raised for every named constant except `inf`, `neginf` and `nan`, because the Python constant table was built from the wrong source. All of them now convert.
- `to_python()` emitted `np.pow`, which only exists in NumPy 2.0 and later; it now emits `np.power`.
- `TMath::Min(a, b)` and `TMath::Max(a, b)`, which are element-wise two-argument functions, were conflated with the `Min$`/`Max$` array reductions and silently round-tripped as the wrong one. They are now distinct, and convert to `np.minimum`/`np.maximum` in Python. They have no numexpr equivalent, and say so rather than converting.
- ROOT's `$` functions used without parentheses, such as a bare `Length$`, are now parsed.
- An index followed by a power, such as `Jet_pt[0]**2`, was a parse error in ROOT.
- Zero-argument calls such as `Length$()` raised an internal error.
- `named_constants` and `unnamed_constants` ignored the indexed expression itself, so `pi[0]` reported no constants.
- `from_root()` and `from_numexpr()` accepted arbitrary keyword arguments and silently ignored them, turning a typo into a no-op.
- The ROOT parse-error hints missed a bare `&` or `|` written without surrounding spaces.
- Converting `TMath::Min`/`TMath::Max` to numexpr reported the internal name (`Function "tmath_min" is not supported`) rather than what was written.

### Improvements

- Expression trees are now walked iteratively throughout, so deeply nested expressions are limited by memory rather than by Python's recursion limit.
- AST nodes are immutable (frozen, slotted dataclasses).
- Each grammar is compiled on first use rather than at import, so parsing only one language costs only one parser.
- The package ships a `py.typed` marker, so type checkers now see its annotations.
- The documentation has been substantially expanded: every supported operator, function and constant is now listed with its spelling in each language, and the API reference is generated from real docstrings.
- Python 3.14, including the free-threaded build, is tested in CI.

## v1.0.1 (16 Oct. 2025)

This release provided significant bug fixes and cleanup with respect to the previous overhaul. The switch to Lark as the parsing backend and the internal AST were kept, but the code was significantly simplified and many issues were ironed out.

### Breaking changes

- A `numexpr` parsing bug was fixed, which had been present since the initial release of `formulate`. Bitwise operator precedence was changed, so some expressions will be interpreted differently, or fail to be parsed if they are not valid `numexpr` expressions. (See bug fixes section for more details.)
- Some constant names were changed. In particular, very generic names are not assumed to be constants and will instead need more specific names. For example `c` is no longer interpreted as the speed of light, so `c_light` should be used instead. Constant names were taken from `hepunits` for consistency within Scikit-HEP.

### Features and improvements

- The CLI interface (which was briefly removed) was reintroduced.
- Added dependency on `hepunits` in order to provide a useful set of constants.
- Added methods to suggest fixes to parsing issues. These will be expanded in the future.

### Bug fixes

- ROOT parsing issues were resolved.
- Various issues with constant and function conversions were resolved.
- Bitwise operator precedence for `numexpr` expressions was fixed. An expression like `x > 1 & x < 3` was being parsed as `(x > 1) & (x < 3)` whereas `numexpr` would actually parse it as `x > (1 & x) < 3`.

### Maintainability improvements

- Added `lark` as a dependency, and moved away from standalone parsers. This simplifies the code and makes future adjustments to the grammar rules much easier.
- Moved function and constant conversions into a central location instead of having them in each `to_*` function. Expressions are converted into a unified internal representation when they are parsed. This makes it easier to identify parsing and conversion issues.
