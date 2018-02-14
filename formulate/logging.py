# Licensed under a 3-clause BSD style license, see LICENSE.
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
    import logging

    logging.basicConfig()
    logger = logging.getLogger(LOGGER_NAME)


logger.setLevel(logging.WARN)
