# -*- coding: utf-8 -*-
from __future__ import annotations

import formulate as m
from formulate._compat.typing import Protocol, runtime_checkable


def test_version():
    assert m.__version__


