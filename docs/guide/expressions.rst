Supported Expressions
===================================

This page is the reference for what formulate accepts and what it produces: the
operators of each language, the functions and constants it knows, and the
handful of constructs it deliberately refuses.

Three languages are involved. ROOT and NumExpr can each be both an input and an
output; Python is output-only, and is rendered with NumPy function names, so it
is meant to be evaluated somewhere ``numpy`` is imported as ``np``.

.. jupyter-execute::
   :hide-code:

   import formulate

Two things are true of every conversion. Output is **fully parenthesized**,
because the languages disagree about precedence and formulate would rather be
explicit than clever:

.. jupyter-execute::

   print(formulate.from_root("a + b * c").to_numexpr())

And a parsed expression is **immutable and reusable** — parse once, render as
many times as you like:

.. jupyter-execute::

   expr = formulate.from_root("TMath::Sqrt(px**2 + py**2)")
   print(expr.to_root())
   print(expr.to_numexpr())
   print(expr.to_python())

Operators
----------------

Arithmetic
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. list-table::
   :header-rows: 1
   :widths: 25 25 25 25

   * - Operation
     - ROOT
     - NumExpr
     - Python
   * - Addition
     - ``x + y``
     - ``x + y``
     - ``x + y``
   * - Subtraction
     - ``x - y``
     - ``x - y``
     - ``x - y``
   * - Multiplication
     - ``x * y``
     - ``x * y``
     - ``x * y``
   * - Division
     - ``x / y``
     - ``x / y``
     - ``x / y``
   * - Power
     - ``x**y``, ``x^y``, ``TMath::Power(x, y)``
     - ``x**y``
     - ``x**y``
   * - Modulo
     - ``x % y``
     - ``x % y``
     - ``x % y``
   * - Unary plus / minus
     - ``+x``, ``-x``
     - ``+x``, ``-x``
     - ``+x``, ``-x``

Power is the only operator that groups from the right, in all three languages:
``a**b**c`` is ``a**(b**c)``.

.. warning::

   ROOT and NumExpr disagree about what ``%`` computes, and formulate converts
   it in either direction without complaint. It is the one construct that can
   silently change meaning. See :ref:`issues-modulo`.

Comparisons
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

``==``, ``!=``, ``>``, ``<``, ``>=`` and ``<=`` are spelled the same way in all
three languages.

NumExpr does not support chained comparisons, so ``a < b < c`` is rejected on
input; write ``(a < b) & (b < c)``. ROOT accepts chains, because C++ does, but
they mean ``(a < b) < c`` there rather than what they mean in Python — so they
are almost always a mistake worth rewriting too.

Logical operators
~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. list-table::
   :header-rows: 1
   :widths: 25 25 25 25

   * - Operation
     - ROOT
     - NumExpr
     - Python
   * - AND
     - ``x && y``
     - ``x & y``
     - ``x & y``
   * - OR
     - ``x || y``
     - ``x | y``
     - ``x | y``
   * - NOT
     - ``!x``
     - ``~x``
     - ``np.logical_not(x)``
   * - XOR
     - —
     - ``x ^ y``
     - ``x ^ y``

Each parser accepts only its own language's spelling, and tells you which one an
expression needs if you get it wrong:

.. jupyter-execute::

   try:
       formulate.from_numexpr("a && b")
   except formulate.ParseError as error:
       print(error)

Two differences are worth internalising. The operators **bind differently**
against comparisons — ROOT's are logical and bind looser, NumExpr's are bitwise
and bind tighter (see :ref:`issues-logical-binding`) — and **ROOT has no XOR**,
since it spells exponentiation with ``^``, so a NumExpr expression using XOR
cannot be converted to ROOT.

Python's NOT is rendered as ``np.logical_not`` rather than ``~`` on purpose:
ROOT's ``!`` is a logical negation, whereas NumPy's ``~`` is a bitwise
inversion, and they disagree on anything that is not a boolean (``!5`` is ``0``
but ``~5`` is ``-6``).

The ROOT multi-output operator
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

