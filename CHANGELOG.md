# Changelog

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
