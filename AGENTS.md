# AGENTS.md

This file provides guidance to agents when working with code in this repository.

## What this is

`formulate` converts expressions between ROOT/`TTreeFormula` syntax, NumExpr syntax, and
(output-only) plain Python/NumPy. Public API is `formulate.from_root(str)` /
`formulate.from_numexpr(str)` returning an `AST`, then `.to_root()`, `.to_numexpr()`,
`.to_python()`, or the `.variables` / `.named_constants` / `.unnamed_constants` properties.
There is also a `formulate` CLI (`src/formulate/cli.py`).

## Commands

```bash
pip install -e ".[dev]"     # dev install
prek install                # hook runner; reads .pre-commit-config.yaml

pytest                      # all tests
pytest tests/test_root.py -k tmath_min       # single file / single test
pytest --cov=formulate --cov-branch          # with coverage

nox                         # default: lint + pylint + tests
nox -s tests                # tests in an isolated env
nox -s docs -- --serve      # build and serve the Sphinx docs
nox -s coverage
prek run --all-files        # ruff, ruff-format, mypy (strict, src only), codespell, zizmor
```

`prek` is a drop-in, much faster reimplementation of `pre-commit` — same
`.pre-commit-config.yaml`, same hook IDs, same subcommands. It is what the `dev` extra installs
and what `nox -s lint` runs. pre-commit.ci (configured by the `ci:` block in the config) still
runs `pre-commit` proper on pull requests, so hooks must stay compatible with both.

`tests/test_constants.py` is the only file that evaluates expressions with the real engines.
It imports `numexpr` at module scope — so `numexpr` is in the `test` extra, not just `docs`,
or the suite cannot be collected at all — and `importorskip`s `ROOT`, which CI installs only
on Linux/Python 3.10. So `.[test]` runs everything except the ROOT half, which skips.

## Architecture

Pipeline, in order:

1. **Grammar** — `src/formulate/resources/{root,numexpr}_grammar.lark`, parsed by lark's LALR
   parser (cached per backend in `__init__.py`). Each grammar encodes _its own_ language's
   precedence: ROOT follows C++ (`&&`/`||` bind looser than comparisons, `^` is exponentiation,
   `!` is logical not), NumExpr follows Python (`&`/`|` bind tighter than comparisons, `^` is
   XOR, chained comparisons are rejected). Rule aliases (`-> add`, `-> inv`, `-> multi_out`)
   are the canonical operator names used downstream.
2. **`toast.py`** — walks the lark parse tree and emits the backend-neutral AST. This is where
   surface names are normalized: namespaces (`TMath::`), the trailing `$` on ROOT array
   functions, function aliases (`atan2` → `arctan2`), and constant aliases (`e_num` → `exp1`).
   Unknown names raise here. `toast` itself is one `_traversal.fold` call; `_expand` is what
   handles a single parse-tree node, returning the children still to convert plus a builder
   that assembles the AST node from them.
3. **`AST.py`** — six frozen dataclass node types (`Literal`, `Symbol`, `UnaryOperator`,
   `BinaryOperator`, `Matrix`, `Call`) plus a `_Backend` descriptor. A node type implements
   exactly three things: `_children()`, `_format(*parts)` for `str()`, and
   `_serializer(backend)`, which returns the builder that joins its already-serialized
   children. Every traversal lives on the base class and is iterative: `__str__` and
   `_to_backend` are both `_traversal.fold` calls, and `_walk` backs `variables` /
   `named_constants` / `unnamed_constants`. Nothing here recurses, so depth is bounded by
   memory, not by the stack. The three public `to_*` methods just pass the corresponding
   `_Backend` instance (`_ROOT`, `_NUMEXPR`, `_PYTHON`). There is no per-backend visitor
   class — a new backend is a new `_Backend` literal plus new tables. Every node validates in
   `_serializer`, which runs before its children are visited, so an expression with more than
   one unsupported construct reports the outermost one. Keep new checks there: the builder
   `_serializer` returns should only join strings, and moving a check into it would silently
   change which error surfaces.
4. **`identifiers.py`** — the hand-maintained lookup tables. `FUNCTIONS`/`CONSTANTS` are the
   canonical name sets; `ROOT_*`/`NUMEXPR_*`/`PYTHON_*` map canonical names to each backend's
   spelling. A name absent from a backend's table is how "unsupported" is expressed — the
   serializer raises `ValueError` on the `None` lookup.

