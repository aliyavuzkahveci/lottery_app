"""
# -----------------------------------------------------------------------------#
#                                                                              #
#                            Python script                                     #
#                                                                              #
# -----------------------------------------------------------------------------#
Description  :
Implementation of exceptions utilized in the application

# -----------------------------------------------------------------------------#
#                                                                              #
#       Copyright (c) 2023 , Ali Yavuz Kahveci.                                #
#                         All rights reserved                                  #
#                                                                              #
# -----------------------------------------------------------------------------#
"""
import functools

import structlog

LOGGER = structlog.get_logger()


class BadRequestException(Exception):
    pass


def catch_exceptions():
    def catch_exceptions_decorator(job_func):
        @functools.wraps(job_func)
        def wrapper(*args, **kwargs):
            try:
                return job_func(*args, **kwargs)
            except Exception as exc:
                LOGGER.exception(
                    f"Exception occurred while running the scheduled task: {exc}"
                )

        return wrapper

    return catch_exceptions_decorator
