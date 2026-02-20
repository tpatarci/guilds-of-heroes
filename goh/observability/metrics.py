"""In-process counters for application metrics."""

from __future__ import annotations

import threading
from collections import defaultdict


class Metrics:
    """Thread-safe in-process counter metrics."""

    def __init__(self) -> None:
        self._counters: dict[str, int] = defaultdict(int)
        self._lock = threading.Lock()

    def increment(self, name: str, amount: int = 1) -> None:
        """Increment a counter by the given amount."""
        with self._lock:
            self._counters[name] += amount

    def get(self, name: str) -> int:
        """Get the current value of a counter."""
        with self._lock:
            return self._counters[name]

    def snapshot(self) -> dict[str, int]:
        """Get a snapshot of all counters."""
        with self._lock:
            return dict(self._counters)

    def reset(self) -> None:
        """Reset all counters (mainly for testing)."""
        with self._lock:
            self._counters.clear()


# Module-level singleton
metrics = Metrics()
