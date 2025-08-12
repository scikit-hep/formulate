from __future__ import annotations

import pathlib

from hatchling.builders.hooks.plugin.interface import BuildHookInterface
from lark import Lark
from lark.tools.standalone import gen_standalone


class CustomBuildHook(BuildHookInterface):
    def initialize(self, version, build_data):  # noqa: ARG002
        parsers = ["numexpr", "ttreeformula"]
        for p in parsers:
            # TODO: Check if we should be more careful with the path
            grammar_path = pathlib.Path(f"src/formulate/{p}_grammar.lark")
            parser_path = pathlib.Path(f"src/formulate/{p}_parser.py")
            parser = Lark(grammar_path.read_text(), parser="lalr")
            gen_standalone(parser, out=parser_path.open("w"))
