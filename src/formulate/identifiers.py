# Licensed under a 3-clause BSD style license, see LICENSE.

"""The tables that say how each name is spelled in each language.

``FUNCTIONS`` and ``CONSTANTS`` hold the canonical names — the ones that appear
inside the AST — and the ``ROOT_*``, ``NUMEXPR_*`` and ``PYTHON_*`` maps give
each backend's spelling of them. A canonical name absent from a backend's map
is how "not supported here" is expressed: rendering it raises ``ValueError``
rather than emitting an approximation.

The ``*_ALIASES`` maps go the other way, folding the surface spellings a parser
may see onto one canonical name, which is what makes ``TMath::ATan2``,
``atan2`` and ``arctan2`` the same function, and ``e_num``, ``e_euler`` and
``TMath::E()`` the same constant.

Numeric values for the physical constants come from :mod:`hepunits`, so they
agree with the rest of Scikit-HEP.
"""

import math

from hepunits import constants
from hepunits.units import coulomb, e_SI, electronvolt, joule, kelvin, m, mole, s

UNARY_OPERATORS = {"pos", "neg", "inv"}
"""Canonical names of the operators a :class:`~formulate.AST.UnaryOperator` may use."""

BINARY_OPERATORS = {
    "add",
    "sub",
    "mul",
    "div",
    "mod",
    "lt",
    "gt",
    "lte",
    "gte",
    "eq",
    "neq",
    "and",
    "or",
    "xor",
    "pow",
    "multi_out",
}
"""Canonical names of the operators a :class:`~formulate.AST.BinaryOperator` may use."""

COMMON_OPERATOR_SYMBOLS = {
    "pos": "+",
    "neg": "-",
    "add": "+",
    "sub": "-",
    "mul": "*",
    "div": "/",
    "mod": "%",
    "lt": "<",
    "gt": ">",
    "lte": "<=",
    "gte": ">=",
    "eq": "==",
    "neq": "!=",
    "pow": "**",
}
"""Operator spellings that all three languages agree on."""

NUMEXPR_OPERATOR_SYMBOLS = {
    **COMMON_OPERATOR_SYMBOLS,
    "inv": "~",
    "and": "&",
    "or": "|",
    "xor": "^",
}
"""NumExpr's spelling of each operator."""

ROOT_OPERATOR_SYMBOLS = {
    **COMMON_OPERATOR_SYMBOLS,
    "inv": "!",
    "and": "&&",
    "or": "||",
    # xor is not supported since ^ is interpreted as a power operator
    "multi_out": ":",
}
"""ROOT's spelling of each operator. There is no ``xor``, since ROOT reads ``^`` as
exponentiation."""

PYTHON_OPERATOR_SYMBOLS = {
    # "inv" is deliberately absent, and handled by PYTHON_UNARY_FUNCTIONS
    # instead; see the comment there.
    **{op: symbol for op, symbol in NUMEXPR_OPERATOR_SYMBOLS.items() if op != "inv"},
    "multi_out": ",",
}
"""Python's spelling of each operator. ``inv`` is absent on purpose; see
:data:`PYTHON_UNARY_FUNCTIONS`."""

# Operators that Python spells as a function call rather than as a symbol.
#
# ROOT's "!" is a logical NOT and NumPy's "~" is a bitwise inversion. They agree
# on booleans, which is the common case, but not on integers: ROOT reads "!5" as
# 0 while "~5" is -6 in NumPy. np.logical_not is what ROOT's "!" means for every
# dtype, and is identical to "~" when the operand is boolean, so it is used
# unconditionally. (NumExpr needs no such treatment: its "~" has no opcode for
# anything but booleans, so a mistranslation there fails loudly instead.)
PYTHON_UNARY_FUNCTIONS = {"inv": "logical_not"}
"""Unary operators Python writes as a function call rather than as a symbol. Takes
precedence over :data:`PYTHON_OPERATOR_SYMBOLS`."""

# Later on we could add Python libraries as "namespaces" here
NAMESPACES = {"tmath"}
"""Namespace prefixes a function name may carry, lower-cased."""

