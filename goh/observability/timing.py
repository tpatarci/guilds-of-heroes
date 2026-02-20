"""@timed decorator — logs start/end/duration of service functions."""

from __future__ import annotations

import functools
import time
from collections.abc import Callable
from typing import Any, TypeVar

import structlog

logger = structlog.get_logger(__name__)

F = TypeVar("F", bound=Callable[..., Any])

SLOW_THRESHOLD_MS = 500


def timed(func: F) -> F:
    """Decorator that logs function execution time. Warns if > 500ms."""

    @functools.wraps(func)
    def wrapper(*args: Any, **kwargs: Any) -> Any:
        func_name = f"{func.__module__}.{func.__qualname__}"
        logger.info("function.start", function=func_name)

        start = time.monotonic()
        try:
            result = func(*args, **kwargs)
            return result
        finally:
            elapsed_ms = (time.monotonic() - start) * 1000
            log_method = logger.warning if elapsed_ms > SLOW_THRESHOLD_MS else logger.info
            log_method(
                "function.end",
                function=func_name,
                duration_ms=round(elapsed_ms, 2),
            )

    return wrapper  # type: ignore[return-value]
