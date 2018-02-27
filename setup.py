#!/usr/bin/env python
# Licensed under a 3-clause BSD style license, see LICENSE.
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import os.path

from setuptools import find_packages
from setuptools import setup


def get_version():
    g = {}
    exec(open(os.path.join('formulate', 'version.py')).read(), g)
    return g['__version__']


setup(name='formulate',
      version=get_version(),
      packages=find_packages(exclude=['tests']),
      scripts=[],
      data_files=[],
      description='Convert between different style of formulae',
      long_description=None,
      author='Chris Burr',
      author_email='c.b@cern.ch',
      maintainer='Chris Burr',
      maintainer_email='c.b@cern.ch',
      url='https://github.com/scikit-hep/formulate',
      download_url='https://github.com/scikit-hep/formulate/releases',
      license='BSD 3-clause',
      test_suite='tests',
      install_requires=['numpy', 'pyparsing>=2.1.9', 'colorlog', 'aenum', 'scipy'],
      setup_requires=['pytest-runner'],
      tests_require=['pytest', 'numexpr'],
      classifiers=[
          'Development Status :: 3 - Alpha',
          'Intended Audience :: Developers',
          'Intended Audience :: Information Technology',
          'Intended Audience :: Science/Research',
          'License :: OSI Approved :: BSD License',
          'Operating System :: Microsoft :: Windows',
          'Operating System :: MacOS',
          'Operating System :: POSIX',
          'Operating System :: Unix',
          'Programming Language :: Python',
          'Programming Language :: Python :: 2.7',
          'Programming Language :: Python :: 3.4',
          'Programming Language :: Python :: 3.5',
          'Programming Language :: Python :: 3.6',
          'Programming Language :: Python :: 3.7',
          'Topic :: Scientific/Engineering',
          'Topic :: Scientific/Engineering :: Information Analysis',
          'Topic :: Scientific/Engineering :: Mathematics',
          'Topic :: Scientific/Engineering :: Physics',
          'Topic :: Software Development',
          'Topic :: Utilities',
          ],
      platforms='Any',
      )