``TTreeFormula`` uses ``:`` to separate the several expressions of a
multi-dimensional draw. formulate parses it, and renders it in Python as the
comma-separated list that Python reads as a tuple:

.. jupyter-execute::

   print(formulate.from_root("px : py : pz").to_root())
   print(formulate.from_root("px : py : pz").to_python())

NumExpr evaluates a single expression and has no equivalent, so converting one
of these raises.

``:`` separates whole expressions rather than combining two values, so it is
only accepted between them -- ``a:b`` and ``a+1 : b*2`` are fine, but
``(a:b)+c`` and ``sqrt(a:b)`` are rejected, as they are by ROOT. This is also
what lets it be the one operator that is never parenthesized: were it allowed
to nest, ``(a:b)+c`` would have to serialize as ``a : b + c`` and would read
back as ``a:(b+c)``.

Indexing
----------------

ROOT indexes with one bracket pair per dimension and Python with a single
comma-separated pair; formulate translates between the two spellings:

.. jupyter-execute::

   print(formulate.from_root("arr[0]").to_root())
   print(formulate.from_root("energies[i][j]").to_python())

NumExpr has no indexing at all — arrays are passed in whole, already sliced — so
an indexed expression cannot be converted to it.

Functions
----------------

Names are matched case-insensitively and through a table of aliases, so
``TMath::ATan2(y, x)``, ``atan2(y, x)`` and ``arctan2(y, x)`` all parse to the
same thing. The aliases are ``ln`` for ``log``, ``power`` for ``pow``, and the
``asin``/``acos``/``atan``/``atan2``/``asinh``/``acosh``/``atanh`` spellings of
the inverse trigonometric functions.

A dash below means the language has no faithful equivalent, and converting such
an expression to it raises ``ValueError`` rather than approximating.

Common functions
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. list-table::
   :header-rows: 1
   :widths: 22 26 26 26

   * - Canonical name
     - ROOT
     - NumExpr
     - Python
   * - ``sqrt``
     - ``TMath::Sqrt``
     - ``sqrt``
     - ``np.sqrt``
   * - ``abs``
     - ``TMath::Abs``
     - ``abs``
     - ``np.abs``
   * - ``pow``
     - ``TMath::Power``
     - ``**``
     - ``np.power``
   * - ``exp``
     - ``TMath::Exp``
     - ``exp``
     - ``np.exp``
   * - ``log``
     - ``TMath::Log``
     - ``log``
     - ``np.log``
   * - ``log2``
     - ``TMath::Log2``
     - —
     - —
   * - ``log10``
     - ``TMath::Log10``
     - ``log10``
     - ``np.log10``
   * - ``log1p``
     - —
     - ``log1p``
     - ``np.log1p``
   * - ``expm1``
     - —
     - ``expm1``
     - ``np.expm1``
   * - ``sin``
     - ``TMath::Sin``
     - ``sin``
     - ``np.sin``
   * - ``cos``
     - ``TMath::Cos``
     - ``cos``
     - ``np.cos``
   * - ``tan``
     - ``TMath::Tan``
     - ``tan``
     - ``np.tan``
   * - ``arcsin``
     - ``TMath::ASin``
     - ``arcsin``
     - ``np.arcsin``
   * - ``arccos``
     - ``TMath::ACos``
     - ``arccos``
     - ``np.arccos``
   * - ``arctan``
     - ``TMath::ATan``
     - ``arctan``
     - ``np.arctan``
   * - ``arctan2``
     - ``TMath::ATan2``
     - ``arctan2``
     - ``np.arctan2``
   * - ``sinh``
     - ``TMath::SinH``
     - ``sinh``
     - ``np.sinh``
   * - ``cosh``
     - ``TMath::CosH``
     - ``cosh``
     - ``np.cosh``
   * - ``tanh``
     - ``TMath::TanH``
     - ``tanh``
     - ``np.tanh``
   * - ``arcsinh``
     - ``TMath::ASinH``
     - ``arcsinh``
     - ``np.arcsinh``
   * - ``arccosh``
     - ``TMath::ACosH``
     - ``arccosh``
     - ``np.arccosh``
   * - ``arctanh``
     - ``TMath::ATanH``
     - ``arctanh``
     - ``np.arctanh``
   * - ``ceil``
     - ``TMath::Ceil``
     - ``ceil``
     - ``np.ceil``
   * - ``floor``
     - ``TMath::Floor``
     - ``floor``
     - ``np.floor``

