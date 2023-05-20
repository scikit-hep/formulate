"""
Copyright (c) 2023 Aryan Roy. All rights reserved.

formulate:  Easy conversions between different styles of expressions
"""


import lark


class ptnode(lark.tree.Tree):
    __match_args__ = ("data", "children")
