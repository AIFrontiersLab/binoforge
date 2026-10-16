from __future__ import annotations


class CallBudget:
    def __init__(self, limit: int = 12) -> None:
        self.limit = limit
        self.used = 0

    def take(self, tool: str) -> int:
        self.used += 1
        if self.used > self.limit:
            raise RuntimeError(f"call budget exhausted on {tool}")
        return self.used