``pow`` has no function spelling in NumExpr, where it is written as the ``**``
operator; ``TMath::Power(x, y)`` therefore converts to ``(x ** y)``, and a
``pow`` call with any other number of arguments has nothing to convert to.

Array reductions
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

These take one array and return a scalar. ROOT spells them with a trailing
``$``.

.. list-table::
   :header-rows: 1
   :widths: 22 26 26 26

   * - Canonical name
     - ROOT
     - NumExpr
     - Python
   * - ``sum``
     - ``Sum$``
     - ``sum``
     - ``np.sum``
   * - ``prod``
     - —
     - ``prod``
     - ``np.prod``
   * - ``min``
     - ``Min$``
     - ``min``
     - ``np.min``
   * - ``max``
     - ``Max$``
     - ``max``
     - ``np.max``
   * - ``length``
     - ``Length$``
     - —
     - —

Element-wise minimum and maximum
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

``TMath::Min`` and ``TMath::Max`` take *two* arguments and compare them
element-wise, which is a different operation from the reductions above. They are
tracked separately so that ``Min$(arr)`` and ``TMath::Min(a, b)`` do not collide.

.. list-table::
   :header-rows: 1
   :widths: 22 26 26 26

   * - Canonical name
     - ROOT
     - NumExpr
     - Python
   * - ``tmath_min``
     - ``TMath::Min``
     - —
     - ``np.minimum``
   * - ``tmath_max``
     - ``TMath::Max``
     - —
     - ``np.maximum``

NumExpr's ``min`` and ``max`` are the reductions, not these, so there is nothing
to convert them to; the equivalent would be ``where(a < b, a, b)``, which is an
expression rather than a function name:

.. jupyter-execute::

   try:
       formulate.from_root("TMath::Min(a, b)").to_numexpr()
   except ValueError as error:
       print(error)

NumExpr-specific functions
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. list-table::
   :header-rows: 1
   :widths: 22 26 26 26

   * - Canonical name
     - ROOT
     - NumExpr
     - Python
   * - ``where``
     - —
     - ``where``
     - ``np.where``
   * - ``conj``
     - —
     - ``conj``
     - ``np.conj``
   * - ``real``
     - —
     - ``real``
     - ``np.real``
   * - ``imag``
     - —
     - ``imag``
     - ``np.imag``
   * - ``complex``
     - —
     - ``complex``
     - ``np.complex128``
   * - ``contains``
     - —
     - ``contains``
     - —

``contains`` is a substring test, and NumPy has no equivalent that can be
written as a single function name, so it converts to neither of the other two.

ROOT-specific functions
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

The rest of ``TMath`` that formulate knows about. None of these have NumExpr or
NumPy equivalents, so they can only be converted back to ROOT — but they parse,
which is what makes :attr:`~formulate.AST.AST.variables` usable on any ROOT
expression.