FUNCTIONS = {
    # Common functions
    "sqrt",
    "abs",
    "pow",
    "log",
    "log10",
    "exp",
    "sin",
    "cos",
    "tan",
    "arcsin",
    "arccos",
    "arctan",
    "arctan2",
    "sinh",
    "cosh",
    "tanh",
    "arcsinh",
    "arccosh",
    "arctanh",
    "ceil",
    "floor",
    # Functions specific to NumExpr
    "log1p",
    "expm1",
    "where",
    "conj",
    "real",
    "imag",
    "complex",
    "contains",
    # Functions specific to ROOT
    # One argument
    "besseli0",
    "besseli1",
    "besselj0",
    "besselj1",
    "bessely0",
    "bessely1",
    "ceilnint",
    "dilog",
    "erf",
    "erfc",
    "erfinverse",
    "erfcinverse",
    "even",
    "factorial",
    "floornint",
    "freq",
    "kolmogorovprob",
    "landaui",
    "lngamma",
    "log2",
    "nextprime",
    "normquantile",
    "odd",
    "struveh0",
    "struveh1",
    "struvel0",
    "struvel1",
    # Two arguments
    "besseli",
    "besselk",
    "beta",
    "binomial",
    "chisquarequantile",
    "ldexp",
    "permute",
    "poisson",
    "poissoni",
    "prob",
    "student",
    "studenti",
    # Three arguments
    "areequalabs",
    "areequalrel",
    "betacf",
    "betadist",
    "betadisti",
    "betaincomplete",
    "binomiali",
    "bubblehigh",
    "bubblelow",
    "fdist",
    "fdisti",
    "vavilov",
    "vavilovi",
    # 4+ arguments
    "gaus",
    "rootscubic",
    "quantiles",
    # Array to scalar functions
    "sum",
    "prod",
    "min",
    "max",
    "length",
    # TMath scalar functions that collide with array-reduction names
    "tmath_min",
    "tmath_max",
}
"""Canonical names of every function formulate knows."""

FUNCTION_ALIASES = {
    "ln": "log",
    "asin": "arcsin",
    "acos": "arccos",
    "atan": "arctan",
    "atan2": "arctan2",
    "asinh": "arcsinh",
    "acosh": "arccosh",
    "atanh": "arctanh",
    "power": "pow",
}
"""Other spellings of a function, mapped onto its canonical name."""

# Canonical names that no language spells that way, so that an error message
# names something the reader could have written. Every other canonical name is
# already a spelling some language accepts, and is used as-is.
FUNCTION_DISPLAY_NAMES = {
    "tmath_min": "TMath::Min",
    "tmath_max": "TMath::Max",
}
"""How to name a function in an error message, where its canonical name is internal."""

# https://numexpr.readthedocs.io/en/latest/user_guide.html#supported-functions
NUMEXPR_FUNCTIONS = {
    "sqrt": "sqrt",
    "abs": "abs",
    "log": "log",
    "log10": "log10",
    "log1p": "log1p",
    "exp": "exp",
    "expm1": "expm1",
    "sin": "sin",
    "cos": "cos",
    "tan": "tan",
    "arcsin": "arcsin",
    "arccos": "arccos",
    "arctan": "arctan",
    "arctan2": "arctan2",
    "sinh": "sinh",
    "cosh": "cosh",
    "tanh": "tanh",
    "arcsinh": "arcsinh",
    "arccosh": "arccosh",
    "arctanh": "arctanh",
    "where": "where",
    "conj": "conj",
    "real": "real",
    "imag": "imag",
    "complex": "complex",
    "contains": "contains",
    "ceil": "ceil",
    "floor": "floor",
    "sum": "sum",
    "prod": "prod",
    "min": "min",
    "max": "max",
    # tmath_min/tmath_max are deliberately absent: NumExpr's min and max are
    # reductions over one array, not the element-wise two-argument functions
    # TMath::Min/TMath::Max are, and "min(a, b)" is rejected by NumExpr. The
    # equivalent is "where(a < b, a, b)", which is not a plain function name.
}
"""NumExpr's spelling of each function it supports."""

