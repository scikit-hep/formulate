#!/usr/bin/env python
# Licensed under a 3-clause BSD style license, see LICENSE.
from __future__ import absolute_import, division, print_function

# testing if packages are installed
import setuptools_scm  # noqa: F401
import toml  # noqa: F401
from setuptools import setup

extras = {
    "dev": ["pytest>=4.6", 'numexpr'],
    "test": ["pytest>=4.6", 'numexpr'],
}

extras["all"] = sum(extras.values(), [])
setup(extras_require=extras)