.. list-table::
   :header-rows: 1
   :widths: 30 70

   * - Arguments
     - ``TMath`` functions
   * - One
     - ``BesselI0``, ``BesselI1``, ``BesselJ0``, ``BesselJ1``, ``BesselY0``,
       ``BesselY1``, ``CeilNint``, ``DiLog``, ``Erf``, ``Erfc``,
       ``ErfInverse``, ``ErfcInverse``, ``Even``, ``Factorial``,
       ``FloorNint``, ``Freq``, ``KolmogorovProb``, ``LandauI``, ``LnGamma``,
       ``NextPrime``, ``NormQuantile``, ``Odd``, ``StruveH0``, ``StruveH1``,
       ``StruveL0``, ``StruveL1``
   * - Two
     - ``BesselI``, ``BesselK``, ``Beta``, ``Binomial``,
       ``ChisquareQuantile``, ``Ldexp``, ``Permute``, ``Poisson``,
       ``PoissonI``, ``Prob``, ``Student``, ``StudentI``
   * - Three
     - ``AreEqualAbs``, ``AreEqualRel``, ``BetaCf``, ``BetaDist``,
       ``BetaDistI``, ``BetaIncomplete``, ``BinomialI``, ``BubbleHigh``,
       ``BubbleLow``, ``FDist``, ``FDistI``, ``Vavilov``, ``VavilovI``
   * - Four or more
     - ``Gaus``, ``RootsCubic``, ``Quantiles``

.. note::

   formulate does not check how many arguments a function is given — the tables
   above record what ROOT's signatures are, but ``TMath::Erf(a, b)`` will parse
   and convert. The one exception is ``pow`` converted to NumExpr, because the
   ``**`` operator it becomes has nowhere to put a third argument.

Constants
----------------

Constants are recognised by name, and in ROOT also in their ``TMath::X()`` call
form. They are stored canonically, so ``TMath::E()``, ``e_num`` and ``ℯ`` are
the same constant and all report as ``exp1``.

NumExpr has no symbolic constants, so converting to it — and to Python, for the
numeric ones — substitutes the value. This is a one-way street: see
:ref:`issues-constants-round-trip`.

A few constants have no single-name spelling in a backend — ``hbarc`` is a
product, ``eminus`` and ``neginf`` are negations — and those are emitted
parenthesized, exactly as shown below, so that they keep binding as one atom
under ``**``.

Mathematical constants
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. list-table::
   :header-rows: 1
   :widths: 18 26 28 28

   * - Canonical name
     - Also accepted as
     - ROOT
     - NumExpr and Python
   * - ``pi``
     - ``π``
     - ``TMath::Pi()``
     - ``3.141592653589793``
   * - ``tau``
     - ``twopi``, ``τ``
     - ``TMath::TwoPi()``
     - ``6.283185307179586``
   * - ``invpi``
     - ``oneoverpi``
     - ``TMath::InvPi()``
     - ``0.3183098861837907``
   * - ``piover2``
     - —
     - ``TMath::PiOver2()``
     - ``1.5707963267948966``
   * - ``piover4``
     - —
     - ``TMath::PiOver4()``
     - ``0.7853981633974483``
   * - ``exp1``
     - ``e``, ``e_num``, ``e_number``, ``e_euler``, ``ℯ``
     - ``TMath::E()``
     - ``2.718281828459045``
   * - ``sqrt2``
     - —
     - ``TMath::Sqrt2()``
     - ``1.4142135623730951``
   * - ``ln10``
     - —
     - ``TMath::Ln10()``
     - ``2.302585092994046``
   * - ``log10e``
     - ``loge``
     - ``TMath::LogE()``
     - ``0.4342944819032518``
   * - ``deg2rad``
     - ``degtorad``
     - ``TMath::DegToRad()``
     - ``0.017453292519943295``
   * - ``rad2deg``
     - ``radtodeg``
     - ``TMath::RadToDeg()``
     - ``57.29577951308232``

Physical constants
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Values come from :mod:`hepunits`, in SI units, matching what ``TMath`` returns.

