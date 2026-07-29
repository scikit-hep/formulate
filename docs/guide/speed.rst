Performance Considerations
================================================

formulate is a translator, not an evaluator. It runs once, on a string, before
any data is touched; the work of evaluating the expression belongs to ROOT,
NumExpr or NumPy afterwards. So the only performance question formulate raises
is whether translating is cheap enough to ignore, and for the expressions people
actually write it is: parsing takes on the order of a hundred microseconds, and
rendering an already-parsed expression an order of magnitude less than that.

That said, a few things are worth knowing if you convert expressions in a loop.

Parse once, render many times
------------------------------------------------

Parsing is by far the more expensive half, and the result is immutable, so an
expression you convert to several backends — or convert once and also inspect —
should be parsed once and kept:

.. jupyter-execute::

   import formulate

   expr = formulate.from_root("TMath::Sqrt(px**2 + py**2) > 10")

   selection = expr.to_numexpr()
   branches = list(expr.variables)

   print(selection, branches)

If the same expression string comes up repeatedly — one per event loop
iteration, say — cache the parsed object rather than the string;
``functools.lru_cache`` over a function that calls
:func:`~formulate.from_root` is enough.

The grammars are compiled lazily, once
------------------------------------------------

Each backend's grammar is compiled into an LALR parser the first time that
backend is used, and then reused for the rest of the process. The first
:func:`~formulate.from_root` in a session therefore costs a few tens of
milliseconds more than the ones after it, and a program that only ever parses
NumExpr never pays for the ROOT grammar at all.

This also means the cost is per process. There is nothing to warm up and
nothing to persist.

Expression size
------------------------------------------------

Cost grows linearly with the size of the expression, and nothing in formulate
recurses — both the parse-tree conversion and the serializers walk the tree with
an explicit stack — so deeply nested expressions are bounded by memory rather
than by Python's recursion limit. An expression a thousand parentheses deep
converts without special handling.

Output is fully parenthesized, so a converted expression is longer than what you
fed in. It does not keep growing, though: re-parsing adds parse-tree depth but
not AST nodes, so converting a converted expression gives the same string back.

.. jupyter-execute::

   once = formulate.from_root("a + b * c").to_root()
   twice = formulate.from_root(once).to_root()
   print(once, twice, once == twice, sep="\n")

That fixed point is what makes the serialized string a canonical form, and it is
what most of the test suite compares against.

What formulate does *not* affect
------------------------------------------------

How fast the converted expression evaluates is entirely up to the target engine.
formulate does not reorder, simplify, or constant-fold anything — ``2 + 2``
converts to ``(2 + 2)``, not ``4`` — because its job is to preserve meaning, and
every engine here does its own optimisation anyway. The one thing it changes is
that named constants become literals when converting to NumExpr, which is a
consequence of NumExpr having no symbolic constants rather than an optimisation.
