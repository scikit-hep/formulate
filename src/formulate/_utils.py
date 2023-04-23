"""
Copyright (c) 2023 Aryan Roy. All rights reserved.

formulate:  Easy conversions between different styles of expressions
"""

import lark
with_sign = {}
val_to_sign = {"add": "+", "sub": "-", "div": "/", "mul": "*", "lt": "<", "gt": ">",\
                "lte": "<=", "gte": ">=", "eq": "==", "neq": "!=", "band": "&"\
                ,"bor": "|","bxor": "^","linv": "!","land": "&&","lor": "||"}



def _ptree_to_string(exp_tree: lark.tree.Tree, out_exp: list):
    # print("==================================")
    # print(exp_tree)
    # print("==================================")
    if isinstance(exp_tree.data, lark.lexer.Token):
        cur_type = exp_tree.data.type
        cur_val = exp_tree.data.value
        children = exp_tree.children
        #print(cur_val)
        if cur_type == "CNAME" or cur_type == "NUMBER":
            out_exp.append(str(children[0]))
        else:
            if len(children) == 1:
                if cur_val in with_sign:
                    out_exp.append("(")
                    out_exp.append(val_to_sign[cur_val])
                out_exp.extend(_ptree_to_string(children[0],[]))
                if cur_val in with_sign:
                    out_exp.append(")")
            else:
                out_exp.append("(")
                out_exp.extend(_ptree_to_string(children[0],[]))
                print(len(exp_tree.children))
                out_exp.append(val_to_sign[cur_val])
                out_exp.extend(_ptree_to_string(children[1],[]))
                out_exp.append(")")
    else:
        children = exp_tree.children
        print(children, "adwe")
        if len(children) == 1 and (children[0].type == "CNAME" or children[0].type == "NUMBER"):
            print(str(children[0]))
            out_exp.append(str(children[0]))
            return out_exp
        out_exp.append("(")
        out_exp.extend(_ptree_to_string(children[0],[]))
        if exp_tree.data == "matr":
            out_exp.append("[")
        else:
            out_exp.append(val_to_sign[exp_tree.data])
        out_exp.extend(_ptree_to_string(children[1],[]))
        if exp_tree.data == "matr":
            out_exp.append("]")
        out_exp.append(")")
    return out_exp