# https://root.cern.ch/doc/master/namespaceTMath.html
ROOT_FUNCTIONS = {
    "sqrt": "TMath::Sqrt",
    "abs": "TMath::Abs",
    "pow": "TMath::Power",
    "log": "TMath::Log",
    "log2": "TMath::Log2",
    "log10": "TMath::Log10",
    "exp": "TMath::Exp",
    "sin": "TMath::Sin",
    "cos": "TMath::Cos",
    "tan": "TMath::Tan",
    "arcsin": "TMath::ASin",
    "arccos": "TMath::ACos",
    "arctan": "TMath::ATan",
    "arctan2": "TMath::ATan2",
    "sinh": "TMath::SinH",
    "cosh": "TMath::CosH",
    "tanh": "TMath::TanH",
    "arcsinh": "TMath::ASinH",
    "arccosh": "TMath::ACosH",
    "arctanh": "TMath::ATanH",
    # One argument
    "besseli0": "TMath::BesselI0",
    "besseli1": "TMath::BesselI1",
    "besselj0": "TMath::BesselJ0",
    "besselj1": "TMath::BesselJ1",
    "bessely0": "TMath::BesselY0",
    "bessely1": "TMath::BesselY1",
    "ceil": "TMath::Ceil",
    "ceilnint": "TMath::CeilNint",
    "dilog": "TMath::DiLog",
    "erf": "TMath::Erf",
    "erfc": "TMath::Erfc",
    "erfinverse": "TMath::ErfInverse",
    "erfcinverse": "TMath::ErfcInverse",
    "even": "TMath::Even",
    "factorial": "TMath::Factorial",
    "floor": "TMath::Floor",
    "floornint": "TMath::FloorNint",
    "freq": "TMath::Freq",
    "kolmogorovprob": "TMath::KolmogorovProb",
    "landaui": "TMath::LandauI",
    "lngamma": "TMath::LnGamma",
    "nextprime": "TMath::NextPrime",
    "normquantile": "TMath::NormQuantile",
    "odd": "TMath::Odd",
    "struveh0": "TMath::StruveH0",
    "struveh1": "TMath::StruveH1",
    "struvel0": "TMath::StruveL0",
    "struvel1": "TMath::StruveL1",
    # Two arguments
    "besseli": "TMath::BesselI",
    "besselk": "TMath::BesselK",
    "beta": "TMath::Beta",
    "binomial": "TMath::Binomial",
    "chisquarequantile": "TMath::ChisquareQuantile",
    "ldexp": "TMath::Ldexp",
    "permute": "TMath::Permute",
    "poisson": "TMath::Poisson",
    "poissoni": "TMath::PoissonI",
    "prob": "TMath::Prob",
    "student": "TMath::Student",
    "studenti": "TMath::StudentI",
    # Three arguments
    "areequalabs": "TMath::AreEqualAbs",
    "areequalrel": "TMath::AreEqualRel",
    "betacf": "TMath::BetaCf",
    "betadist": "TMath::BetaDist",
    "betadisti": "TMath::BetaDistI",
    "betaincomplete": "TMath::BetaIncomplete",
    "binomiali": "TMath::BinomialI",
    "bubblehigh": "TMath::BubbleHigh",
    "bubblelow": "TMath::BubbleLow",
    "fdist": "TMath::FDist",
    "fdisti": "TMath::FDistI",
    "vavilov": "TMath::Vavilov",
    "vavilovi": "TMath::VavilovI",
    # 4+ arguments
    "gaus": "TMath::Gaus",
    "rootscubic": "TMath::RootsCubic",
    "quantiles": "TMath::Quantiles",
    # Array functions in ROOT
    "sum": "Sum$",
    "min": "Min$",
    "max": "Max$",
    "length": "Length$",
    # Scalar two-argument functions (distinct from array reductions above)
    "tmath_min": "TMath::Min",
    "tmath_max": "TMath::Max",
}
"""ROOT's spelling of each function it supports."""

PYTHON_FUNCTIONS = {
    # NumExpr's contains() is a substring test with no NumPy equivalent that can
    # be written as a single function name (np.strings.find(a, b) != -1 is an
    # expression, not a name), so Python rejects it just as ROOT does.
    **{name: func for name, func in NUMEXPR_FUNCTIONS.items() if name != "contains"},
    "pow": "power",
    "complex": "complex128",
    # np.minimum/maximum are the element-wise equivalents of TMath::Min/Max
    "tmath_min": "minimum",
    "tmath_max": "maximum",
}
"""NumPy's name for each function it supports, without the ``np.`` prefix, which is
added when the expression is rendered."""

