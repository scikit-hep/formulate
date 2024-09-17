"""
Copyright (c) 2023 Aryan Roy. All rights reserved.

formulate:  Easy conversions between different styles of expressions
"""
from __future__ import annotations

from . import numexpr_parser
from . import  ttreeformula_parser

UNARY_OP = {"pos", "neg", "binv", "linv"}
with_sign = {}
val_to_sign = {
    "add": "+",
    "sub": "-",
    "div": "/",
    "mul": "*",
    "lt": "<",
    "gt": ">",
    "lte": "<=",
    "gte": ">=",
    "eq": "==",
    "neq": "!=",
    "band": "&",
    "bor": "|",
    "bxor": "^",
    "linv": "!",
    "land": "&&",
    "lor": "||",
    "neg": "-",
    "pos": "+",
    "binv": "~",
    "linv": "!",
    "pow": "**",
}


def _ptree_to_string(exp_tree, out_exp: list):
    if isinstance(exp_tree, numexpr_parser.Token) or isinstance(exp_tree, ttreeformula_parser.Token):
        out_exp.append(str(exp_tree))
        return out_exp

    elif exp_tree is None:
        return out_exp

    elif isinstance(exp_tree.data, numexpr_parser.Token) or isinstance(exp_tree.data, ttreeformula_parser.Token):
        cur_type = exp_tree.data.type
        cur_val = exp_tree.data.value
        children = exp_tree.children
        if cur_type == "CNAME" or cur_type == "NUMBER":
            out_exp.append(str(children[0]))
        else:
            if len(children) == 1:
                if cur_val in with_sign:
                    out_exp.append("(")
                    out_exp.append(val_to_sign[cur_val])
                out_exp.extend(_ptree_to_string(children[0], []))
                if cur_val in with_sign:
                    out_exp.append(")")
            else:
                out_exp.append("(")
                out_exp.extend(_ptree_to_string(children[0], []))
                # print(len(exp_tree.children))
                out_exp.append(val_to_sign[cur_val])
                out_exp.extend(_ptree_to_string(children[1], []))
                out_exp.append(")")

    else:
        children = exp_tree.children
        # print(exp_tree, "adwe")
        if exp_tree.data in UNARY_OP:
            child = exp_tree.children[0]
            out_exp.append("(")
            out_exp.append(val_to_sign[exp_tree.data])
            out_exp.extend(_ptree_to_string(child, []))
            out_exp.append(")")
            return out_exp

        if len(children) == 1 and (
            children[0].type == "CNAME" or children[0].type == "NUMBER"
        ):
            # print(str(children[0]))
            out_exp.append(str(children[0]))
            return out_exp

        if exp_tree.data == "func":
            children = exp_tree.children
            head = children[0]
            tail = children[1]
            pre_name = head.children[0]
            out_exp.append(str(pre_name))

            if len(head.children) > 1:
                subchild = head.children[1]

                while not (isinstance(subchild, numexpr_parser.Token) or isinstance(subchild, ttreeformula_parser.Token)):
                    out_exp.append("::")
                    out_exp.append(str(subchild.children[0]))

                    if len(subchild.children) > 1:
                        subchild = subchild.children[1]
                    else:
                        break

            out_exp.append("(")
            out_exp.extend(_ptree_to_string(tail, []))
            out_exp.append(")")
            return out_exp
            
        if exp_tree.data != "matr":
            out_exp.append("(")
        out_exp.extend(_ptree_to_string(children[0], []))

        for i in range(1, len(children)):

            if exp_tree.data == "matr":
                out_exp.append("[")

            else:
                out_exp.append(val_to_sign[exp_tree.data])
            out_exp.extend(_ptree_to_string(children[i], []))

            if exp_tree.data == "matr":
                out_exp.append("]")
                
        if exp_tree.data != "matr":
            out_exp.append(")")
    return out_exp
