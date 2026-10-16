from __future__ import annotations

TERMINAL = {"completed", "failed"}


def reconcile_after_timeout(fetch_status, operation_id: str, *, attempts: int = 3) -> dict:
    """Poll durable status. Do not issue another restart from this function."""
    last = None
    for _ in range(attempts):
        last = fetch_status(operation_id)
        state = (last or {}).get("state")
        if state in TERMINAL:
            return {"outcome": "reconciled", "record": last}
        if state != "running":
            break
    return {"outcome": "escalate", "record": last}
