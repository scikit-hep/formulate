from __future__ import annotations

try:
    from lark import LarkError, ParseError
except ImportError:

    class LarkError(Exception):
        pass

    class ParseError(LarkError):
        pass
