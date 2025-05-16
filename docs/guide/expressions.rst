Supported Expressions
===================================

Formulate supports a wide range of expressions in both ROOT and numexpr formats. This page documents the supported expression types and syntax.

Operators
----------------

Arithmetic Operators
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Both ROOT and numexpr support the following arithmetic operators:

.. list-table::
   :header-rows: 1
   :widths: 20 40 40

   * - Operator
     - ROOT Example
     - numexpr Example
   * - Addition (+)
     - ``x + y``
     - ``x + y``
   * - Subtraction (-)
     - ``x - y``
     - ``x - y``
   * - Multiplication (*)
     - ``x * y``
     - ``x * y``
   * - Division (/)
     - ``x / y``
     - ``x / y``
   * - Power (**)
     - ``x**2`` or ``TMath::Power(x, 2)``
     - ``x**2``
   * - Modulo (%)
     - ``x % y``
     - ``x % y``

Comparison Operators
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. list-table::
   :header-rows: 1
   :widths: 20 40 40

   * - Operator
     - ROOT Example
     - numexpr Example
   * - Equal (==)
     - ``x == y``
     - ``x == y``
   * - Not Equal (!=)
     - ``x != y``
     - ``x != y``
   * - Greater Than (>)
     - ``x > y``
     - ``x > y``
   * - Less Than (<)
     - ``x < y``
     - ``x < y``
   * - Greater Than or Equal (>=)
     - ``x >= y``
     - ``x >= y``
   * - Less Than or Equal (<=)
     - ``x <= y``
     - ``x <= y``

Logical Operators
~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. list-table::
   :header-rows: 1
   :widths: 20 40 40

   * - Operator
     - ROOT Example
     - numexpr Example
   * - AND
     - ``x && y``
     - ``x & y``
   * - OR
     - ``x || y``
     - ``x | y``
   * - NOT
     - ``!x``
     - ``~x``

Functions
----------------

Formulate supports many mathematical and utility functions. Here are some commonly used functions:

Mathematical Functions
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. list-table::
   :header-rows: 1
   :widths: 30 35 35

   * - Function
     - ROOT Syntax
     - numexpr Syntax
   * - Square Root
     - ``TMath::Sqrt(x)``
     - ``sqrt(x)``
   * - Absolute Value
     - ``TMath::Abs(x)``
     - ``abs(x)``
   * - Exponential
     - ``TMath::Exp(x)``
     - ``exp(x)``
   * - Logarithm (natural)
     - ``TMath::Log(x)``
     - ``log(x)``
   * - Logarithm (base 10)
     - ``TMath::Log10(x)``
     - ``log10(x)``
   * - Sine
     - ``TMath::Sin(x)``
     - ``sin(x)``
   * - Cosine
     - ``TMath::Cos(x)``
     - ``cos(x)``
   * - Tangent
     - ``TMath::Tan(x)``
     - ``tan(x)``
   * - Arc Sine
     - ``TMath::ASin(x)``
     - ``arcsin(x)``
   * - Arc Cosine
     - ``TMath::ACos(x)``
     - ``arccos(x)``
   * - Arc Tangent
     - ``TMath::ATan(x)``
     - ``arctan(x)``
   * - Arc Tangent (2 args)
     - ``TMath::ATan2(y, x)``
     - ``arctan2(y, x)``
   * - Hyperbolic Sine
     - ``TMath::SinH(x)``
     - ``sinh(x)``
   * - Hyperbolic Cosine
     - ``TMath::CosH(x)``
     - ``cosh(x)``
   * - Hyperbolic Tangent
     - ``TMath::TanH(x)``
     - ``tanh(x)``
   * - Floor
     - ``TMath::Floor(x)``
     - ``floor(x)``
   * - Ceiling
     - ``TMath::Ceil(x)``
     - ``ceil(x)``

Statistical Functions
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. list-table::
   :header-rows: 1
   :widths: 30 35 35

   * - Function
     - ROOT Syntax
     - numexpr Syntax
   * - Error Function
     - ``TMath::Erf(x)``
     - ``erf(x)``
   * - Complementary Error Function
     - ``TMath::Erfc(x)``
     - ``erfc(x)``
   * - Gamma Function
     - ``TMath::Gamma(x)``
     - Not directly supported
   * - Log Gamma Function
     - ``TMath::LnGamma(x)``
     - Not directly supported

Complex Expressions
-------------------------------

Formulate can handle complex expressions combining multiple operators and functions:

.. jupyter-execute::
   :hide-code:

    import formulate

.. code-block:: python

    # ROOT expression
    # TODO: doesn't work yet?
    root_expr = "TMath::Sqrt(px**2 + py**2 + pz**2) > 10 && TMath::Abs(eta) < 2.5"

    # Equivalent numexpr expression
    numexpr_expr = "sqrt(px**2 + py**2 + pz**2) > 10 & abs(eta) < 2.5"

    # Convert between them
    from_root = formulate.from_root(root_expr)
    print(from_root.to_numexpr())  # Outputs the numexpr version

    from_numexpr = formulate.from_numexpr(numexpr_expr)
    print(from_numexpr.to_root())  # Outputs the ROOT version

Limitations
-----------------------

While Formulate supports a wide range of expressions, there are some limitations:

1. **Function Support**: Not all functions available in ROOT or numexpr are supported for conversion. If you encounter an unsupported function, please check the API documentation or consider contributing to add support.

2. **Complex Data Types**: Formulate primarily focuses on scalar operations. Operations on complex data types like arrays may have limited support.

3. **Custom Functions**: User-defined functions are not automatically supported for conversion.

4. **Recursion Depth**: Very complex nested expressions might hit recursion limits. If you encounter such issues, consider increasing the recursion limit in Python or simplifying the expression, via ``sys.setrecursionlimit(N)``, with ``N`` above 10'000.

For more details on specific limitations or to request support for additional expressions, please refer to the :doc:`issues` page or open an issue on the GitHub repository.
