Common Issues
===========================================================================

.. _issues-modulo:

``%`` does not mean the same thing in ROOT and numexpr
---------------------------------------------------------------------------

``a % b`` is valid in both languages, and formulate converts it in either
direction without complaint. The two engines do not compute the same thing,
however, so this is the one conversion that can silently change the meaning of
an expression.

ROOT's ``TTreeFormula`` truncates both operands to integers and then applies
C's ``%``, whose result takes the sign of the *dividend*. numexpr (and NumPy)
perform floating-point modulo, whose result takes the sign of the *divisor*:

.. list-table::
   :header-rows: 1
   :widths: 20 20 30 30

   * - ``a``
     - ``b``
     - ROOT
     - numexpr
   * - ``7.0``
     - ``3.0``
     - ``1.0``
     - ``1.0``
   * - ``7.5``
     - ``3.0``
     - ``1.0``
     - ``1.5``
   * - ``-7.0``
     - ``3.0``
     - ``-1.0``
     - ``2.0``
   * - ``-7.5``
     - ``3.0``
     - ``-1.0``
     - ``1.5``
   * - ``7.0``
     - ``-3.0``
     - ``1.0``
     - ``-2.0``
   * - ``0.5``
     - ``3.0``
     - ``0.0``
     - ``0.5``

The two agree only when both operands are non-negative whole numbers. Put
differently, ROOT computes ``fmod(int(a), int(b))`` while numexpr computes the
floating-point remainder.

formulate does not try to paper over this. Reproducing ROOT's behaviour in
numexpr would require emitting something like ``fmod(trunc(a), trunc(b))``
rather than an operator, and numexpr's behaviour has no ``TTreeFormula``
spelling at all, so there is no faithful translation to offer in either
direction. If an expression you intend to convert uses ``%``, check that the
values it will see make the two definitions agree.

Note also that ``%`` is specific to ``TTreeFormula``, the evaluator that
formulate's ROOT syntax targets. ``TFormula`` compiles to C++, where ``%`` is
integer-only, and will refuse to compile it against floating-point branches.

Constructs with no equivalent raise rather than approximating
---------------------------------------------------------------------------

``%`` above is the exception. Everything else that cannot be expressed in the
target language raises ``ValueError`` instead of producing something subtly
different:

.. code-block:: pycon

   >>> formulate.from_root("arr[0]").to_numexpr()
   ValueError: Matrix operations are forbidden in NumExpr.
   >>> formulate.from_root("TMath::Infinity()").to_numexpr()
   ValueError: Constant "inf" is not supported in NumExpr.
   >>> formulate.from_numexpr("where(a, b, c)").to_root()
   ValueError: Function "where" is not supported in ROOT.

Two that are easy to trip over:

* ``TMath::Min(a, b)`` and ``TMath::Max(a, b)`` are element-wise, whereas
  numexpr's ``min`` and ``max`` reduce a single array. They convert to
  ``np.minimum`` and ``np.maximum`` for ``to_python()``, but have no numexpr
  form. Note that ``Min$(arr)`` and ``Max$(arr)`` *are* the reductions, and do
  convert to numexpr's ``min`` and ``max``.
* numexpr's ``contains()`` is a string operation with no ROOT or NumPy
  counterpart.

``^`` is exponentiation in ROOT and XOR in numexpr
---------------------------------------------------------------------------

formulate handles this correctly, but the same character meaning two different
things is worth knowing about when reading a converted expression:

.. code-block:: pycon

   >>> formulate.from_root("a^b").to_numexpr()
   '(a ** b)'
   >>> formulate.from_numexpr("a^b").to_numexpr()
   '(a ^ b)'
   >>> formulate.from_numexpr("a^b").to_root()
   ValueError: Operator "xor" is not supported in ROOT.

ROOT has no XOR operator at all, since it spells exponentiation with ``^``, so
a numexpr expression using XOR cannot be converted.

.. _issues-logical-binding:

Logical operators bind differently in the two languages
---------------------------------------------------------------------------

ROOT's ``&&`` and ``||`` are logical operators and bind *looser* than a
comparison, as in C. numexpr's ``&`` and ``|`` are bitwise and bind *tighter*
than a comparison, as in Python. Each parser follows its own language, so the
same-looking expression is grouped differently:

.. code-block:: pycon

   >>> formulate.from_root("a && b < c").to_root()
   '(a && (b < c))'
   >>> formulate.from_numexpr("a & b < c").to_numexpr()
   '((a & b) < c)'

This is why ``a < b & c < d`` is rejected in numexpr: ``&`` binds tighter, so
it parses as the chained comparison ``a < (b & c) < d``, which is not
supported. Write ``(a < b) & (c < d)`` instead.

Named constants do not survive a round trip through numexpr
---------------------------------------------------------------------------

numexpr has no symbolic constants, so formulate substitutes their numeric
values. Converting back to ROOT therefore yields the number rather than the
original name:

.. code-block:: pycon

   >>> formulate.from_root("TMath::Pi()").to_numexpr()
   '3.141592653589793'
   >>> formulate.from_numexpr("3.141592653589793").to_root()
   '3.141592653589793'

The value is preserved; only the spelling is lost.
