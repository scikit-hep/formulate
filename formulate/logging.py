# Licensed under a 3-clause BSD style license, see LICENSE.
from functools import wraps
import logging
import os
import random
import string


__all__ = [
    "logger",
    "add_logging",
]


def get_identifier() -> str:
    """Generate an identifier for keeping track of return values when logging."""
    return "".join(
        random.choice(string.ascii_uppercase + string.digits) for _ in range(5)
    )


def add_logging(func=None, *args, ignore_args=None, ignore_kwargs=None, **kwargs):
    """Decorator to add logging to a method.

    Parameters
    ----------
    func : function
        Function to decorate
    ignore_args : list
        Indices of the arguments to ignore
    ignore_kwargs : list
        Names of the keyword arguments to ignore
    """

    def real_decorator(func):
        @wraps(func)
        def new_func(*args, **kwargs):
            my_id = get_identifier()
            func_name = func.__qualname__

            # Don't log arguments which should be ignored
            _args = [
                a for i, a in enumerate(args) if ignore_args and i not in ignore_args
            ]
            _kwargs = {
                k: v
                for k, v in kwargs.items()
                if ignore_kwargs and k not in ignore_kwargs
            }
            logger.debug(
                f"{my_id} Calling {func_name} with {repr(_args)} and {repr(_kwargs)}"
            )

            result = func(*args, **kwargs)
            logger.debug(f"{my_id}  - Got result {repr(result)}")
            return result

        return new_func

    if func is None:
        return real_decorator
    else:
        return real_decorator(func)


LOGGER_NAME = "formulate"

try:
    import colorlog

    handler = colorlog.StreamHandler()
    handler.setFormatter(
        colorlog.ColoredFormatter("%(log_color)s%(levelname)s:%(name)s:%(message)s")
    )

    logger = colorlog.getLogger(LOGGER_NAME)
    logger.addHandler(handler)
except ImportError:
    logging.basicConfig()
    logger = logging.getLogger(LOGGER_NAME)


try:
    logger.setLevel(
        {
            "CRITICAL": logging.CRITICAL,
            "FATAL": logging.CRITICAL,
            "ERROR": logging.ERROR,
            "WARNING": logging.WARNING,
            "WARN": logging.WARNING,
            "INFO": logging.INFO,
            "DEBUG": logging.DEBUG,
        }[os.environ["FOMULATE_LOG_LEVEL"].upper()]
    )
except KeyError:
    logger.setLevel(logging.WARNING)