CONSTANTS = {
    "true",
    "false",
    "inf",
    "neginf",
    "nan",
    "sqrt2",
    "exp1",
    "pi",
    "invpi",
    "piover2",
    "piover4",
    "tau",
    "ln10",
    "log10e",
    "deg2rad",
    "rad2deg",
    "avogadro",
    "k_boltzmann",
    "c_light",
    "eminus",
    "eplus",
    "h_planck",
    "hbar",
    "hbarc",
}
"""Canonical names of every constant formulate knows. A :class:`~formulate.AST.Symbol`
whose name is in here is a constant; every other symbol is a variable."""

CONSTANTS_ALIASES = {
    "π": "pi",
    "oneoverpi": "invpi",
    "twopi": "tau",
    "τ": "tau",
    # This is U+212F, not e.
    "ℯ": "exp1",  # noqa: RUF001
    "e_number": "exp1",
    "e_euler": "exp1",
    "e_num": "exp1",
    "e_plus": "eplus",
    "e_minus": "eminus",
    "kboltzmann": "k_boltzmann",
    "clight": "c_light",
    "hplanck": "h_planck",
    "ℏ": "hbar",
    "h_bar": "hbar",
    "ℏc": "hbarc",
    "h_bar_c": "hbarc",
    # ∞ is not a valid identifier, so it was not included here
    "infinity": "inf",
    "negative_infinity": "neginf",
    "quietnan": "nan",
    "signalingnan": "nan",
    "loge": "log10e",
    "degtorad": "deg2rad",
    "radtodeg": "rad2deg",
}
"""Other spellings of a constant, mapped onto its canonical name."""

CONSTANTS_FUNCTION_ALIASES = {
    "e": "exp1",
    "c": "c_light",
    "h": "h_planck",
    "k": "k_boltzmann",
    "na": "avogadro",
    "qe": "eplus",
}
"""Constants recognised only in call form, such as ``c()``. Kept separate so that a bare
``c`` stays a variable, since short branch names are common."""

NUMEXPR_CONSTANTS = {
    "true": True,
    "false": False,
    # inf, neginf, nan not supported
    "sqrt2": math.sqrt(2),
    "exp1": math.e,
    "pi": math.pi,
    "invpi": 1 / math.pi,
    "piover2": math.pi / 2,
    "piover4": math.pi / 4,
    "tau": 2 * math.pi,
    "ln10": math.log(10),
    "log10e": math.log10(math.e),
    "deg2rad": math.pi / 180,
    "rad2deg": 180 / math.pi,
    "avogadro": constants.Avogadro / (1 / mole),
    "k_boltzmann": constants.k_Boltzmann / (joule / kelvin),
    "c_light": constants.c_light / (m / s),
    "eminus": constants.eminus / (coulomb),
    "eplus": -constants.eminus / (coulomb),
    "h_planck": constants.h_Planck / (electronvolt * s / e_SI),
    "hbar": constants.hbar / (electronvolt * s / e_SI),
    "hbarc": constants.hbarc / (electronvolt * m / e_SI),
}
"""The value substituted for each constant when rendering to NumExpr, which has no
symbolic constants of its own."""

ROOT_CONSTANTS = {
    "true": "true",
    "false": "false",
    "inf": "TMath::Infinity()",
    "neginf": "(-TMath::Infinity())",
    "nan": "TMath::QuietNaN()",
    "sqrt2": "TMath::Sqrt2()",
    "exp1": "TMath::E()",
    "pi": "TMath::Pi()",
    "invpi": "TMath::InvPi()",
    "piover2": "TMath::PiOver2()",
    "piover4": "TMath::PiOver4()",
    "tau": "TMath::TwoPi()",
    "ln10": "TMath::Ln10()",
    "log10e": "TMath::LogE()",
    "deg2rad": "TMath::DegToRad()",
    "rad2deg": "TMath::RadToDeg()",
    "avogadro": "TMath::Na()",
    "k_boltzmann": "TMath::K()",
    "c_light": "TMath::C()",
    "eminus": "(-TMath::Qe())",
    "eplus": "TMath::Qe()",
    "h_planck": "TMath::H()",
    "hbar": "TMath::Hbar()",
    "hbarc": "(TMath::Hbar() * TMath::C())",
}
"""ROOT's spelling of each constant, usually a ``TMath`` call."""

PYTHON_CONSTANTS = {
    **NUMEXPR_CONSTANTS,
    "inf": "float('inf')",
    "neginf": "float('-inf')",
    "nan": "float('nan')",
}
"""The value substituted for each constant when rendering to Python."""
