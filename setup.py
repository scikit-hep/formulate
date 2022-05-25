#!/usr/bin/env python
# Licensed under a 3-clause BSD style license, see LICENSE.
# testing if packages are installed
import setuptools_scm  # noqa: F401

# import toml  # noqa: F401
from setuptools import setup

extras = {
    "test": ["pytest>=4.6", "numexpr", "pytest-helpers-namespace"],
}
extras["dev"] = extras["test"]

extras["all"] = sum(extras.values(), [])
setup(extras_require=extras)