.. list-table::
   :header-rows: 1
   :widths: 18 22 24 20 16

   * - Canonical name
     - Also accepted as
     - ROOT
     - NumExpr and Python
     - Unit
   * - ``c_light``
     - ``clight``, ``c()``
     - ``TMath::C()``
     - ``299792458.0``
     - m/s
   * - ``h_planck``
     - ``hplanck``, ``h()``
     - ``TMath::H()``
     - ``6.626070149999999e-34``
     - J·s
   * - ``hbar``
     - ``h_bar``, ``ℏ``
     - ``TMath::Hbar()``
     - ``1.0545718176461563e-34``
     - J·s
   * - ``hbarc``
     - ``h_bar_c``, ``ℏc``
     - ``(TMath::Hbar() * TMath::C())``
     - ``3.16152677349669e-26``
     - J·m
   * - ``k_boltzmann``
     - ``kboltzmann``, ``k()``
     - ``TMath::K()``
     - ``1.380649e-23``
     - J/K
   * - ``avogadro``
     - ``na()``
     - ``TMath::Na()``
     - ``6.02214076e+23``
     - 1/mol
   * - ``eplus``
     - ``e_plus``, ``qe()``
     - ``TMath::Qe()``
     - ``1.602176634e-19``
     - C
   * - ``eminus``
     - ``e_minus``
     - ``(-TMath::Qe())``
     - ``(-1.602176634e-19)``
     - C

.. note::

   The single-letter forms — ``e``, ``c``, ``h``, ``k``, ``na``, ``qe`` — are
   recognised only in their call form, ``c()`` or ``TMath::C()``. A bare ``c``
   is a variable, which is what you want when ``c`` is a branch name. This
   changed in v1.0.1; expressions written for older versions that relied on a
   bare ``c`` meaning the speed of light need ``c_light``.

Booleans and special values
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. list-table::
   :header-rows: 1
   :widths: 20 20 20 20 20

   * - Canonical name
     - Also accepted as
     - ROOT
     - NumExpr
     - Python
   * - ``true``
     - ``True``
     - ``true``
     - ``True``
     - ``True``
   * - ``false``
     - ``False``
     - ``false``
     - ``False``
     - ``False``
   * - ``inf``
     - ``infinity``
     - ``TMath::Infinity()``
     - —
     - ``float('inf')``
   * - ``neginf``
     - ``negative_infinity``
     - ``(-TMath::Infinity())``
     - —
     - ``float('-inf')``
   * - ``nan``
     - ``quietnan``, ``signalingnan``
     - ``TMath::QuietNaN()``
     - —
     - ``float('nan')``

NumExpr has no literal for the non-finite values, so those three cannot be
converted to it.

Inspecting an expression
--------------------------------------

Beyond conversion, a parsed expression reports what it refers to. This is what
you want when deciding which branches to read from a file:

.. jupyter-execute::

   expr = formulate.from_root("TMath::Sqrt(px**2 + py**2) > 5 * TMath::Pi() + 1.5")
   print(list(expr.variables))
   print(list(expr.named_constants))
   print(list(expr.unnamed_constants))

Names come out in the order they first appear, and each is reported once. They
are reported as ROOT spells them, which for a dotted branch name is *not* how
``to_numexpr()`` writes it — numexpr cannot take a dot, so those names are
hex-encoded on the way out and it is the encoded name you must supply when you
evaluate. See :ref:`issues-dotted-names`.

``str()`` on the expression shows the parsed structure in canonical names, which
is the quickest way to check how something was grouped:

.. jupyter-execute::

   print(formulate.from_root("a && b < c"))
   print(formulate.from_numexpr("a & b < c"))

Limitations
-----------------------

Anything with no faithful equivalent in the target language raises
``ValueError`` rather than converting to something subtly different — the
dashes throughout this page are all instances of that. The :doc:`issues` page
covers the cases people hit most.

Beyond those:

1. **Not every function is known.** The tables above are hand-maintained, and a
   name that is not in them raises rather than being passed through, so that a
   typo does not become a mysterious failure in the target engine. If something
   is missing, please open an issue — or add it: a function is one entry per
   table, and :doc:`../contributing/contributing` describes how.

2. **User-defined functions are not supported**, for the same reason.

3. **Argument counts are not validated**, except for ``pow``.

4. **Strings are not supported.** NumExpr's ``contains`` takes them, but
   formulate's grammars only accept numbers, names and operators, so an
   expression containing a string literal will not parse.

5. **Types are not tracked.** formulate translates syntax; whether a branch is
   an integer or a float, a scalar or an array, is something only the target
   engine knows. This is what makes ``%`` dangerous — see :ref:`issues-modulo`.
