"""
Copyright (c) 2023 Aryan Roy. All rights reserved.

formulate:  Easy conversions between different styles of expressions
"""


from __future__ import annotations


def error_handler(expr: str, index: int):
    marker = [" " for _ in range(index)]
    temp_out = "".join(marker)
    out = temp_out + "^"
    print(expr)
    print(out)
