# Licensed under a 3-clause BSD style license, see LICENSE.

from __future__ import annotations


def error_handler(expr: str, index: int):
    marker = [" " for _ in range(index)]
    temp_out = "".join(marker)
    out = temp_out + "^"
    print(expr)
    print(out)
