"""
------------------------------------------------------------
Timer Utility (Gatekeeper AI Platform)
------------------------------------------------------------

Purpose:
- Measure execution time of agents
- Support observability metrics
- Decorator-based profiling
------------------------------------------------------------
"""

import time
from functools import wraps
from utils.logger import logger


##########################################################
# Timing Decorator
##########################################################

def timed(func):

    @wraps(func)
    def wrapper(*args, **kwargs):

        start_time = time.time()

        result = func(*args, **kwargs)

        end_time = time.time()

        duration_ms = (end_time - start_time) * 1000

        logger.info(
            f"{func.__name__} executed in {duration_ms:.2f} ms"
        )

        return result

    return wrapper


##########################################################
# Manual Timer Context Manager
##########################################################

class Timer:

    def __init__(self, name: str = "operation"):

        self.name = name
        self.start = None

    def __enter__(self):

        self.start = time.time()

        return self

    def __exit__(self, exc_type, exc_val, exc_tb):

        end = time.time()

        duration_ms = (end - self.start) * 1000

        logger.info(
            f"{self.name} completed in {duration_ms:.2f} ms"
        )
