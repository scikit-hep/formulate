# Licensed under a 3-clause BSD style license, see LICENSE.
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import logging


__all__ = [
    'logger'
]


LOGGER_NAME = 'formulate'

try:
    import colorlog
    handler = colorlog.StreamHandler()
    handler.setFormatter(colorlog.ColoredFormatter(
        '%(log_color)s%(levelname)s:%(name)s:%(message)s'))

    logger = colorlog.getLogger(LOGGER_NAME)
    logger.addHandler(handler)
except ImportError:
    logging.basicConfig()
    logger = logging.getLogger(LOGGER_NAME)


logger.setLevel(logging.WARN)
