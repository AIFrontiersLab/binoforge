TRANSITIONS = {
    "missing": {"running", "completed"},
    "running": {"completed", "running"},
    "completed": {"completed"},
}

def allows(current: str, nxt: str) -> bool:
    return nxt in TRANSITIONS.get(current, set())