Cutting across all of it, `_traversal.py` holds the single bottom-up walk both stages 2 and 3
are built on. It is underscore-prefixed because unlike the modules above it names no part of
the conversion — `fold` is a generic utility, is not documented, and nothing outside the
package should import it.

Two invariants worth knowing before editing:

- **The AST is canonical, not any backend's dialect.** Node operator/function strings
  (`"add"`, `"inv"`, `"tmath_min"`) are internal identifiers. Never leak a backend spelling
  into the AST or into `toast.py`.
- **Serialization is fully parenthesized and deterministic**, which makes the serialized string
  a canonical form. Most tests exploit this: they parse two spellings and assert the output
  strings are identical, rather than evaluating numerically. Changing the parenthesization
  rules (`_Backend.unparenthesized_ops`) will move a lot of expected strings.

### Adding a function or constant

Add the canonical name to `FUNCTIONS`/`CONSTANTS`, then an entry in each backend map where it
is supported, plus any spelling in `FUNCTION_ALIASES` / `CONSTANTS_ALIASES` /
`CONSTANTS_FUNCTION_ALIASES`. `tests/test_identifiers.py` drives every table entry through the
parser and cross-checks the tables against each other, so a declared-but-unmapped name fails
loudly. If the name has both a scalar `TMath::` form and an array `$` form (as with
`Min`/`Max`), it needs the `tmath_`-prefixed qualified variant — see `_get_function_name` —
and an entry in `FUNCTION_DISPLAY_NAMES`, since that canonical name is one nobody writes and
would be meaningless in an error message.
Each table also carries an attribute docstring, which is what the API page renders; the
name additionally needs a row in the tables in `docs/guide/expressions.rst`, which nothing
checks automatically.

### Docs

`docs/` is Sphinx (RTD theme, `nox -s docs`, `-- --serve` to serve). Two things to know
before editing it:

- **Examples execute at build time.** Narrative pages use `jupyter-execute`, not
  `code-block`, wherever an output is shown, so a stale example fails the build instead of
  lying on the website. Keep it that way — if you add an example with output, run it.
- **Which page owns what.** `guide/expressions.rst` is the reference for every supported
  operator, function and constant, and how each is spelled per backend; `guide/issues.rst`
  is the reference for where the languages disagree. Behaviour changes belong in one of
  those two. API pages are `automodule`/`autodata` over the docstrings, so the docstring is
  where API prose goes, not the `.rst`.

### Unsupported constructs

Anything with no faithful equivalent in the target raises `ValueError` rather than emitting
something subtly different. The single documented exception is `%`, which converts silently
even though ROOT truncates its operands to integers and NumExpr does float modulo. See
`docs/guide/issues.rst`; that file is the reference for the cross-language gotchas and should
be kept in sync with behaviour changes.

`exceptions.py` builds `ParseError` with heuristic suggestions (`debug_root`, `debug_numexpr`)
based on regex-scanning the source expression — e.g. suggesting `&&` when a ROOT expression
contains a lone `&`. New syntax that people commonly get wrong belongs here.

## Constraints to respect

- **Coverage is enforced at 100%** for both project and patch (`codecov.yml`, threshold 0).
  Genuinely unreachable code is marked `# pragma: no cover`; prefer deleting dead branches.
- `filterwarnings = ["error"]` and `xfail_strict` are on — a new warning fails the suite.
- mypy runs `--strict` over `src` only; the package ships `py.typed`.
- Supported Python is 3.10+, and the CI matrix includes Windows and free-threaded 3.14.
- **No recursive tree walks.** `_traversal.fold` and `AST._walk` are the only two, and both
  use an explicit stack, so peak frame depth is a small constant whatever the expression size.
  `tests/test_performance.py` runs at CPython's default recursion limit on purpose and nests
  1,000 levels deep, so a recursive walk added back anywhere fails there. The sizes in that file are
  bounded by its 3s timing budget on the slowest job (Windows/3.10 under coverage), not by the
  stack.
- Version comes from git tags via `hatch-vcs` (`_version.py` is generated; do not edit).
